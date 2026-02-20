---
myst:
  html_meta:
    description: Enable Intel TDX confidential computing on Ubuntu to run encrypted Trust Domain VMs with memory and CPU state protection from the host.
---

(intel-tdx)=
# 1. Confidential Computing with Intel® Trust Domain Extensions (TDX)

{term}`Intel TDX` is a Confidential Computing technology which deploys hardware-isolated Virtual Machines (VMs) called Trust Domains (TDs). It protects TDs from a broad range of software attacks by isolating them from the Virtual-Machine Manager (VMM), hypervisor, and other non-TD software on the host platform. As a result, Intel TDX enhances a platform user's control of data security and IP protection. It also enhances the Cloud Service Providers' (CSP) ability to provide managed cloud services without exposing tenant data to adversaries. For more information, see the [Intel TDX overview](https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/overview.html).

Ubuntu supports Intel TDX for both host and guest operating systems. Guest support is available from Ubuntu 24.04 LTS onwards, while host support begins with Ubuntu 25.10.

<a id="supported-hardware"></a>
## 2. Supported hardware
This table lists Intel® Xeon® processors that support Intel TDX:

| Processor | Code Name | TDX Module Version |
| - | - | - |
| 4th Gen Intel® Xeon® Scalable Processors (select SKUs with Intel® TDX) | Sapphire Rapids | 1.5.x |
| 5th Gen Intel® Xeon® Scalable Processors | Emerald Rapids | 1.5.x |
| Intel® Xeon® 6 Processors with E-Cores | Sierra Forest | 1.5.x |
| Intel® Xeon® 6 Processors with P-Cores | Granite Rapids | 2.0.x |

## 3. Configure host

To enable Intel TDX on the host, BIOS and host OS configurations are required.

1. First, enable Intel TDX settings in the BIOS.

:::{note}
The following is a sample BIOS configuration. The necessary BIOS settings or menus may differ based on the platform used. Reach out to your OEM/ODM or independent BIOS vendor for platform-specific instructions.
:::

Navigate to `Socket Configuration > Processor Configuration > TME, TME-MT, TDX` and configure:

* Set `Memory Encryption (TME)` to `Enable`
* Set `Total Memory Encryption Bypass` to `Enable` (optional setting for best host OS and regular VM performance)
* Set `Total Memory Encryption Multi-Tenant (TME-MT)` to `Enable`
* Set `TME-MT memory integrity` to `Disable`
* Set `Trust Domain Extension (TDX)` to `Enable`
* Set `TDX Secure Arbitration Mode Loader (SEAM Loader)` to `Enable` (allows loading Intel TDX Loader and Intel TDX Module from the ESP or BIOS)
* Set `TME-MT/TDX key split` to a non-zero value

Navigate to `Socket Configuration > Processor Configuration > Software Guard Extension (SGX)` and configure:

* Set `SW Guard Extensions (SGX)` to `Enable`

2. Save the BIOS settings and reboot.

3. Now, add the following kernel parameters to `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`, run `sudo update-grub`, and then reboot.

```
nohibernate kvm_intel.tdx=1
```

4. After rebooting, verify the parameters are applied.

```bash
cat /proc/cmdline 

BOOT_IMAGE=/boot/vmlinuz-6.19.0-3-generic root=UUID=f6ce4201-d6d1-4505-bdf5-019ee4fe842e ro nohibernate kvm_intel.tdx=1
```

5. Confirm Intel TDX is enabled successfully with the message `virt/tdx: module initialized`.

```bash
sudo dmesg | grep -i tdx

[    1.824045] virt/tdx: BIOS enabled: private KeyID range [32, 64)
[    1.824049] virt/tdx: Disable ACPI S3. Turn off Intel TDX in the BIOS to use ACPI S3.
[   24.195089] virt/tdx: 1050644 KB allocated for PAMT
[   24.195098] virt/tdx: module initialized
```

## 4. Install virtualization stack

1. Install the required virtualization components to run TDs.

```bash
sudo apt update
sudo apt install \
  qemu-system-x86 \
  ovmf-inteltdx \
  libvirt-daemon-system \
  libvirt-clients
```

This installs:

* `qemu-system-x86` - QEMU emulator for x86_64 with Intel TDX support
* `ovmf-inteltdx` - EDK II UEFI firmware with Intel TDX-capable OVMF builds
* `libvirt-daemon-system` - Libvirt daemon for managing VMs
* `libvirt-clients` - Command-line tools for libvirt (virsh, etc.)

2. After installation, verify the Intel TDX-capable OVMF firmware is available.

```bash
$ ls -l /usr/share/ovmf/OVMF.inteltdx.ms.fd
-rw-r--r-- 1 root root 4194304 Jan 15 12:00 /usr/share/ovmf/OVMF.inteltdx.ms.fd
```

## 5. Create guest image

Download an Ubuntu Server cloud image and generate a cloud-init ISO to set the root password.

1. Download the Ubuntu 24.04 LTS (for example) cloud image.
```bash
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
```

2. Install required tools.
```bash
sudo apt install cloud-image-utils
```

3. Create a cloud-init configuration file.
```bash
cat > user-data.yaml << 'EOF'
#cloud-config
chpasswd:
  list: |
    root:root
  expire: False
ssh_pwauth: True
disable_root: false
EOF
```

4. Create a cloud-init ISO.
```bash
cloud-localds user-data.img user-data.yaml
```

The user-data.img will be attached to the VM to apply the configuration.


