(virtualisation-with-qemu)=
# Virtualisation with QEMU

```{include} ../notices/qemu-user-group-notice.md```

[QEMU](http://wiki.qemu.org/Main_Page) is a machine emulator that can run operating systems and programs for one machine on a different machine. However, it is more often used as a virtualiser in collaboration with [KVM](https://www.linux-kvm.org/page/Main_Page) kernel components. In that case it uses the hardware virtualisation technology to virtualise guests.

Although QEMU has a [command line interface](https://qemu-project.gitlab.io/qemu/system/invocation.html ) and a [monitor](https://qemu-project.gitlab.io/qemu/system/monitor.html) to interact with running guests, they are typically only used for development purposes. [libvirt]( libvirt.md) provides an abstraction from specific versions and hypervisors and encapsulates some workarounds and best practices.

## Running QEMU/KVM

While there *are* more user-friendly and comfortable ways, the quickest way to get started with QEMU is by directly running it from the netboot ISO. You can achieve this by running the following command:

> **Warning**: 
> This example is just for illustration purposes - it is not generally recommended without verifying the checksums; [Multipass](https://discourse.ubuntu.com/t/virtualization-multipass/11983) and [UVTool](https://discourse.ubuntu.com/t/virtualization-uvt/11524) are much better ways to get actual guests easily.

```bash
qemu-system-x86_64 -enable-kvm -cdrom http://archive.ubuntu.com/ubuntu/dists/bionic-updates/main/installer-amd64/current/images/netboot/mini.iso
```

Downloading the ISO provides for faster access at runtime. We can now allocate the space for the VM:

```bash
qemu-img create -f qcow2 disk.qcow 5G
```

And then we can use the disk space we have just allocated for storage by adding the argument: `-drive file=disk.qcow,format=qcow2`.

These tools can do much more, as you'll discover in their respective (long) [manpages](https://manpages.ubuntu.com/). They can also be made more consumable for specific use-cases and needs through a vast selection of auxiliary tools - for example [virt-manager](https://virt-manager.org/) for UI-driven use through [libvirt](https://libvirt.org/). But in general, it comes down to:

```bash
qemu-system-x86_64 options image[s]
```

So take a look at the [QEMU manpage](http://manpages.ubuntu.com/manpages/bionic/man1/qemu-system.1.html), [`qemu-img`](http://manpages.ubuntu.com/manpages/bionic/man1/qemu-img.1.html) and the [QEMU documentation](https://www.qemu.org/documentation/) and see which options best suit your needs.

## Next steps

QEMU can be extended in many different ways. If you'd like to take QEMU further, you might want to check out this follow-up guide on [virtualizing graphics using QEMU/KVM](gpu-virtualization-with-qemu-kvm.md), or this guide on how you can [use QEMU to create MicroVMs](../explanation/using-qemu-for-microvms.md).
