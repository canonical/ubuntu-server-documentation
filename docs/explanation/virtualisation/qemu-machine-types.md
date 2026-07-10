---
myst:
  html_meta:
    description: Understand QEMU machine types on Ubuntu, and how to upgrade the machine type of an existing guest.
---

(qemu-machine-types)=
# QEMU Machine types

The QEMU machine type defines the exact virtual hardware blueprint (chipset, bus architecture, and version-locked features) of a virtual machine. This allows QEMU to offer to virtual machines a well-defined and stable environment they can run not impacted by changes that happen under the hood like software upgrades or migrations to other systems.

However, when the QEMU software is upgraded, it might get new features and behavior that would be incompatible with the current definition virtual machine. But since the purpose of these types is to lock the feature set, they can't be changed - the solution is to version the machine types. The following is the list of Q35 machine types available in QEMU 10.2:

```text
...
pc-q35-8.0           Standard PC (Q35 + ICH9, 2009)
pc-q35-8.1           Standard PC (Q35 + ICH9, 2009)
pc-q35-8.2           Standard PC (Q35 + ICH9, 2009)
pc-q35-9.0           Standard PC (Q35 + ICH9, 2009)
pc-q35-9.1           Standard PC (Q35 + ICH9, 2009)
pc-q35-9.2           Standard PC (Q35 + ICH9, 2009)
pc-q35-10.0          Standard PC (Q35 + ICH9, 2009)
pc-q35-10.1          Standard PC (Q35 + ICH9, 2009)
pc-q35-10.2          Standard PC (Q35 + ICH9, 2009)
```

## Ubuntu specific machine types