:::{note}
For production use, set a strong password and configure SSH key-based authentication instead of password authentication.
:::

## 6. Launch TD guest using QEMU

1. Launch a TD using QEMU with the prepared image.

```bash
qemu-system-x86_64 \
  -accel kvm \
  -smp 32 \
  -m 16G \
  -cpu host \
  -object '{"qom-type":"tdx-guest","id":"tdx","quote-generation-socket":{"type": "vsock", "cid":"2","port":"4050"}}' \
  -object memory-backend-ram,id=mem0,size=16G \
  -machine q35,kernel_irqchip=split,confidential-guest-support=tdx,memory-backend=mem0 \
  -bios /usr/share/ovmf/OVMF.inteltdx.ms.fd \
  -nographic \
  -nodefaults \
  -vga none \
  -drive file=noble-server-cloudimg-amd64.img,if=none,id=virtio-disk0 \
  -device virtio-blk-pci,drive=virtio-disk0 \
  -drive file=user-data.img,if=none,id=cloud-init,format=raw \
  -device virtio-blk-pci,drive=cloud-init \
  -serial stdio
```

Key Intel TDX-specific parameters:

* `-object '{"qom-type":"tdx-guest","id":"tdx",...}'`: Creates the TDX guest object that enables confidential computing capabilities. The `quote-generation-socket` configures the vsock channel (CID 2, port 4050) for remote attestation quote generation.
* `-machine q35,kernel_irqchip=split,confidential-guest-support=tdx,memory-backend=mem0`: 
  - `kernel_irqchip=split`: Required for Intel TDX to properly isolate interrupt handling between host and guest
  - `confidential-guest-support=tdx`: Links the machine to the Intel TDX guest object
  - `memory-backend=mem0`: Associates the machine with the Intel TDX-protected memory backend
* `-object memory-backend-ram,id=mem0,size=16G`: Defines the memory backend that will be encrypted by Intel TDX
* `-bios /usr/share/ovmf/OVMF.inteltdx.ms.fd`: Specifies the Intel TDX-capable UEFI firmware with Microsoft Secure Boot keys
* `-cpu host`: Uses the host CPU model to expose Intel TDX capabilities to the guest

For more details about these parameters, refer to the [QEMU documentation](https://www.qemu.org/docs/master/system/i386/tdx.html).

## 7. Verify Intel TDX enablement in guest

Once the TD is launched, verify that Intel TDX is enabled by checking the kernel logs.

```bash
sudo dmesg | grep tdx

[    0.000000] tdx: Guest detected
[   11.162378] systemd[1]: Detected confidential virtualization tdx.
```

You can also check the Intel TDX guest device.

```bash
ls -l /dev/tdx_guest

crw------- 1 root root 10, 125 Jan  1 00:00 /dev/tdx_guest
```

## 8. Troubleshooting tips
1. Intel TDX is not enabled on the host.
   1. Ensure BIOS settings are correct and kernel parameters are enabled. 
   2. Confirm these MSR checks: 
      * Verify that MK-TME (Multi-Key Total Memory Encryption) is enabled by checking bit 1 of MSR 0x982: 
         ```bash
         sudo rdmsr 0x982 -f 1:1 1
         ``` 
         Expected value of `1` indicates MK-TME is enabled in BIOS.

      * Verify Intel TDX support by checking bit 11 of MSR 0x1401 (Enable bit for SEAMRR - SEAM Range Registers): 
         ```bash
         sudo rdmsr 0x1401 -f 11:11 1
         ```
         Expected value of `1` indicates SEAMRR is enabled.  

      * Verify the number of private keys allocated to TDs by checking bits 63:32 of IA32_TME_CAPABILITY MSR: <br> 
         ```bash
         echo $((0x$(sudo rdmsr 0x87 -f 63:32)))
         ```
         This shows the number of private keys available for Trust Domains (NUM_TDX_PRIV_KEYS) in decimal format. A non-zero value indicates keys are allocated for Intel TDX.  

      * Verify the number of private keys allocated to TDs by checking bits 63:32 of IA32_TME_CAPABILITY MSR: 
         ```bash
         echo $((0x$(sudo rdmsr 0x87 -f 63:32)))
         ```
         This shows the number of private keys available for Trust Domains (NUM_TDX_PRIV_KEYS) in decimal format. A non-zero value indicates keys are allocated for Intel TDX.

      * Verify the Intel SGX and MCHECK status.  
        ```bash
        sudo rdmsr 0xa0
        ```
        Expected value of `1` indicates it is enabled.
        A value of `1861` indicates SGX registration UEFI variables maybe corrupt. Boot into the BIOS and set `SGX Factory Reset` to `Enable`. This will result in two new keys. 

2. `sudo dmesg | grep -i tdx` shows `virt/tdx: module initialization failed (-5)`.
   1. You may have an old and unsupported Intel TDX Module.  Try updating to the latest Intel TDX Module. See [link](https://cc-enabling.trustedservices.intel.com/intel-tdx-enabling-guide/04/hardware_setup/#deploy-specific-intel-tdx-module-version) on ways to update your Intel TDX Module. <br> NOTE: If you chose to "Update Intel TDX Module via Binary Deployment", make sure you're using the correct Intel TDX Module version for your hardware. See the [Supported hardware](#supported-hardware) table.

3. I rebooted my TD, but it actually shuts down instead.
   1. Legacy (non-TDX) guests support reboot by resetting VCPU context. However, TD guests does not allow it for security reasons. You must power it down and boot it up again.
