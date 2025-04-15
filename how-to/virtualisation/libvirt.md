(libvirt)=
# Libvirt

The [libvirt library](https://libvirt.org/) is used to interface with many different virtualisation technologies. Before getting started with libvirt it is best to make sure your hardware supports the necessary virtualisation extensions for [Kernel-based Virtual Machine (KVM)](https://www.linux-kvm.org/page/Main_Page). To check this, enter the following from a terminal prompt:

```bash
kvm-ok
```

A message will be printed informing you if your CPU *does* or *does not* support hardware virtualisation.

```{note}
On many computers with processors supporting hardware-assisted virtualisation, it is necessary to first activate an option in the BIOS to enable it.
```

## Virtual networking

There are a few different ways to allow a virtual machine access to the external network. The default virtual network configuration includes **bridging** and **iptables** rules implementing **usermode** networking, which uses the [SLiRP](https://en.wikipedia.org/wiki/Slirp) protocol. Traffic is NATed through the host interface to the outside network.

To enable external hosts to directly access services on virtual machines, a different type of *bridge* than the default needs to be configured. This allows the virtual interfaces to connect to the outside network through the physical interface, making them appear as normal hosts to the rest of the network.

There is a great example of [how to configure a bridge](https://netplan.readthedocs.io/en/latest/netplan-yaml/#properties-for-device-type-bridges) and combine it with libvirt so that guests will use it at the [netplan.io documentation](https://netplan.readthedocs.io/en/latest/).

## Install libvirt

To install the necessary packages, from a terminal prompt enter:

```bash
sudo apt update
sudo apt install qemu-kvm libvirt-daemon-system
```

After installing `libvirt-daemon-system`, the user that will be used to manage virtual machines needs to be added to the *libvirt* group. This is done automatically for members of the *sudo* group, but needs to be done in addition for anyone else that should access system-wide libvirt resources. Doing so will grant the user access to the advanced networking options.

In a terminal enter:

```bash
sudo adduser $USER libvirt
```

```{note}
If the chosen user is the current user, you will need to log out and back in for the new group membership to take effect.
```

You are now ready to install a *Guest* operating system. Installing a virtual machine follows the same process as installing the operating system directly on the hardware.

You will need **one** of the following:

- A way to automate the installation.
- A keyboard and monitor attached to the physical machine.
- To use cloud images which are meant to self-initialise (see {ref}`Multipass <create-vms-with-multipass>` and {ref}`UVTool <cloud-image-vms-with-uvtool>`).

In the case of virtual machines, a {term}`Graphical User Interface (GUI) <GUI>` is analogous to using a physical keyboard and mouse on a real computer. Instead of installing a GUI the `virt-viewer` or `virt-manager` application can be used to connect to a virtual machine's console using VNC. See {ref}`Virtual Machine Manager / Viewer <virtual-machine-manager>` for more information.

## Virtual machine management

The following section covers `virsh`, a virtual machine management tool that is a part of libvirt. But there are other tools available at different levels of complexities and feature-sets, like:

* {ref}`Multipass <create-vms-with-multipass>`
* {ref}`UVTool <cloud-image-vms-with-uvtool>`
* {ref}`virt-* tools <virtual-machine-manager>`
* [OpenStack](https://ubuntu.com/openstack)

## Manage VMs with `virsh`

There are several utilities available to manage virtual machines and libvirt. The `virsh` utility can be used from the command line. Some examples:

- To list running virtual machines:

  ```bash
  virsh list
  ```

- To start a virtual machine:

  ```bash
  virsh start <guestname>
  ```

- Similarly, to start a virtual machine at boot:

  ```bash
  virsh autostart <guestname>
  ```

- Reboot a virtual machine with:

  ```bash
  virsh reboot <guestname>
  ```

- The **state** of virtual machines can be saved to a file in order to be restored later. The following will save the virtual machine state into a file named according to the date:

  ```bash
  virsh save <guestname> save-my.state
  ```

  Once saved, the virtual machine will no longer be running.

- A saved virtual machine can be restored using:

  ```bash
  virsh restore save-my.state
  ```

- To shut down a virtual machine you can do:

  ```bash
  virsh shutdown <guestname>
  ```

- A CD-ROM device can be mounted in a virtual machine by entering:

  ```bash
  virsh attach-disk <guestname> /dev/cdrom /media/cdrom
  ```

- To change the definition of a guest, `virsh` exposes the domain via:

  ```bash
  virsh edit <guestname>
  ```

This will allow you to edit the [XML representation that defines the guest](https://libvirt.org/formatdomain.html). When saving, it will apply format and integrity checks on these definitions.

Editing the XML directly certainly is the most powerful way, but also the most complex one. Tools like {ref}`Virtual Machine Manager / Viewer <virtual-machine-manager>` can help inexperienced users to do most of the common tasks.

```{note}
If `virsh` (or other `vir*` tools) connect to something other than the default `qemu-kvm`/system hypervisor, one can find alternatives for the `--connect` option using `man virsh` or the [libvirt docs](http://libvirt.org/uri.html).
```

### `system` and `session` scope

You can pass connection strings to `virsh` - as well as to most other tools for managing virtualisation.

```bash
virsh --connect qemu:///system
```

There are two options for the connection.

* `qemu:///system` - connect locally as **root** to the daemon supervising QEMU and KVM domains
* `qemu:///session` - connect locally as a **normal user** to their own set of QEMU and KVM domains

The *default* was always (and still is) `qemu:///system` as that is the behavior most users are accustomed to. But there are a few benefits (and drawbacks) to `qemu:///session` to consider.

`qemu:///session` is per user and can -- on a multi-user system -- be used to separate the people.
Most importantly, processes run under the permissions of the user, which means no permission struggle on the just-downloaded image in your `$HOME` or the just-attached USB-stick.

On the other hand it can't access system resources very well, which includes network setup that is known to be hard with `qemu:///session`. It falls back to [SLiRP networking](https://en.wikipedia.org/wiki/Slirp) which is functional but slow, and makes it impossible to be reached from other systems.

`qemu:///system` is different in that it is run by the global system-wide libvirt that can arbitrate resources as needed. But you might need to `mv` and/or `chown` files to the right places and change permissions to make them usable.

Applications will usually decide on their primary use-case. Desktop-centric applications often choose `qemu:///session` while most solutions that involve an administrator anyway continue to default to `qemu:///system`.

> **Further reading**:
> There is more information about this topic in the [libvirt FAQ](https://wiki.libvirt.org/page/FAQ#What_is_the_difference_between_qemu:.2F.2F.2Fsystem_and_qemu:.2F.2F.2Fsession.3F_Which_one_should_I_use.3F) and this [blog post](https://blog.wikichoon.com/2016/01/qemusystem-vs-qemusession.html) about the topic.

## Migration

There are different types of migration available depending on the versions of libvirt and the hypervisor being used. In general those types are:

- [Offline migration](https://libvirt.org/migration.html#offline)

- [Live migration](https://libvirt.org/migration.html)

- [Postcopy migration](http://wiki.qemu.org/Features/PostCopyLiveMigration)

There are various options to those methods, but the entry point for all of them is `virsh migrate`. Read the integrated help for more detail.

```bash
 virsh migrate --help
```

Some useful documentation on the constraints and considerations of live migration can be found at the [Ubuntu Wiki](https://wiki.ubuntu.com/QemuKVMMigration).

## Device passthrough/hotplug

If you want to always pass through a device rather than using the hotplugging method described here, add the XML content of the device to your static guest XML representation via `virsh edit <guestname>`. In that case, you won't need to use *attach/detach*. There are different kinds of passthrough, and the types available to you depend on your hardware and software setup.

- USB {term}`hotplug`/passthrough

- VF hotplug/Passthrough

Both kinds are handled in a very similar way and while there are various way to do it (e.g. also via QEMU monitor), driving such a change via libvirt is recommended. That way, libvirt can try to manage all sorts of special cases for you and also somewhat masks version differences.

In general, when driving hotplug via libvirt, you create an XML snippet that describes the device just as you would do in a static [guest description](https://libvirt.org/formatdomain.html). A USB device is usually identified by vendor/product ID:

```xml
<hostdev mode='subsystem' type='usb' managed='yes'>
  <source>
    <vendor id='0x0b6d'/>
    <product id='0x3880'/>
  </source>
</hostdev>
```

Virtual functions are usually assigned via their PCI ID (domain, bus, slot, and function).

```xml
<hostdev mode='subsystem' type='pci' managed='yes'>
  <source>
    <address domain='0x0000' bus='0x04' slot='0x10' function='0x0'/>
  </source>
</hostdev>
```

```{note}
Getting the virtual function in the first place is very device-dependent and can, therefore, not be fully covered here. But in general, it involves setting up an {term}`IOMMU`, registering via [VFIO](https://www.kernel.org/doc/Documentation/vfio.txt) and sometimes requesting a number of VFs.
```

Here is an example of configuring a [ppc64el](https://wiki.debian.org/ppc64el) system to create four VFs on a device:

```bash
$ sudo modprobe vfio-pci
# identify device
$ lspci -n -s 0005:01:01.3
0005:01:01.3 0200: 10df:e228 (rev 10)
# register and request VFs
$ echo 10df e228 | sudo tee /sys/bus/pci/drivers/vfio-pci/new_id
$ echo 4 | sudo tee /sys/bus/pci/devices/0005\:01\:00.0/sriov_numvfs
```

You then attach or detach the device via libvirt by relating the guest with the XML snippet.

```bash
virsh attach-device <guestname> <device-xml>
# Use the Device in the Guest
virsh detach-device <guestname> <device-xml>
```

## Access QEMU Monitor via libvirt

The [QEMU Monitor](https://en.wikibooks.org/wiki/QEMU/Monitor) is the way to interact with QEMU/KVM while a guest is running. This interface has many powerful features for experienced users. When running under libvirt, the monitor interface is bound by libvirt itself for management purposes, but a user can still run QEMU monitor commands via libvirt. The general syntax is `virsh qemu-monitor-command [options] [guest] 'command'`.

Libvirt covers most use cases needed, but if you ever want/need to work around libvirt or want to tweak very special options you can e.g. add a device as follows:

```bash
virsh qemu-monitor-command --hmp focal-test-log 'drive_add 0 if=none,file=/var/lib/libvirt/images/test.img,format=raw,id=disk1'
```

The monitor is a power tool, especially for debugging purposes. For example, one can use the monitor to show the guest registers:

```bash
$ virsh qemu-monitor-command --hmp y-ipns 'info registers'

RAX=00ffffc000000000 RBX=ffff8f0f5d5c7e48 RCX=0000000000000000 RDX=ffffea00007571c0
RSI=0000000000000000 RDI=ffff8f0fdd5c7e48 RBP=ffff8f0f5d5c7e18 RSP=ffff8f0f5d5c7df8
[...]
```

## Huge pages

Let's start with a summary of the allocation and structuring of memory in an OS, and its relationship to transparent huge pages and {term}`huge pages <hugepage>`.

When you launch an application, the OS allocates virtual memory to it as a range of virtual addresses. The virtual memory is fake; it only allows the application to think it has more memory than what's physically available.

However, the CPU architecture will determine the amount of virtual memory allocated to the application; [64-bit CPUs](https://en.wikipedia.org/wiki/64-bit_computing) support 16 EB, whereas [32-bit CPUs](https://en.wikipedia.org/wiki/32-bit_computing) support 4 GB.
[x86_64](https://en.wikipedia.org/wiki/X86-64), however, typically supports only 256 TB of virtual memory.

The OS splits the virtual memory into pages (4 KB each). A page contains several virtual addresses ([1 byte each]((https://en.wikipedia.org/wiki/Memory_address))). These pages contain different parts of the application, like the code, data, stack, and heap. The OS maps these pages to real memory (RAM) because the virtual memory is a fake.

Although the OS allocates the virtual memory, the range of virtual addresses is generated by the CPU whenever the application accesses memory (e.g., reading a variable, fetching an instruction, or writing data). The [Memory Management Unit (MMU)](https://en.wikipedia.org/wiki/Memory_management_unit) receives these virtual addresses and uses the page table to convert them into physical addresses.

With a 4 KB page size in the table, a large application having 200 MB in size, for example, could have thousands of pages. So, constantly looking up the page table in RAM would be slow. To briefly fix this, the CPU uses a {term}`Translation Lookaside Buffer (TLB) <TLB>` to cache recent page table entries to speed up memory access; however, the TLB can only hold a certain number of entries.

To reduce this overhead, you can use huge pages, which increase the page size from 4 KB to larger sizes (e.g., 2 MB or 1 GB). This reduces the number of page table entries in the TLB, making lookups faster.

Huge pages must frequently be [pre-allocated](#huge-page-allocation) on the host for Libvirt to [map the VMs memory to the host](#huge-page-usage-in-libvirt). This is because VMs rely on two layers of address translation — one for the VM and one for the host - so expect memory lookups to be CPU-intensive.
Since huge pages can be configured on Libvirt, the page table entries are reduced, hence, memory access from the VM speeds up.

It's now clear how huge pages can lessen page table entries and TLB overhead.

Huge pages can have some disadvantages too, as they frequently require manual setup. To address this, [transparent huge pages](https://www.kernel.org/doc/html/next/admin-guide/mm/transhuge.html) are used to manage pages dynamically.

The dynamic page resizing can also be an issue when using libvirt since huge pages have to be pre-allocated. So, if it is clear that using huge pages is preferred, then making them explicit usually has some gains.

While huge pages are admittedly harder to manage (especially later in the system's lifetime if memory is fragmented), they provide a useful boost, especially for rather large guests.

> **Bonus**:
> When using device passthrough on very large guests, there is an extra benefit of using huge pages, as it is faster to do the initial memory clear on the VFIO {term}`DMA` pin.

### Huge page allocation

Huge pages come in different sizes. A *normal* page is usually 4k and huge pages are either 2M or 1G, but depending on the architecture, other options are possible.

The simplest yet least reliable way to allocate some huge pages is to just echo a value to `sysfs`:

```bash
echo 256 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
```

Be sure to re-check if it worked:

```bash
$ cat /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

256
```

There one of these sizes is the "default huge page size", which will be used in the auto-mounted `/dev/hugepages`. Changing the default size requires a reboot and is set via [default_hugepagesz](https://www.kernel.org/doc/html/v5.4/admin-guide/kernel-parameters.html).

You can check the current default size:

```bash
$ grep Hugepagesize /proc/meminfo

Hugepagesize:       2048 kB
```

But there can be more than one at the same time -- so it's a good idea to check:

```bash
$ tail /sys/kernel/mm/hugepages/hugepages-*/nr_hugepages`
==> /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages <==
0
==> /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages <==
2
```

And even that could -- on bigger systems -- be further split per [Numa node](https://www.kernel.org/doc/html/v5.4/vm/numa.html).

One can allocate huge pages at [boot or runtime](https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt), but due to fragmentation there are no guarantees it works later. The [kernel documentation](https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt) lists details on both ways.

Huge pages need to be allocated by the kernel as mentioned above, but to be consumable, they also have to be mounted. By default, `systemd` will make `/dev/hugepages` available for the default huge page size.

Feel free to add more mount points if you need different sized ones. An overview can be queried with [hugeadm](https://linux.die.net/man/8/hugeadm):

```bash
$ apt install libhugetlbfs-bin
$ hugeadm --list-all-mounts

Mount Point          Options
/dev/hugepages       rw,relatime,pagesize=2M
```

A one-stop info for the overall huge page status of the system can be reported with:

```bash
hugeadm --explain
```

### Huge page usage in libvirt

With the above in place, libvirt can map guest memory to huge pages. In a guest definition add the most simple form of:

```xml
<memoryBacking>
  <hugepages/>
</memoryBacking>
```

That will allocate the huge pages using the default huge page size from an autodetected mount point.
For more control, e.g. how memory is spread over [Numa nodes](https://www.kernel.org/doc/html/v5.4/vm/numa.html) or which page size to use, check out the details at the [libvirt docs](https://libvirt.org/formatdomain.html#elementsMemoryBacking).

## Controlling addressing bits

This is a topic that rarely matters on a single computer with virtual machines for generic use; libvirt will automatically use the hypervisor default, which in the case of QEMU is 40 bits. This default aims for compatibility since it will be the same on all systems, which simplifies migration between them and usually is compatible even with older hardware.

However, it can be very important when driving more advanced use cases. If one needs bigger guest sizes with more than a terabyte of memory then controlling the addressing bits is crucial.

### -hpb machine types

Since Ubuntu 18.04, the QEMU in Ubuntu has [provided special machine-types](https://bugs.launchpad.net/ubuntu/+source/qemu/+bug/1776189). These include machine types like `pc-q35-jammy` or `pc-i440fx-jammy`, but with a `-hpb` suffix. The “{term}`HPB`” abbreviation stands for “host-physical-bits”, which is the QEMU option that this represents.

For example, by using `pc-q35-jammy-hpb`, the guest would use the number of physical bits that the Host CPU has available.

Providing the configuration that a guest should use more address bits as a machine type has the benefit that many higher level management stacks like for example openstack, are already able to control it through libvirt.

One can check the bits available to a given CPU via the procfs:

```bash
$ cat /proc/cpuinfo | grep '^address sizes'
...
# an older server with a E5-2620
address sizes   : 46 bits physical, 48 bits virtual
# a laptop with an i7-8550U
address sizes   : 39 bits physical, 48 bits virtual
```

### maxphysaddr guest configuration

Since libvirt version 8.7.0 (>= Ubuntu 22.10 Lunar), `maxphysaddr` can be controlled via the [CPU model and topology section](https://libvirt.org/formatdomain.html#cpu-model-and-topology) of the guest configuration.
If one needs just a large guest, like before when using the `-hpb` types, all that is needed is the following libvirt guest xml configuration:

```xml
  <maxphysaddr mode='passthrough' />
```

Since libvirt 9.2.0 and 9.3.0 (>= Ubuntu 23.10 Mantic), an explicit number of emulated bits or a limit to the passthrough can be specified. Combined, this pairing can be very useful for computing clusters where the CPUs have different hardware physical addressing 
bits. Without these features, guests could be large, but potentially unable to migrate freely between all nodes since not all systems would support the same amount of addressing bits.

But now, one can either set a fixed value of addressing bits:

```xml
  <maxphysaddr mode='emulate' bits='42'/>
```

Or use the best available by a given hardware, without going over a certain limit to retain some compute node compatibility.

```xml
  <maxphysaddr mode='passthrough' limit='41/>
```

## AppArmor isolation

By default, libvirt will spawn QEMU guests using AppArmor isolation for enhanced security. The [AppArmor rules for a guest](https://gitlab.com/apparmor/apparmor/-/wikis/Libvirt#implementation-overview) will consist of multiple elements:

- A static part that all guests share => `/etc/apparmor.d/abstractions/libvirt-qemu`
- A dynamic part created at guest start time and modified on hotplug/unplug => `/etc/apparmor.d/libvirt/libvirt-f9533e35-6b63-45f5-96be-7cccc9696d5e.files`

Of the above, the former is provided and updated by the `libvirt-daemon` package, and the latter is generated on guest start. Neither of the two should be manually edited. They will, by default, cover the vast majority of use cases and work fine. But there are certain cases where users either want to:

- Further lock down the guest, e.g. by explicitly denying access that usually would be allowed.
- Open up the guest isolation. Most of the time this is needed if the setup on the local machine does not follow the commonly used paths.

To do so there are two files. Both are local overrides which allow you to modify them without getting them clobbered or command file prompts on package upgrades.

- `/etc/apparmor.d/local/abstractions/libvirt-qemu`
  This will be applied to every guest. Therefore it is a rather powerful (if blunt) tool. It is a quite useful place to add additional [deny rules](https://gitlab.com/apparmor/apparmor/-/wikis/FAQ#what-is-default-deny-white-listing).
- `/etc/apparmor.d/local/usr.lib.libvirt.virt-aa-helper`
  The above-mentioned *dynamic part* that is individual per guest is generated by a tool called `libvirt.virt-aa-helper`. That is under AppArmor isolation as well. This is most commonly used if you want to use uncommon paths as it allows one to have those uncommon paths in the [guest XML](https://libvirt.org/formatdomain.html) (see `virsh edit`) and have those paths rendered to the per-guest dynamic rules.

## Sharing files between Host<->Guest

To be able to exchange data, the memory of the guest has to be allocated as "shared". To do so you need to add the following to the guest config:

```xml
<memoryBacking>
  <access mode='shared'/>
</memoryBacking>
```

For performance reasons (it helps `virtiofs`, but also is generally wise to consider) it
is recommended to use huge pages which then would look like:

```xml
<memoryBacking>
  <hugepages>
    <page size='2048' unit='KiB'/>
  </hugepages>
  <access mode='shared'/>
</memoryBacking>
```

In the guest definition, one then can add `filesystem` sections to specify host paths to share with the guest. The *target dir* is a bit special as it isn't really a directory -- instead, it is a *tag* that in the guest can be used to access this particular `virtiofs` instance.

```xml
<filesystem type='mount' accessmode='passthrough'>
  <driver type='virtiofs'/>
  <source dir='/var/guests/h-virtiofs'/>
  <target dir='myfs'/>
</filesystem>
```

And in the guest, this can now be used based on the tag `myfs` like:

```bash
sudo mount -t virtiofs myfs /mnt/
```

Compared to other Host/Guest file sharing options -- commonly Samba, NFS, or 9P -- `virtiofs` is usually much faster and also more compatible with usual file system semantics.

See the [libvirt domain/filesystem](https://libvirt.org/formatdomain.html#filesystems) documentation for further details on these.

> **Note**:
> While `virtiofs` works with >=20.10 (Groovy), with >=21.04 (Hirsute) it became more comfortable, especially in small environments (no hard requirement to specify guest Numa topology, no hard requirement to use huge pages). If needed to set up on 20.10 or just interested in those details - the libvirt [knowledge-base about virtiofs](https://libvirt.org/kbase/virtiofs.html) holds more details about these.

## Resources

- See the [KVM home page](http://www.linux-kvm.org/) for more details.

- For more information on libvirt see the [libvirt home page](http://libvirt.org/).

  - XML configuration of [domains](https://libvirt.org/formatdomain.html) and [storage](https://libvirt.org/formatstorage.html) are the most often used libvirt reference.

- Another good resource is the [Ubuntu Wiki KVM](https://help.ubuntu.com/community/KVM) page.

- For basics on how to assign VT-d devices to QEMU/KVM, please see the [linux-kvm](http://www.linux-kvm.org/page/How_to_assign_devices_with_VT-d_in_KVM#Assigning_the_device) page.

- [Introduction to Memory Management in Linux](https://www.youtube.com/watch?v=7aONIVSXiJ8)
