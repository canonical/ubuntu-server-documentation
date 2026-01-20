---
myst:
  html_meta:
    description: Enable AMD SEV-SNP confidential computing on Ubuntu 25.04 to run encrypted VMs with memory and register protection from the host.
---

(sev-snp)=
# Confidential Computing with AMD

AMD offers a suite of security features designed to protect virtual machine workloads from unauthorized access by the host operating system and hypervisor. These technologies form a progression of capabilities, with each building upon previous generations:

- {term}`AMD-SME`: **AMD Memory Encryption (SME)** is the foundation, providing transparent encryption of physical memory for both the host OS and guest VMs. It protects against physical attacks on memory but doesn't prevent the hypervisor from accessing VM memory contents.

- {term}`AMD-SEV`: **Secure Encrypted Virtualization (SEV)** extends SME specifically to virtual machines, encrypting each VM's memory with its own key. This prevents the hypervisor from reading or modifying VM memory, but the hypervisor can still access unencrypted CPU registers and state.

- {term}`AMD-SEV-ES`: **SEV with Encrypted State (SEV-ES)** enhances SEV by also encrypting the VM's CPU registers and sensitive state information, preventing the hypervisor from reading or tampering with the guest's execution state during initial VM setup and operation.

- {term}`AMD-SEV-SNP`: **SEV with Secure Nested Paging (SEV-SNP)** represents the most comprehensive protection, adding memory integrity verification to SEV-ES. SEV-SNP prevents the hypervisor from manipulating the memory mapping and encrypts guest memory pages with per-page authentication tags, ensuring data integrity and preventing rollback attacks. These features are available on the latest AMD EPYC CPUs (starting from "Rome"). While using Ubuntu as a guest OS on SEV-SNP VMs has been supported since Ubuntu 24.04 LTS, the host enablement (QEMU and OVMF support) was only added later with Ubuntu 25.04.

This documentation focuses only on {term}`AMD-SEV-SNP`, the latest generation of the AMD Confidential computing technologies.

## Host configuration

To enable `SEV-SNP` on the host, first enable memory-encryption features and SNP in the firmware settings, then allocate Address-Space Identifiers (ASIDs) for SNP use. For further details, see [AMD's documentation](https://docs.amd.com/v/u/en-US/58207-using-sev-with-amd-epyc-processors) and consult the documentation for your specific motherboard or Baseboard Management Controller (BMC).

To check if the host supports `SEV-SNP`:

```bash
$ cat /sys/module/kvm_amd/parameters/sev
Y
$ cpuid -1 -l 0x8000001f
CPU:
   AMD Secure Encryption (0x8000001f):
      SME: secure memory encryption support    = true
      SEV: secure encrypted virtualize support = true
      VM page flush MSR support                = false
      SEV-ES: SEV encrypted state support      = true
      SEV-SNP: SEV secure nested paging        = true
```

To launch a SEV-SNP-enabled VM using `QEMU`, first install `qemu-system-x86_64` and launch a VM with the following parameters:

```bash
qemu-system-x86_64 \
  -enable-kvm \
  -nographic \
  -machine q35 -smp 6 -m 6G \
  -drive "if=virtio,format=qcow2,file=disk.img" \
  -net nic,model=e1000 -net user,hostfwd=tcp::2222-:22 \
  -cpu EPYC-v4 \
  -machine memory-encryption=sev0,vmport=off \
  -object memory-backend-memfd,id=ram1,size=6G,share=true,prealloc=false \
  -machine memory-backend=ram1 \
  -object sev-snp-guest,id=sev0,cbitpos=47,reduced-phys-bits=1,kernel-hashes=on,policy=0x30000 \
  -kernel ./vmlinuz \
  -append "root=/dev/vda1 console=ttyS0" \
  -bios /usr/share/ovmf/OVMF.amdsev.fd
```

* `OVMF.amdsev.fd` is a specific version of [EDK II](https://en.wikipedia.org/wiki/TianoCore_EDK_II).

The important argument that tells `QEMU` that this VM is a SEV-SNP VM is:

```bash
  -object sev-snp-guest,id=sev0,cbitpos=47,reduced-phys-bits=1,kernel-hashes=on \
```

* `cbitpos`: Specifies the position of the C-bit in the physical address. This is a platform-specific value required for SEV to operate correctly.
* `reduced-phys-bits`: Informs the hypervisor that one bit of the physical address space is reserved for memory encryption state (the C-bit) and therefore cannot be used for addressing. As a result, the usable physical address space is reduced by one bit; this is commonly set to 1.
* `kernel-hashes=on`: Ensures that the kernel, initramfs, and kernel command line are measured at VM launch. This option can be disabled; however, when enabled, the kernel must be supplied explicitly using the `-kernel` option.
* `policy`: Defines the SEV-SNP guest security policy enforced at launch. This bitmask controls which features and restrictions are enabled for the guest, such as whether debugging is permitted, whether SMT is allowed, or whether migration is restricted. The policy must be compatible with both the platform firmware and the guest workload, as it directly affects guest capabilities and security guarantees. For further details, see the [QEMU documentation](https://www.qemu.org/docs/master/system/i386/amd-memory-encryption.html).

For more details about these parameters, refer to QEMU documentation pages for [invocation](https://www.qemu.org/docs/master/system/invocation.html) and [AMD SEV](https://www.qemu.org/docs/master/system/i386/amd-memory-encryption.html#sevapi).

## Guest configuration

On the guest side, Ubuntu 24.04 LTS and newer fully support AMD SEV-SNP. You can download the disk image and kernel for your VM from `cloud-images.ubuntu.com`. The latest image and kernel can be found here:
 * https://cloud-images.ubuntu.com/releases/noble/release/ubuntu-24.04-server-cloudimg-amd64.img
 * https://cloud-images.ubuntu.com/releases/noble/release/unpacked/

Once the VM is launched, install `linux-generic` to get the `sev-guest` module and insert it with `modprobe sev-guest`. This will create a new character device on the guest that can be used to generate attestation reports from the TEE: `/dev/sev-guest`.
Finally, you can use AMD's [`snpguest`](https://github.com/virtee/snpguest) to generate an attestation report that can be used for a remote attestation:

```bash
sudo ./snpguest report --random attestation-report.bin request-file.txt
```
