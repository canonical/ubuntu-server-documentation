# VM tools in the Ubuntu space

Let's take a look at some of the major tools and technologies available in the Ubuntu virtualization stack, in order of increasing abstraction. 

## KVM

**Abstraction layer**: Hardware virtualization

[Kernel-Based Virtual Machine (KVM)](https://www.linux-kvm.org/page/Main_Page) is a Linux kernel module that enables hardware-assisted virtualization. It is the default virtualization technology supported by Ubuntu.

For Intel and AMD hardware, KVM requires virtualization extensions in order to run. KVM is also available for IBM Z and LinuxONE, IBM POWER, and ARM64.

## QEMU

**Abstraction layer**: Emulation

[Quick Emulator (QEMU)](https://www.qemu.org/) is a versatile and powerful open source machine emulator. It emulates complete virtual machines, which allows users to run machines with different operating systems than the underlying host system -- without needing to purchase dedicated hardware. 

QEMU primarily functions as the user-space backend for KVM. When used in collaboration with KVM kernel components, it harnesses the hardware virtualization capability that KVM provides in order to efficiently virtualize guests.

It also has a [command line interface](https://qemu-project.gitlab.io/qemu/system/invocation.html) and [a monitor](https://qemu-project.gitlab.io/qemu/system/monitor.html) for interacting with running guests. However, these are typically only used for development purposes.

To find out how to get started with QEMU quickly, check out this guide on [how to set up QEMU](../how-to/virtualisation-with-qemu.md).

## libvirt

**Abstraction layer**: API and toolkit

[libvirt](https://libvirt.org/) provides an abstraction layer away from specific versions and hypervisors, giving users a command-line toolkit and API for managing virtualizations.

By providing an abstraction away from the underlying technologies (such as QEMU/KVM), libvirt makes it possible to manage all kinds of virtual resources -- across different platforms and hypervisors -- using one single, common interface. This can greatly simplify administration and automation tasks.

For details of how to get libvirt set up and the basics of how to use it, see this guide on [how to use libvirt](../how-to/libvirt.md). 

## Multipass and UVtool

**Abstraction layer**: User-friendly, CLI-based VM management

[Multipass](https://multipass.run/install) and [UVtool](https://launchpad.net/uvtool) provide an abstraction layer away from libvirt, using command-line interfaces to simplify VM management. Both Multipass and UVtool are widely used in development and testing; they are lightweight and straightforward to use, and can greatly simplify the process of creating and managing VMs. 

UVtool is essentially a wrapper around libvirt, providing an additional abstraction layer to simplify its use. Multipass is not based on libvirt, but can be integrated with it. This means that both tools can be used as part of a virtualization "stack" based around QEMU and libvirt.

If you want to get started with either of these tools, you can see our guides on [how to use Multipass](../how-to/how-to-create-a-vm-with-multipass.md) or [how to use UVtool](../how-to/create-cloud-image-vms-with-uvtool.md).

## virt-manager

**Abstraction layer**: GUI-based VM management

[Virt-manager](https://virt-manager.org/), the Virtual Machine Manager, provides another high-level way to manage VMs. Like UVtool, virt-manager uses libvirt on the backend. However, unlike UVtool, its abstraction is presented in the form of a graphical user interface (GUI).

Although in many ways this makes virt-manager easier to use than Multipass and UVtool, it also introduces more complex tooling that supports more advanced users. 

To get started with virt-manager, [this how-to guide](../how-to/virtual-machine-manager.md) showcases all the basic functionality and tooling.
