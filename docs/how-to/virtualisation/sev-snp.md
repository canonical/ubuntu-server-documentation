---
myst:
  html_meta:
    description: Enable AMD SEV-SNP confidential computing on Ubuntu 25.04 to run encrypted VMs with memory and register protection from the host.
---

(sev-snp)=
# Confidential Computing with AMD

Secure Encrypted Virtualization - Secure Nested Paging (SEV-SNP) are a set of virtualization features available on the latest AMD EPIC CPUs (starting from "Rome"). These features enable *Confidential Computing* which is a way to better isolate a workload from the hypervisor and the host Operating System.
Virtual Machines launched with SEV-SNP features enabled have their CPU registers protected from the host OS and their memory encrypted and integrity protected. The memory protection relies on the CPU's Memory Management Unit (MMU) which verifies the integrity of the secure pages and generates per-VM encryption keys to encrypt them and prevent the host OS from reading their content.
While using Ubuntu as a guest OS on SEV-SNP VMs has been supported since Ubuntu 24.04 LTS, the host enablement (QEMU and OVMF support) was only added later with Ubuntu 25.04.

## Host configuration

AMD SEV-SNP is fully supported as of Ubuntu 25.04. To launch a VM with these features, enable memory encryption features and SNP in the firmware settings, and then assign Address-Space Identifiers (ASIDs) to SNP. For more details, refer to [AMD's documentation](https://docs.amd.com/v/u/en-US/58207-using-sev-with-amd-epyc-processors) and to the manuals for your specific mainboard or Baseboard Management Controller (BMC).

On the host OS, install `qemu-system-x86_64` and launch QEMU with the following parameters:

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
  -object sev-snp-guest,id=sev0,cbitpos=47,reduced-phys-bits=1,kernel-hashes=on \
  -kernel ./vmlinuz \
  -append "root=/dev/vda1 console=ttyS0" \
  -bios /usr/share/ovmf/OVMF.amdsev.fd
```

Here we are configuring the VM to use 6GB of encrypted memory:
* `cbitpos` and `reduced-phys-bits` have to be `47` and `1` respectively for all EPYC CPUs.
* `kernel-hashes=on` makes sure the kernel, initramfs and command line will be measured during the launch. It can be disabled but if enabled, the kernel needs to be provided with `-kernel`
* `OVMF.amdsev.fd` is a specific version of [EDK II](https://en.wikipedia.org/wiki/TianoCore_EDK_II).

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
