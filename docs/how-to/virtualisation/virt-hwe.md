---
myst:
  html_meta:
    description: Installing the hardware enablement (HWE) virtualization stack.
---

(virt-hwe)=
# Virtualization Hardware Enablement Stack

Starting from [Ubuntu Resolute 26.04](https://releases.ubuntu.com/resolute/), we introduce the hardware enablement (HWE) stack for virtualization components:

- [**qemu-hwe**](https://launchpad.net/ubuntu/+source/qemu-hwe): Hypervisor and system emulation
- [**libvirt-hwe**](https://launchpad.net/ubuntu/+source/libvirt-hwe): Virtualization management library and tools
- [**edk2-hwe**](https://launchpad.net/ubuntu/+source/edk2-hwe): Firmware for UEFI support
- [**seabios-hwe**](https://launchpad.net/ubuntu/+source/seabios-hwe): BIOS firmware for compatibility

During the first 2 years of each Ubuntu LTS, this stack is upgraded every 6 months to have the latest upstream version supported in Ubuntu.

## Helper package

We provide the helper script **ubuntu_virt_helper** via the new package **ubuntu-helper-virt-hwe** as a management tool of the HWE stack

```bash
root@enticed-cichlid:~# apt install ubuntu-helper-virt-hwe
```

On a freshly installed system, running **ubuntu_virt_helper** gives the following output:

```bash
root@enticed-cichlid:~# ubuntu_virt_helper
Installed variant: none

1 packages:
  - ubuntu-helper-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe)
```

## Impact on current usage

The HWE stack is opt-in, so existing systems continue to work as-is. The base stack remains the default, and selecting HWE is an explicit action. For example, installing **qemu-system-x86** pulls in the base virtualization packages:

```bash
root@enticed-cichlid:~# apt install qemu-system-x86
```

These are the virtualization components installed as dependencies of **qemu-system-x86**:

```bash
root@enticed-cichlid:~# ubuntu_virt_helper --verbose
Installed variant: base


15 packages:
  - ovmf (2025.11-3ubuntu7, src:edk2, auto)
  - ovmf-amdsev (2025.11-3ubuntu7, src:edk2, auto)
  - ovmf-generic (2025.11-3ubuntu7, src:edk2, auto)
  - ovmf-inteltdx (2025.11-3ubuntu7, src:edk2, auto)
  - qemu-block-extra (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - qemu-system-common (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - qemu-system-data (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - qemu-system-gui (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - qemu-system-modules-opengl (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - qemu-system-modules-spice (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - qemu-system-x86 (1:10.2.1+ds-1ubuntu3, src:qemu, manual)
  - qemu-utils (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - seabios (1.17.0-1ubuntu1, src:seabios, auto)
  - ubuntu-helper-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, manual)
  - ubuntu-virt (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
```

The output indicates the **apt mark** for each package: ubuntu-helper-virt-hwe and qemu-system-x86 are marked as **manual** because they were directly installed, while the other packages are marked as **auto** as they were pulled in as dependencies.

## Uncontrolled variant switches and dependency management implications

Since the 2 stacks are mutually exclusive and one package can be individually requested for installation, one variant can be selected by installing any package from this variant:

```bash
root@enticed-cichlid:~# apt install qemu-utils-hwe
The following packages were automatically installed and are no longer required:
  adwaita-icon-theme              libflac14
  …
  x11-common
Use 'sudo apt autoremove' to remove them.


Installing:
  qemu-utils-hwe


Installing dependencies:
  qemu-block-extra-hwe  ubuntu-virt-hwe


REMOVING:
  ovmf          ovmf-inteltdx       qemu-system-data            qemu-system-modules-spice  seabios
  ovmf-amdsev   qemu-block-extra    qemu-system-gui             qemu-system-x86            ubuntu-virt
  ovmf-generic  qemu-system-common  qemu-system-modules-opengl  qemu-utils


Summary:
  Upgrading: 0, Installing: 3, Removing: 14, Not Upgrading: 9
  Download size: 2496 kB
  Freed space: 118 MB


Continue? [Y/n]
```

In this specific example, installing qemu-utils-hwe does not automatically install the HWE counterparts for several related packages, as they aren't part of qemu-utils-hwe’s dependencies. Consequently, APT issues a warning, noting that packages have been removed but have not been replaced with their respective HWE counterparts:

```bash
Get:1 http://archive.ubuntu.com/ubuntu resolute/main amd64 ubuntu-virt-hwe all 1:10.2.1+ds-1ubuntu4 [11.6 kB]
Get:2 http://archive.ubuntu.com/ubuntu resolute/main amd64 qemu-utils-hwe amd64 1:10.2.1+ds-1ubuntu4 [2389 kB]
Get:3 http://archive.ubuntu.com/ubuntu resolute/main amd64 qemu-block-extra-hwe amd64 1:10.2.1+ds-1ubuntu4 [95.4 kB]
Fetched 2496 kB in 1s (3358 kB/s)
Virt: switch of the ubuntu-virt[-hwe] stack is detected and there are orphaned removals (no counterpart being installed):
  - ovmf
  - ovmf-amdsev
  - ovmf-generic
  - ovmf-inteltdx
  - qemu-system-x86
  - qemu-system-modules-spice
  - qemu-system-common
  - qemu-system-data
  - qemu-system-gui
  - qemu-system-modules-opengl
  - seabios
Virt: Please install them back and use the ubuntu-virt-helper script to switch between ubuntu-virt[-hwe] packages.
(Reading database ... 96412 files and directories currently installed.)
Removing ovmf (2025.11-3ubuntu7) ...
Removing ovmf-amdsev (2025.11-3ubuntu7) ...
Removing ovmf-generic (2025.11-3ubuntu7) ...
```

The result can be an incomplete stack (in this case missing 11 packages when compared to before), as shown below:

```bash
root@enticed-cichlid:~# ubuntu_virt_helper --verbose
Installed variant: hwe


4 packages:
  - qemu-block-extra-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-utils-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, manual)
  - ubuntu-helper-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, manual)
  - ubuntu-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
```

## Proper variant switch using the helper script

Manual un-managed switch can break existing workflows that make use of the virtualization features. To avoid such partial exchanges, instead use the helper for a complete and safe switch. The example starts from the same conditions as above:

```bash
root@enticed-cichlid:~# ubuntu_virt_helper switch
Switching from base to hwe variant...
Installing:
  ovmf-amdsev-hwe   ovmf-inteltdx-hwe       qemu-system-data-hwe            qemu-system-modules-spice-hwe  seabios-hwe
  ovmf-generic-hwe  qemu-block-extra-hwe    qemu-system-gui-hwe             qemu-system-x86-hwe            ubuntu-virt-hwe
  ovmf-hwe          qemu-system-common-hwe  qemu-system-modules-opengl-hwe  qemu-utils-hwe


Suggested packages:
  samba  vde2  passt


REMOVING:
  ovmf         ovmf-generic   qemu-block-extra    qemu-system-data  qemu-system-modules-opengl  qemu-system-x86  seabios
  ovmf-amdsev  ovmf-inteltdx  qemu-system-common  qemu-system-gui   qemu-system-modules-spice   qemu-utils       ubuntu-virt


Summary:
  Upgrading: 0, Installing: 14, Removing: 14, Not Upgrading: 9
  Download size: 25.5 MB
  Freed space: 7168 B


Continue? [Y/n]
```

The helper performs a one-to-one replacement, preserving dependencies and preventing partial transitions. It also preserves each package's auto/manual install mark, making the switch transparent to users:

```bash
root@enticed-cichlid:~# ubuntu_virt_helper --verbose
Installed variant: hwe


15 packages:
  - ovmf-amdsev-hwe (2025.11-3ubuntu8, src:edk2-hwe, auto)
  - ovmf-generic-hwe (2025.11-3ubuntu8, src:edk2-hwe, auto)
  - ovmf-hwe (2025.11-3ubuntu8, src:edk2-hwe, auto)
  - ovmf-inteltdx-hwe (2025.11-3ubuntu8, src:edk2-hwe, auto)
  - qemu-block-extra-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-system-common-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-system-data-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-system-gui-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-system-modules-opengl-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-system-modules-spice-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-system-x86-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, manual)
  - qemu-utils-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - seabios-hwe (1.17.0-1ubuntu2, src:seabios-hwe, auto)
  - ubuntu-helper-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, manual)
  - ubuntu-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
```
