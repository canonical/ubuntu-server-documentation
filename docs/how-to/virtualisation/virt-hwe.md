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

We provide the helper script **ubuntu_virt_helper** via the new package **ubuntu-helper-virt-hwe** as a management tool of the HWE stack

```bash
root@virt:~# apt install ubuntu-helper-virt-hwe
```

On a freshly installed system, running **ubuntu_virt_helper** gives the following output:

```bash
root@virt:~# ubuntu_virt_helper
Installed variant: none

1 packages:
  - ubuntu-helper-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe)
```

The HWE stack is opt-in, so existing systems continue to work as-is. The base stack remains the default, and selecting HWE is an explicit action. For example, installing **virt-manager** pulls in the base virtualization packages:

```bash
root@virt:~# apt install virt-manager
```

These are the virtualization components installed as dependencies of **virt-manager**:

```bash
root@virt:~# ubuntu_virt_helper --verbose
Installed variant: base

8 packages:
  - libvirt-clients (12.0.0-1ubuntu5, src:libvirt, auto)
  - libvirt-common (12.0.0-1ubuntu5, src:libvirt, auto)
  - libvirt-l10n (12.0.0-1ubuntu5, src:libvirt, auto)
  - libvirt0:amd64 (12.0.0-1ubuntu5, src:libvirt, auto)
  - qemu-block-extra (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - qemu-utils (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
  - ubuntu-helper-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, manual)
  - ubuntu-virt (1:10.2.1+ds-1ubuntu3, src:qemu, auto)
```

Since the 2 stacks are mutually exclusive and one package can be individually requested for installation, one variant can be selected by installing any package from this variant:

<pre><code>
root@virt:~# apt install qemu-utils-hwe
The following package was automatically installed and is no longer required:
  libxml2-utils
Use 'apt autoremove' to remove it.

Installing:
  <span style="color: #28c635;">qemu-utils-hwe</span>

Installing dependencies:
  <span style="color: #28c635;">libvirt-common-hwe  libvirt-l10n-hwe  libvirt0-hwe  qemu-block-extra-hwe  ubuntu-virt-hwe</span>

REMOVING:
  <span style="color: #f30707;">libvirt-clients  libvirt-common  libvirt-l10n  libvirt0  qemu-block-extra  qemu-utils  ubuntu-virt</span>

Summary:
  Upgrading: 0, Installing: 6, Removing: 7, Not Upgrading: 130
  Download size: 8003 kB
  Space needed: 23.6 MB / 6638 MB available

Continue? [Y/n] 
</code></pre>

In this example, the installation of the **qemu-utils-hwe** misses installing the counterpart package of **libvirt-clients** since it is only a Recommends dependency. Here, APT warns that **libvirt-clients** is removed but not replaced with **libvirt-clients-hwe**:

<pre><code>Continue? [Y/n]
Get:1 http://archive.ubuntu.com/ubuntu resolute/main amd64 libvirt0-hwe amd64 12.0.0-1ubuntu5 [1676 kB]
Get:2 http://archive.ubuntu.com/ubuntu resolute/main amd64 ubuntu-virt-hwe all 1:10.2.1+ds-1ubuntu4 [11.6 kB]
Get:3 http://archive.ubuntu.com/ubuntu resolute/main amd64 libvirt-common-hwe amd64 12.0.0-1ubuntu5 [116 kB]
Get:4 http://archive.ubuntu.com/ubuntu resolute/main amd64 libvirt-l10n-hwe all 12.0.0-1ubuntu5 [3715 kB]
Get:5 http://archive.ubuntu.com/ubuntu resolute/main amd64 qemu-utils-hwe amd64 1:10.2.1+ds-1ubuntu4 [2389 kB]
Get:6 http://archive.ubuntu.com/ubuntu resolute/main amd64 qemu-block-extra-hwe amd64 1:10.2.1+ds-1ubuntu4 [95.4 kB]
Fetched 8003 kB in 5s (1488 kB/s)
<span style="color: #c62828;">Virt: switch of the ubuntu-virt[-hwe] stack is detected and there are orphaned removals (no counterpart being installed):</span>
<span style="color: #c62828;">  - libvirt-clients</span>
<span style="color: #c62828;">Virt: Please install them back and use the ubuntu_virt_helper script to switch between ubuntu-virt[-hwe] packages.</span>
(Reading database ... 97187 files and directories currently installed.)
Removing libvirt-clients (12.0.0-1ubuntu5) ...
Removing libvirt-l10n (12.0.0-1ubuntu5) ...
Removing qemu-block-extra (1:10.2.1+ds-1ubuntu3) ...</code></pre>

The result is an incomplete stack (missing **libvirt-clients-hwe**), as shown below:

```bash
root@virt:~# ubuntu_virt_helper --verbose
Installed variant: hwe

7 packages:
  - libvirt-common-hwe (12.0.0-1ubuntu5, src:libvirt-hwe, auto)
  - libvirt-l10n-hwe (12.0.0-1ubuntu5, src:libvirt-hwe, auto)
  - libvirt0-hwe:amd64 (12.0.0-1ubuntu5, src:libvirt-hwe, auto)
  - qemu-block-extra-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-utils-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, manual)
  - ubuntu-helper-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, manual)
  - ubuntu-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
```

This can break existing **virt-manager** workflows. To avoid partial transitions, use the helper for a complete and safe switch:

<pre><code>root@virt:~# ubuntu_virt_helper switch
Switching from base to hwe variant...
Installing:                     
  <span style="color: #28c635;">libvirt-clients-hwe  libvirt-common-hwe  libvirt-l10n-hwe  libvirt0-hwe  qemu-block-extra-hwe  qemu-utils-hwe  ubuntu-virt-hwe</span>

Suggested packages:
  libvirt-clients-qemu  libvirt-daemon  libvirt-login-shell

REMOVING:
  <span style="color: #c62828;">libvirt-clients  libvirt-common  libvirt-l10n  libvirt0  qemu-block-extra  qemu-utils  ubuntu-virt</span>

Summary:
  Upgrading: 0, Installing: 7, Removing: 7, Not Upgrading: 130
  Download size: 8431 kB
  Space needed: 24.8 MB / 6674 MB available

Continue? [Y/n] </code></pre>


The helper performs a one-to-one replacement, preserving dependencies and preventing partial transitions. It also preserves each package's auto/manual install mark, making the switch transparent to users:

<pre><code>root@virt:~# ubuntu_virt_helper --verbose
Installed variant: hwe

8 packages:
  - libvirt-clients-hwe (12.0.0-1ubuntu5, src:libvirt-hwe, auto)
  - libvirt-common-hwe (12.0.0-1ubuntu5, src:libvirt-hwe, auto)
  - libvirt-l10n-hwe (12.0.0-1ubuntu5, src:libvirt-hwe, auto)
  - libvirt0-hwe:amd64 (12.0.0-1ubuntu5, src:libvirt-hwe, auto)
  - qemu-block-extra-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - qemu-utils-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - ubuntu-helper-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
  - ubuntu-virt-hwe (1:10.2.1+ds-1ubuntu4, src:qemu-hwe, auto)
</code></pre>
