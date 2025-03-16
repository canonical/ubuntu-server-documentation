(qemu)=
# QEMU

```{include} notices/qemu-user-group-notice.txt
```

## Virtualisation with QEMU

[QEMU](http://wiki.qemu.org/Main_Page) is a machine emulator that can run operating systems and programs for one machine on a different machine. However, it is more often used as a virtualiser in collaboration with [KVM](https://www.linux-kvm.org/page/Main_Page) kernel components. In that case it uses the hardware virtualisation technology to virtualise guests.

Although QEMU has a [command line interface](https://qemu-project.gitlab.io/qemu/system/invocation.html ) and a [monitor](https://qemu-project.gitlab.io/qemu/system/monitor.html) to interact with running guests, they are typically only used for development purposes. On the other hand, [libvirt]( libvirt.md) provides an abstraction from specific versions and hypervisors and encapsulates some workarounds and best practices.

### Running QEMU/KVM

The first step to using QEMU on Ubuntu is to install it.

```bash
sudo apt-get install qemu-system
```

While there *are* more user-friendly and comfortable ways, the quickest way to get started with QEMU is by booting a VM directly from a netboot ISO. You can achieve this by running the following command:

> **Warning**: 
> This example is just for illustration purposes - it is not generally recommended without verifying the checksums; {ref}`Multipass <create-vms-with-multipass>` and {ref}`UVTool <cloud-image-vms-with-uvtool>` are much better ways to get actual guests easily.

```bash
qemu-system-x86_64 -enable-kvm -cdrom http://archive.ubuntu.com/ubuntu/dists/bionic-updates/main/installer-amd64/current/images/netboot/mini.iso
```

> **Note**:
> If you are testing this example on a headless system, specify an alternative display method such as {term}`VNC`.

Though, downloading the ISO provides for faster access at runtime.

The command above boots the system entirely in RAM without persistent storage. To maintain the OS state across reboots, you should allocate space for the VM:

```bash
qemu-img create -f qcow2 disk.qcow 5G
```

And then we can use the disk space we have just allocated for storage by adding the argument: `-drive file=disk.qcow,format=qcow2`.

These tools can do much more, as you'll discover in their respective (long) [manpages](https://manpages.ubuntu.com/). They can also be made more consumable for specific use-cases and needs through a vast selection of auxiliary tools - for example [virt-manager](https://virt-manager.org/) for UI-driven use through [libvirt](https://libvirt.org/). But in general, it comes down to:

```bash
qemu-system-x86_64 options image[s]
```

So take a look at the [QEMU manpage](http://manpages.ubuntu.com/manpages/bionic/man1/qemu-system.1.html), [`qemu-img`](http://manpages.ubuntu.com/manpages/bionic/man1/qemu-img.1.html) and the [QEMU documentation](https://www.qemu.org/documentation/) and see which options best suit your needs.

Also, QEMU can be extended in many different ways. If you'd like to take QEMU further, you might want to explore {ref}`virtualizing graphics using QEMU/KVM <gpu-virtualization-with-qemu-kvm>`, {ref}`using QEMU to create MicroVMs <qemu-microvm>`, or creating QEMU VMs with up to 1024 vCPUs.

## Create QEMU VMs with up to 1024 vCPUs

For a long time, QEMU only supported launching virtual machines with 288 vCPUs or fewer. While this was acceptable a decade ago, nowadays it is more common to see processors with 300+ physical cores available. For this reason, QEMU has been modified to support virtual machines with up to 1024 vCPUs. The caveat is that the user has to provide a few specific (and not trivial to guess) command line options to enable such a feature, and that is the gap that this document aims to fill.

### Supported QEMU versions

Currently, support for VMs with more than 288 vCPUs is present in the following QEMU versions:

* QEMU 6.2 (Ubuntu 22.04 Jammy)**\***
* QEMU 8.0.4 (Ubuntu 23.10 Mantic)**\***
* QEMU 8.2.1+ (Ubuntu 24.04 Noble)

**\*** *A special QEMU machine type needs to be used in this case. See below.*

From Ubuntu 24.04 Noble onwards, there is native support for more than 288 vCPUs and using the regular `ubuntu` machine type should work out of the box.

#### Special QEMU machine types

To support more than 288 vCPUs, some QEMU versions are only compatible with special machine types.

- **Ubuntu 22.04 Jammy**

    If you are using QEMU on Jammy and want to create VMs with more than 288 vCPUs, you will need to use either of the special `pc-q35-jammy-maxcpus` or `pc-i440fx-jammy-maxcpus` machine types in combination with QEMU 6.2.

    The command line needs to start with:

    ```
    qemu-system-x86_64 -M pc-q35-jammy-maxcpus,accel=kvm,kernel-irqchip=split -device intel-iommu,intremap=on -smp cpus=300,maxcpus=300 ...
    ```

    In the example above, the virtual machine will be launched using 300 vCPUs and a `pc-q35-jammy-maxcpus` machine type. You can adjust the option according to your use case.

    The `kernel-irqchip=split -device intel-iommu,intremap=on` command line options are required, to make sure that the VM is created with a virtual IOMMU with interrupt mapping. This is needed due to some idiosyncrasies present in this scenario.

    Note that both machine types for Jammy are supported in subsequent versions of Ubuntu, so you should be able to migrate your virtual machines to newer versions of QEMU in Ubuntu without problems.

- **Ubuntu 23.10 Mantic**

    If you are using QEMU on Mantic, the special machine types are named in a similar fashion to Jammy's: `pc-q35-mantic-maxcpus` or `pc-i440fx-mantic-maxcpus`, and you must use it in combination with QEMU 8.0.4.
    Therefore, you command line to create a virtual machine with support for more than 288 vCPUs on Mantic should start with:

    ```
    qemu-system-x86_64 -M pc-q35-mantic-maxcpus,accel=kvm,kernel-irqchip=split -device intel-iommu,intremap=on -smp cpus=300,maxcpus=300 ...
    ```

    In the example above, the virtual machine will be launched using 300 vCPUs and a `pc-q35-mantic-maxcpus` machine type. You can adjust the option according to your use case.

    The `kernel-irqchip=split -device intel-iommu,intremap=on` command line options are required, to make sure that the VM is created with a virtual IOMMU with interrupt mapping. This is needed due to some idiosyncrasies present in this scenario.

    Note that both machine types for Mantic are supported in subsequent versions of Ubuntu, so you should be able to migrate your virtual machines to newer versions of QEMU in Ubuntu without problems. As noted in the previous section, it is also possible to create virtual machines using the special Jammy machine types on Mantic.

- **Ubuntu 24.04 Noble**

    From Noble onwards, the regular `ubuntu` machine type supports up to 1024 vCPUs out of the box for QEMU 8.2.1 and newer, this simplifies the command used to create such virtual machines:

    ```
    qemu-system-x86_64 -M ubuntu,accel=kvm,kernel-irqchip=split -device intel-iommu,intremap=on -smp cpus=300,maxcpus=300 ...
    ```

    Although the regular machine type can now be used to launch the virtual machine, it is still necessary to provide some special command line options to make sure that the VM is created with a virtual IOMMU with interrupt mapping.
