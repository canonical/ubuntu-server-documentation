(qemu)=
# QEMU

```{include} notices/qemu-user-group-notice.txt

```

## Virtualisation with QEMU

[QEMU](https://wiki.qemu.org/Main_Page) is a machine emulator that can run operating systems and programs for one machine on a different machine. However, it is more often used as a virtualizer in collaboration with [KVM](https://www.linux-kvm.org/page/Main_Page) kernel components. In that case it uses the hardware virtualization technology to virtualize guests.

Although QEMU has a [command line interface](https://qemu-project.gitlab.io/qemu/system/invocation.html) and a [monitor](https://qemu-project.gitlab.io/qemu/system/monitor.html) to interact with running guests, they are typically only used for development purposes. On the other hand, {ref}`libvirt <libvirt>` provides an abstraction from specific versions and hypervisors, and encapsulates some workarounds and best practices.

### Install QEMU/KVM

The first step to using QEMU/KVM on Ubuntu is to check if your system supports KVM.

```bash
kvm-ok
```

You should get an output saying `KVM acceleration can be used`.

The next step is to install QEMU.

```bash
sudo apt-get install qemu-system
```

### Boot a VM

The quickest way to get started with QEMU is by booting a VM directly from a netboot ISO. You can achieve this by running the following command:

```bash
qemu-system-x86_64 -enable-kvm -cdrom http://archive.ubuntu.com/ubuntu/dists/bionic-updates/main/installer-amd64/current/images/netboot/mini.iso
```

```{caution}
This example is just for illustration purposes - it is not generally recommended without verifying the checksums; {ref}`Multipass <create-vms-with-multipass>` and {ref}`UVTool <cloud-image-vms-with-uvtool>` are much better ways to get actual guests easily.
```

If you are testing this example on a headless system, specify an alternative display method such as {term}`VNC`.

### Create a virtual disk

The command in the previous sub-section boots the system entirely in RAM without persistent storage. To maintain the OS state across reboots, you should allocate space for the VM:

```bash
qemu-img create -f qcow2 disk.qcow 5G
```

And then we can use the disk space we have just allocated for storage by adding the argument: `-drive file=disk.qcow,format=qcow2`.

These tools can do much more, as you'll discover in their respective (long) [manual pages](https://manpages.ubuntu.com/). They can also be made more consumable for specific use-cases and needs through a vast selection of auxiliary tools - for example [virt-manager](https://virt-manager.org/) for UI-driven use through [libvirt](https://libvirt.org/). But in general, it comes down to:

```bash
qemu-system-x86_64 options image[s]
```

So take a look at the {manpage}`QEMU manpage <qemu-system(1)>`, {manpage}`qemu-img(1)` and the [QEMU documentation](https://www.qemu.org/documentation/) and see which options best suit your needs.

While a standard QEMU configuration works for most use cases, some scenarios demand high-vCPU VMs. In the next section, we’ll cover how to create QEMU virtual machines with up to 1024 vCPUs.

(create-qemu-vms-with-up-to-1024-vcpus)=
## Create QEMU VMs with up to 1024 vCPUs

For a long time, QEMU only supported launching virtual machines with 288 vCPUs or fewer. While this was acceptable a decade ago, nowadays it is more common to see processors with 300+ physical cores available. For this reason, QEMU has been modified to support virtual machines with up to 1024 vCPUs. The caveat is that the user has to provide a few specific (and not trivial to guess) command line options to enable such a feature, and that is the gap that this document aims to fill.

### Requirement

To support more than 288 vCPUs, some QEMU versions are only compatible with special machine types.

| QEMU version | Ubuntu release            | Supported machine types                                                                 |
| ------------ | ------------------------- | --------------------------------------------------------------------------------------- |
| QEMU 8.2.1+  | Ubuntu 24.04 LTS (Noble)  | `ubuntu` (Native support, also supports Jammy and Mantic machine types)                 |
| QEMU 8.0.4   | Ubuntu 23.10 (Mantic)     | `pc-q35-mantic-maxcpus`, `pc-i440fx-mantic-maxcpus` (Also supports Jammy machine types) |
| QEMU 6.2     | Ubuntu 22.04 LTS (Jammy)  | `pc-q35-jammy-maxcpus`, `pc-i440fx-jammy-maxcpus`                                       |

### Configuration by Ubuntu release

::::{tab-set}

:::{tab-item} 24.04 Noble
:sync: 24.04

From Noble onward, the regular `ubuntu` machine type supports up to 1024 vCPUs out of the box, which simplifies the command used to create such virtual machines:

```
qemu-system-x86_64 -M ubuntu,accel=kvm,kernel-irqchip=split -device intel-iommu,intremap=on -smp cpus=300,maxcpus=300 ...
```

Although the regular machine type can now be used to launch the virtual machine, it is still necessary to provide some special command line options to make sure that the VM is created with a virtual IOMMU with interrupt mapping.

Now that we've covered high-vCPU configurations for x86_64 VMs, let's look at how to boot ARM64 virtual machines on QEMU.
:::

:::{tab-item} 23.10 Mantic
:sync: 23.10

If you are using QEMU on Mantic, the special machine types are named in a similar fashion to Jammy's: `pc-q35-mantic-maxcpus` or `pc-i440fx-mantic-maxcpus`.
Therefore, you command line to create a virtual machine with support for more than 288 vCPUs on Mantic should start with:

```
qemu-system-x86_64 -M pc-q35-mantic-maxcpus,accel=kvm,kernel-irqchip=split -device intel-iommu,intremap=on -smp cpus=300,maxcpus=300 ...
```

In the example above, the virtual machine will be launched using 300 vCPUs and a `pc-q35-mantic-maxcpus` machine type. You can adjust the option according to your use case.

The `kernel-irqchip=split -device intel-iommu,intremap=on` command line options are required, to make sure that the VM is created with a virtual IOMMU with interrupt mapping. This is needed due to some idiosyncrasies present in this scenario.

Note that both machine types for Mantic are supported in subsequent versions of Ubuntu, so you should be able to migrate your virtual machines to newer versions of QEMU in Ubuntu without problems. As noted in the previous section, it is also possible to create virtual machines using the special Jammy machine types on Mantic.
:::

:::{tab-item} 22.04 Jammy
:sync: 22.04

If you are using QEMU on Jammy and want to create VMs with more than 288 vCPUs, you will need to use either of the special `pc-q35-jammy-maxcpus` or `pc-i440fx-jammy-maxcpus` machine types.

The command line needs to start with:

```
qemu-system-x86_64 -M pc-q35-jammy-maxcpus,accel=kvm,kernel-irqchip=split -device intel-iommu,intremap=on -smp cpus=300,maxcpus=300 ...
```

In the example above, the virtual machine will be launched using 300 vCPUs and a `pc-q35-jammy-maxcpus` machine type. You can adjust the option according to your use case.

The `kernel-irqchip=split -device intel-iommu,intremap=on` command line options are required, to make sure that the VM is created with a virtual IOMMU with interrupt mapping. This is needed due to some idiosyncrasies present in this scenario.

Note that both machine types for Jammy are supported in subsequent versions of Ubuntu, so you should be able to migrate your virtual machines to newer versions of QEMU in Ubuntu without problems.
:::

::::

(boot-arm64-virtual-machines-on-qemu)=
## Boot ARM64 virtual machines on QEMU

Ubuntu ARM64 images can run inside QEMU. You can either do this fully emulated (e.g. on an x86 host) or accelerated with KVM if you have an ARM64 host. This page describes how to do both.

```{note}
This requires Ubuntu 20.04 or greater
```

### Install QEMU to run ARM64 virtual machines

The first step is to install the `qemu-system-arm` package, which needs to be done regardless of where the ARM64 virtual machine will run:

```bash
sudo apt install qemu-system-arm
```

### Create necessary support files

Next, create a VM-specific flash volume for storing NVRAM variables, which are necessary when booting {term}`EFI` firmware:

```bash
truncate -s 64m varstore.img
```

We also need to copy the ARM UEFI firmware into a bigger file:

```bash
truncate -s 64m efi.img
dd if=/usr/share/qemu-efi-aarch64/QEMU_EFI.fd of=efi.img conv=notrunc
```

### Fetch the Ubuntu cloud image

You need to fetch the ARM64 variant of the Ubuntu cloud image you would like to use in the virtual machine. You can go to the official [Ubuntu cloud image](https://cloud-images.ubuntu.com/) website, select the Ubuntu release, and then download the variant whose filename ends in `-arm64.img`. For example, if you want to use the latest Jammy cloud image, you should download the file named `jammy-server-cloudimg-arm64.img`.

### Run QEMU natively on an ARM64 host

If you have access to an ARM64 host, you should be able to create and launch an ARM64 virtual machine there. Note that the command below assumes that you have already set up a network bridge to be used by the virtual machine.

```bash
qemu-system-aarch64 \
 -enable-kvm \
 -m 1024 \
 -cpu host \
 -M virt \
 -nographic \
 -drive if=pflash,format=raw,file=efi.img,readonly=on \
 -drive if=pflash,format=raw,file=varstore.img \
 -drive if=none,file=jammy-server-cloudimg-arm64.img,id=hd0 \
 -device virtio-blk-device,drive=hd0 -netdev type=tap,id=net0 \
 -device virtio-net-device,netdev=net0
```

### Run an emulated ARM64 VM on x86

You can also emulate an ARM64 virtual machine on an x86 host. To do that:

```bash
qemu-system-aarch64 \
 -m 2048\
 -cpu max \
 -M virt \
 -nographic \
 -drive if=pflash,format=raw,file=efi.img,readonly=on \
 -drive if=pflash,format=raw,file=varstore.img \
 -drive if=none,file=jammy-server-cloudimg-arm64.img,id=hd0 \
 -device virtio-blk-device,drive=hd0 \
 -netdev type=tap,id=net0 \
 -device virtio-net-device,netdev=net0
```

### Troubleshooting

#### No output and no response

If you get no output from the QEMU command above, aligning your host and guest release versions may help. For example, if you generated `efi.img` on Focal but want to emulate Jammy (with the Jammy cloud image), the firmware may not be fully compatible. Generating `efi.img` on Jammy when emulating Jammy with the Jammy cloud image may help.

## Further reading

QEMU can be extended in many different ways. If you'd like to take QEMU further, you might want to explore these additional resources:

- {ref}`Virtualizing graphics using QEMU/KVM <gpu-virtualization-with-qemu-kvm>`
- {ref}`Using QEMU to create a microvm <qemu-microvm>`.
