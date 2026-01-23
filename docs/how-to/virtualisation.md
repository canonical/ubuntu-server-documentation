---
myst:
  html_meta:
    description: Create and manage virtual machines on Ubuntu Server using Multipass, UVtool, QEMU, libvirt, and virt-manager with these comprehensive guides.
---

(how-to-virtualisation)=
# Virtualisation

In this section we show how to install, configure and use various options for creating virtual machines (VMs). For more information about these options, you may want to refer to our {ref}`Introduction to virtualization <introduction-to-virtualization>`
  
## Virtual machines and containers

```{toctree}
:hidden:

LXD <virtualisation/lxd-containers>
Multipass <virtualisation/multipass>
UVtool <virtualisation/cloud-image-vms-with-uvtool>
QEMU <virtualisation/qemu>
AMD SEV <virtualisation/sev-snp>
```

* {ref}`LXD containers and virtual machines <lxd-containers>`
* {ref}`Create VMs with Multipass <create-vms-with-multipass>`
* {ref}`Create cloud image VMs with UVtool <cloud-image-vms-with-uvtool>`
* {ref}`QEMU <qemu>`
* {ref}`Confidential Computing with AMD <sev-snp>`

## VM tooling

```{toctree}
:hidden:

Libvirt and virsh <virtualisation/libvirt>
virt-manager <virtualisation/virtual-machine-manager>
Nested virtualization <virtualisation/enable-nested-virtualisation>
```

* {ref}`How to use the libvirt library with virsh <libvirt>`
* {ref}`How to use virt-manager and other virt* tools <virtual-machine-manager>`
* {ref}`How to enable nested virtualisation <enable-nested-virtualisation>`

## Ubuntu in other virtual environments

```{toctree}
:hidden:

Ubuntu on Hyper-V <virtualisation/ubuntu-on-hyper-v>
```

* {ref}`Setting up Ubuntu on Hyper-V <ubuntu-on-hyper-v>` (Windows 11)

## See also

* Explanation: {ref}`explanation-virtualisation`