For each release, Ubuntu-specific machine types are added and point to the corresponding upstream machine types (see [Launchpad bug](https://bugs.launchpad.net/ubuntu/+source/qemu/+bug/1294823)). On Ubuntu Resolute 26.04 LTS, for the x86 platforms, two new Ubuntu machine types are forked from the corresponding `i440fx` and `q35` upstream latest machine types:

```text
root@resolute:~# qemu-system-x86_64 -machine help | grep resolute
ubuntu               Ubuntu 26.04 PC (i440FX + PIIX, 1996) (alias of pc-i440fx-resolute)
pc-i440fx-resolute   Ubuntu 26.04 PC (i440FX + PIIX, 1996) (default)
ubuntu-q35           Ubuntu 26.04 PC (Q35 + ICH9, 2009) (alias of pc-q35-resolute)
pc-q35-resolute      Ubuntu 26.04 PC (Q35 + ICH9, 2009)
```

`pc-q35-resolute` and `pc-i440fx-resolute` are forked respectively from `pc-q35-10.2` and `pc-i440fx-10.2` that are the latest x86 upstream machine types since QEMU 10.2 is the version for Ubuntu Resolute LTS. `pc-i440fx-resolute` is defined as the default machine type for every virtual machine and the `ubuntu` alias now points to it.

These distro-specific machine types allow Ubuntu to support users who have deployed VMs on Ubuntu LTSes to be able to live migrate their VMs to the next LTS dealing with various changes we might introduce into an existing Ubuntu release through the SRU process. Whenever we need to make a change that modifies an existing machine type, we can make a "point-release" element in the Ubuntu names. This is not tied to a usual Ubuntu LTS point release, but to
anything introducing a delta to the machine type / `vmstate`. The format generally follows:

```text
$MACHINE_TYPE-$DISTRO-RELEASE[-v*]
```

This is an example of "point-release" machine types that have been added to address the [arch-capabilities bug](https://bugs.launchpad.net/bugs/2131822) in Noble:

```text
pc-i440fx-questing-v2 Ubuntu 25.10 PC v2 (i440FX + PIIX, + 10.1 machine, 1996)
pc-i440fx-noble-v2   Ubuntu 24.04 PC v2 (i440FX + PIIX, arch-caps fix, 1996)
pc-q35-noble-v2      Ubuntu 24.04 PC v2 (Q35 + ICH9, arch-caps fix, 2009)
```

## Machine type handling summary

Machine types are handled by:

- Adding a distribution-release-specific suffix to the default type(s)
  of each major architecture. Examples for Resolute:
  - x86: `pc-i440fx-resolute` and `pc-q35-resolute`
  - s390x: `s390-ccw-virtio-resolute`
  - ppc64el: `pseries-resolute`
  - arm64: `virt-resolute`
- Feature backports add a `-v%d` suffix to the affected types.
  - To avoid a proliferation of these types, such changes should be done carefully.
- The default, if no machine type is specified, always points to the latest
  distribution-specific machine type.
- We do not drop upstream types; they are provided as-is without further
  guarantees.
  - Cross-vendor/downstream migrations might work for upstream types, but are
    considered unsupported. This has always been the case, but package documentation
    might need updating to reflect this.
- Cleanup matches the usual supported distribution upgrade paths.
  - Drop former non-LTS release definitions after the next LTS.
  - Drop former LTS release definitions when out of support.

## Upgrading the machine type of your VM

Upgrading the machine type of a virtual machine (VM) can be thought of in the same way as buying (virtual) hardware of the same spec but with a newer release date. Whereas to upgrade a physical machine you might buy an improved CPU, more RAM, or increased storage, with a virtual machine you can change the configuration to achieve the same results.

### Why should you do this for a VM?

There are several reasons why you might want to update the machine type of an existing VM. For example, to:

- Improve performance with additional computing power
- Add a virtual {term}`GPU`
- Scale up the allocated resources to cope with increased workloads
- Obtain the latest security fixes and features
- Continue using a guest created on a now-unsupported release
- Prepare for future expansion by upgrading in advance

### How does this work?

It is generally recommended to update machine types when upgrading QEMU/KVM to a new major version. However, this can likely never be an automated task as the change is "guest visible"; the guest devices might change in appearance, new features will be announced to the guest, and so on.

Linux is usually very good at tolerating such changes -- but, it depends so heavily on the setup and workload of the guest that this has to be evaluated by the owner/admin of the system.

Other operating systems were known to often be severely impacted by changing the hardware. Consider a machine type change as similar to replacing all devices and firmware of a physical machine to the latest revision. **All** of the considerations that apply to firmware upgrades apply to evaluating a machine type upgrade as well.

### Backing up guest definitions

As usual, with major configuration changes it is wise to back up your guest definition and disk state to be able to do a rollback -- just in case something goes wrong.

### Upgrade the machine type

There is no integrated single command to update the machine type via `virsh` or similar tools. It is a normal part of your machine definition, and therefore updated the same way as most others.

#### Shut down the VM

First, shut down your machine and wait until it has reached that state:

```bash
virsh shutdown <your_machine>
```

You can check the status of the machine with the following command:

```{terminal}
:copy:
:user:
:host:
:dir:
virsh list --inactive
```

#### Edit the guest definition

Once the machine is listed as "shut off", you can then edit the machine definition and find the type in the `type` tag given at the machine attribute.

```bash
virsh edit <your_machine>
<type arch='x86_64' machine='pc-i440fx-bionic'>hvm</type>
```

Change this to the value you want. If you need to check what machine types are available via the `kvm -M ?` command first, then note that while upstream types are provided for convenience, only Ubuntu types are supported. There you can also see what the current default would be, as in this example:

```{terminal}
:copy:
:user:
:host:
:dir:
kvm -M ?

pc-i440fx-xenial       Ubuntu 16.04 PC (i440FX + PIIX, 1996) (default)
...
pc-i440fx-bionic       Ubuntu 18.04 PC (i440FX + PIIX, 1996) (default)
...
```

We strongly recommend that you change to newer types (if possible), not only to take advantage of newer features, but also to benefit from bug fixes that only apply to the newer device virtualisation.

#### Restart the guest

After this you can start your guest again. You can check the current machine type from guest and host depending on your needs.

```bash
virsh start <your_machine>
# check from host, via dumping the active xml definition
virsh dumpxml <your_machine> | xmllint --xpath "string(//domain/os/type/@machine)" -
# or from the guest via dmidecode (if supported)
sudo dmidecode | grep Product -A 1
        Product Name: Standard PC (i440FX + PIIX, 1996)
        Version: pc-i440fx-bionic
```

If you keep non-live definitions around -- such as `.xml` files -- remember to update those as well.
