---
myst:
  html_meta:
    description: Usage of libvirt to control Qemu/KVM guests; including more advanced tasks like migration, setting up huge pages and more.
---

(libvirt)=
# Libvirt

The [libvirt library](https://libvirt.org/) interfaces with many different virtualisation technologies. Before getting started with libvirt, verify that your hardware supports the necessary virtualisation extensions for [Kernel-based Virtual Machine (KVM)](https://www.linux-kvm.org/page/Main_Page). To check this, enter the following from a terminal prompt:

```{terminal}
:copy:
:user:
:host:
:dir:
kvm-ok
```

:::{note}
This command is part of the package `cpu-checker`, you might need to install it because it is not installed by default.
:::

This command prints a message informing you whether your CPU supports hardware virtualisation.

:::{note}
On many computers with processors supporting hardware-assisted virtualisation, you must activate an option in the {term}`BIOS` to enable it.
:::

## Virtual networking

Virtual machines can access the external network in several ways. The default virtual network configuration includes **bridging** and **`iptables`** rules implementing **usermode** networking, which uses the [SLiRP](https://en.wikipedia.org/wiki/Slirp) protocol. Traffic is Network Address Translation (NAT)-ed through the host interface to the outside network.

To enable external hosts to directly access services on virtual machines, configure a different type of *bridge* than the default. This allows the virtual interfaces to connect to the outside network through the physical interface, making them appear as normal hosts to the rest of the network.

There is a great example of [how to configure a bridge](https://netplan.readthedocs.io/en/latest/netplan-yaml/#properties-for-device-type-bridges) and combine it with libvirt so that guests will use it at the [netplan.io documentation](https://netplan.readthedocs.io/en/latest/).

## Install libvirt

To install the necessary packages, from a terminal prompt enter:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt update
```
```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install qemu-kvm libvirt-daemon-system
```

After installing `libvirt-daemon-system`, add the user who will manage virtual machines to the *libvirt* group. Members of the *sudo* group are added automatically, but you must manually add other users who need access to system-wide libvirt resources. This grants the user access to advanced networking options.

In a terminal enter:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo adduser $USER libvirt
```

:::{note}
If you add the current user, log out and back in for the new group membership to take effect.
:::

You are now ready to install a *Guest* operating system. Installing a virtual machine follows the same process as installing the operating system directly on the hardware.

Use **one** of the following:

- A way to automate the installation.
- A keyboard and monitor attached to the physical machine.
- To use cloud images which are meant to self-initialize (see {ref}`Multipass <create-vms-with-multipass>` and {ref}`UVTool <cloud-image-vms-with-uvtool>`).

In the case of virtual machines, a {term}`Graphical User Interface (GUI) <GUI>` is analogous to using a physical keyboard and mouse on a real computer. Instead of installing a GUI, use the `virt-viewer` or `virt-manager` application to connect to a virtual machine's console using VNC. See {ref}`Virtual Machine Manager / Viewer <virtual-machine-manager>` for more information.

## Virtual machine management

The following section covers `virsh`, a virtual machine management tool that is a part of libvirt. But there are other tools available at different levels of complexities and feature-sets, like:

* {ref}`Multipass <create-vms-with-multipass>`
* {ref}`UVTool <cloud-image-vms-with-uvtool>`
* {ref}`virt-* tools <virtual-machine-manager>`
* [OpenStack](https://ubuntu.com/openstack)

## Manage VMs with `virsh`

Several utilities are available to manage virtual machines and libvirt. `libvirt` comes with the command line utility `virsh`, which allows you to interact with the libvirt daemon to manage VMs. Some examples:

- To list running virtual machines:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh list
  ```

- To start a virtual machine:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh start <guestname>
  ```

- Similarly, to start a virtual machine at boot:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh autostart <guestname>
  ```

- Reboot a virtual machine with:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh reboot <guestname>
  ```

- Save the **state** of virtual machines to a file to restore later. The following command saves the virtual machine state into a file:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh save <guestname> save-my.state
  ```

  Once saved, the virtual machine stops running.

- Restore a saved virtual machine using:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh restore save-my.state
  ```

- To shut down a virtual machine you can do:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh shutdown <guestname>
  ```

- Mount a CD-ROM device in a virtual machine:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh attach-disk <guestname> /dev/cdrom /media/cdrom
  ```

- To change the definition of a guest, `virsh` exposes the domain via:

  ```{terminal}
  :copy:
  :user:
  :host:
  :dir:
  virsh edit <guestname>
  ```

This allows you to edit the [XML representation that defines the guest](https://libvirt.org/formatdomain.html). When saving, the system applies format and integrity checks on these definitions.

Editing the XML directly is the most powerful method, but also the most complex. Tools like {ref}`Virtual Machine Manager / Viewer <virtual-machine-manager>` can help inexperienced users perform most common tasks.

:::{note}
If `virsh` (or other `vir*` tools) connects to something other than the default `qemu-kvm`/system hypervisor, you can find alternatives for the `--connect` option using `man virsh` or the [libvirt docs](https://libvirt.org/uri.html).
:::

### `system` and `session` scope

`libvirt` has two execution contexts for VMs: system mode and session mode. For system mode, the `libvirtd` daemon runs as `root` and VMs run as `libvirt-qemu` user. For the session mode, both the `libvirtd` deamon and VM processes run as the session's user.

When working with virtuazation clients (`virsh`), you can specify the mode by using the appropriate URI:

```{terminal}
:copy:
:user:
:host:
:dir:
virsh --connect qemu:///session list
```

Or set it for the current shell with the `LIBVIRT_DEFAULT_URI` environment variable:

```{terminal}
:copy:
:user:
:host:
:dir:
export LIBVIRT_DEFAULT_URI=qemu:///session
```

On Ubuntu, by default, the system mode is used when no mode is specified by the user.

#### How each mode runs

In **system mode**, the root daemon sets up resources on the guest's behalf — disk images, networking, and a dynamic AppArmor profile — so that a guest can reach the host devices it needs (disks and I/O devices) even though the QEMU process itself runs as the unprivileged `libvirt-qemu` user. System guests are shared across all users on the host and can auto-start at boot, independently of any login session.

In **session mode**, both the daemon and the guests run as your unprivileged user, so a guest can only reach what your account can reach. Guest definitions and disk images live in your home directory (`~/.config/libvirt/` and `~/.local/share/libvirt/`) and are not visible to other users. Networking is restricted to user-mode ([SLiRP](https://en.wikipedia.org/wiki/Slirp)): you cannot easily attach guests to host bridges or manipulate system network interfaces without a setuid helper such as `qemu-bridge-helper`.

Because session mode is per user, libvirt runs a separate daemon for each user that connects:

```{terminal}
:output-only:
root       11351  0.0  4.3 752264 39292 ?        Ssl  15:15   0:00 /usr/sbin/libvirtd --timeout 120
ubuntu     13104  0.0  4.3 748272 39360 ?        Sl   23:01   0:00 /usr/sbin/libvirtd --timeout=120
debian     14364  2.4  4.1 747848 37660 ?        Sl   23:18   0:00 /usr/sbin/libvirtd --timeout=120
```

The session daemon is started on demand in one of two ways, and exits again after an idle period (the `--timeout` shown above):

- **systemd socket activation** — if the user socket unit is enabled (`systemctl --user enable --now virtqemud.socket`, or `libvirtd.socket` on the monolithic daemon), the per-user `systemd --user` instance listens on `$XDG_RUNTIME_DIR/libvirt/` and launches the daemon on the first connection.
- **Client auto-spawn** — if no socket is set up, the libvirt client library inside `virsh` starts the daemon itself as a child of your login session. This is why a session daemon can appear even when `systemctl --user list-sockets` shows no libvirt socket.

#### AppArmor differences

AppArmor is less strict — and often effectively absent — for session guests than for system guests.

In system mode, the daemon runs as `root`. Before launching a guest, it dynamically creates, loads, and registers a specialized AppArmor profile under `/etc/apparmor.d/libvirt/`. That profile restricts the QEMU process to only the disk images, ISOs, and sockets defined in the guest's XML.

In session mode, the daemon runs as your unprivileged user. Loading or compiling AppArmor profiles requires `root` (write access to `/etc/apparmor.d/` and kernel security capabilities), so a session daemon cannot generate these per-guest profiles. Isolation then relies entirely on standard Linux file permissions: the QEMU process runs with your user's privileges and can access any file your account owns.

We can see the list of active AppArmor profiles for system guests using `aa-status`:

```{terminal}
:input: aa-status
...
7 processes are in enforce mode.
  ...
   /usr/bin/qemu-system-x86_64 (13660) libvirt-03cf1350-1de5-4400-96e3-16dce6a9a921
   /usr/sbin/libvirtd (11351) libvirtd
```

The profile `libvirt-03cf1350-1de5-4400-96e3-16dce6a9a921` (`/etc/apparmor.d/libvirt/libvirt-03cf1350-1de5-4400-96e3-16dce6a9a921` on disk) corresponds to a system guest, whose UUID you can confirm with:

```{terminal}
:input: virsh domuuid tcg-minimal
03cf1350-1de5-4400-96e3-16dce6a9a921
```

The same guest run in session mode has no AppArmor profile generated.

#### When to use session mode ?

Applications will usually decide on their primary use-case. Desktop-centric applications often choose `qemu:///session` while most solutions that involve an administrator anyway continue to default to `qemu:///system`.

The two scopes differ in more than permissions. They use separate daemons, configuration directories, storage locations, and defaults, so a domain defined under one scope is not visible under the other:

| Aspect | `qemu:///system` | `qemu:///session` |
| --- | --- | --- |
| Runs as | `root` (via a system-wide daemon) | the invoking user |
| Guest process owner | the `libvirt-qemu` user by default | the invoking user |
| Configuration directory | `/etc/libvirt/` | `~/.config/libvirt/` |
| Default storage pool | `/var/lib/libvirt/images/` | `~/.local/share/libvirt/images/` |
| Default networking | NAT-ed `default` network (`virbr0`) | user-mode ([SLiRP](https://en.wikipedia.org/wiki/Slirp)) only |
| Bridged networking | managed by libvirt | requires the setuid `qemu-bridge-helper` |

Use qemu:///session if:

-  You are a desktop developer who wants to spin up test VMs without giving elevated/root permissions to libvirt.
- You want your VM disks and configurations completely confined to your user home directory.
- Basic outbound access over user-mode networking is enough and you do not need complex virtual networks.
- You do not need advanced I/O device capabilities such as device passthrough or SR-IOV.

:::{seealso}
There is more information about this topic in the [libvirt FAQ](https://wiki.libvirt.org/FAQ.html#what-is-the-difference-between-qemu-system-and-qemu-session-which-one-should-i-use) and this [blog post](https://blog.wikichoon.com/2016/01/qemusystem-vs-qemusession.html) about the topic.
:::

## Migration

Different types of migration are available depending on the versions of libvirt and the hypervisor being used. In general those types are:

- [Offline migration](https://libvirt.org/migration.html#offline-migration)

- [Live migration](https://libvirt.org/migration.html)

- [Postcopy migration](https://wiki.qemu.org/Features/PostCopyLiveMigration)

Various options exist for these methods, but the entry point for all of them is `virsh migrate`. Read the integrated help for more detail.

```{terminal}
:copy:
:user:
:host:
:dir:
virsh migrate --help
```

For further details on live migration, see {ref}`live-migration`.

## CPU model and topology

libvirt abstracts CPU configuration and provides several options to specify the VM CPU model in the domain definition:

- custom
- host-model
- host-passthrough
- maximum

While most of these modes are straightforward, the behavior of `host-model` is more subtle and the source of many common misunderstandings. There is no direct
translation of `host-model` into a single QEMU `-cpu` argument. Instead, libvirt selects a baseline CPU model and appends
a list of features:

```
# example snippet from qemu command line generated by libvirt
... -cpu Haswell-noTSX-IBRS,vmx=on,pdcm=off,...,vmx-entry-load-efer=on,vmx-eptp-switching=on ...
```

Because libvirt cannot include every known CPU model and variant, it chooses the model that shares the largest set of features with
the host's physical CPU and then lists the remaining features explicitly. In many cases, libvirt therefore cannot detect the
exact host CPU model. At first this may seem like a flaw, but in practice, knowing the exact model is not necessary.

For example, running `virsh capabilities` on a host with an Intel **Broadwell CPU** may produce the following output,
where libvirt uses **Haswell-noTSX-IBRS** as the baseline:

```xml
<capabilities>
  <host>
    <uuid>30303837-3831-584d-5135-323430354a38</uuid>
    <cpu>
      <arch>x86_64</arch>
      <model>Haswell-noTSX-IBRS</model>
      <vendor>Intel</vendor>
      <microcode version='73'/>
      <signature family='6' model='63' stepping='2'/>
      <counter name='tsc' frequency='2397195000' scaling='no'/>
      <topology sockets='1' dies='1' cores='6' threads='2'/>
      <maxphysaddr mode='emulate' bits='46'/>
      <feature name='vme'/>
      <feature name='ds'/>
      <feature name='acpi'/>
      <feature name='ss'/>
```

This mismatch between the baseline model reported by libvirt and the actual physical CPU model is not a bug and you can safely ignore it.

For more details, refer to the [upstream CPU model and features documentation](https://libvirt.org/formatcaps.html#host-cpu-model-and-features).

### Host CPU capabilities


## Device passthrough/hotplug

To pass through a device rather than using the hotplugging method described here, add the XML content of the device to your static guest XML representation via `virsh edit <guestname>`. In that case, you won't need to use *attach/detach*. Different kinds of passthrough exist, and the types available to you depend on your hardware and software setup.

- USB {term}`hotplug`/passthrough

- VF hotplug/Passthrough

Handle both kinds in a similar way. While there are various ways to do it (e.g., also via QEMU monitor), using libvirt is recommended. This way, libvirt can manage all sorts of special cases for you and also masks version differences.

In general, when driving hotplug via libvirt, you create an XML snippet that describes the device as you would in a static [guest description](https://libvirt.org/formatdomain.html). Identify a USB device by vendor/product ID:

```xml
<hostdev mode='subsystem' type='usb' managed='yes'>
  <source>
    <vendor id='0x0b6d'/>
    <product id='0x3880'/>
  </source>
</hostdev>
```

Assign virtual functions via their PCI ID (domain, bus, slot, and function).

```xml
<hostdev mode='subsystem' type='pci' managed='yes'>
  <source>
    <address domain='0x0000' bus='0x04' slot='0x10' function='0x0'/>
  </source>
</hostdev>
```

:::{note}
Getting the virtual function is device-dependent and cannot be fully covered here. In general, it involves setting up an {term}`IOMMU`, registering via [VFIO](https://www.kernel.org/doc/Documentation/vfio.txt), and sometimes requesting a number of VFs.
:::

Here is an example of configuring a [ppc64el](https://wiki.debian.org/ppc64el) system to create four VFs on a device:

```sh
$ sudo modprobe vfio-pci
# identify device
$ lspci -n -s 0005:01:01.3
0005:01:01.3 0200: 10df:e228 (rev 10)
# register and request VFs
$ echo 10df e228 | sudo tee /sys/bus/pci/drivers/vfio-pci/new_id
$ echo 4 | sudo tee /sys/bus/pci/devices/0005\:01\:00.0/sriov_numvfs
```

You then attach or detach the device via libvirt by relating the guest with the XML snippet.

```sh
virsh attach-device <guestname> <device-xml>
# Use the Device in the Guest
virsh detach-device <guestname> <device-xml>
```

## Access QEMU Monitor via libvirt

The [QEMU Monitor](https://en.wikibooks.org/wiki/QEMU/Monitor) is the way to interact with QEMU/KVM while a guest is running. This interface has many powerful features for experienced users. When running under libvirt, the monitor interface is bound by libvirt itself for management purposes, but you can still run QEMU monitor commands via libvirt. The general syntax is `virsh qemu-monitor-command [options] [guest] 'command'`.

Libvirt covers most needed use cases, but if you need to work around libvirt or tweak special options, you can, for example, add a device as follows:

```{terminal}
:copy:
:user:
:host:
:dir:
virsh qemu-monitor-command --hmp focal-test-log 'drive_add 0 if=none,file=/var/lib/libvirt/images/test.img,format=raw,id=disk1'
```

The monitor is a powerful tool, especially for debugging. For example, you can use the monitor to show the guest registers:

```{terminal}
:copy:
:user:
:host:
:dir:
virsh qemu-monitor-command --hmp y-ipns 'info registers'

RAX=00ffffc000000000 RBX=ffff8f0f5d5c7e48 RCX=0000000000000000 RDX=ffffea00007571c0
RSI=0000000000000000 RDI=ffff8f0fdd5c7e48 RBP=ffff8f0f5d5c7e18 RSP=ffff8f0f5d5c7df8
[...]
```

## Huge pages

Let's start with a summary of the allocation and structuring of memory in an OS, and its relationship to transparent huge pages and {term}`huge pages <hugepage>`.

When you launch an application, the OS allocates virtual memory to it as a range of virtual addresses. The virtual memory is not *truly* allocated on the physical memory; it allows the application to appear to have more memory than what's physically available.

However, the CPU architecture will determine the amount of virtual memory allocated to the application; [64-bit CPUs](https://en.wikipedia.org/wiki/64-bit_computing) support 16 EB, whereas [32-bit CPUs](https://en.wikipedia.org/wiki/32-bit_computing) support 4 GB.
[x86_64](https://en.wikipedia.org/wiki/X86-64), however, typically supports only 256 TB of virtual memory.

The OS splits the virtual memory into pages (4 KB each). A page contains several virtual addresses ([1 byte each](https://en.wikipedia.org/wiki/Memory_address)). These pages contain different parts of the application, like the code, data, stack, and heap. The OS maps these pages to real memory (RAM) because the virtual memory is not physical.

Although the OS allocates the virtual memory, the CPU generates the range of virtual addresses whenever the application accesses memory (e.g., reading a variable, fetching an instruction, or writing data). The [Memory Management Unit (MMU)](https://en.wikipedia.org/wiki/Memory_management_unit) receives these virtual addresses and uses the page table to convert them into physical addresses.

With a 4 KB page size in the table, a large application (200 MB, for example) could have thousands of pages. Constantly looking up the page table in RAM would be slow. To address this, the CPU uses a {term}`Translation Lookaside Buffer (TLB) <TLB>` to cache recent page table entries to speed up memory access. However, the TLB can hold a limited number of entries.

To reduce this overhead, you can use huge pages, which increase the page size from 4 KB to larger sizes (e.g., 2 MB or 1 GB). This reduces the number of page table entries in the TLB, making lookups faster.

Huge pages must typically be [pre-allocated](#huge-page-allocation) on the host for Libvirt to [map the VM's memory to the host](#huge-page-usage-in-libvirt). This is because VMs rely on two layers of address translation — one for the VM and one for the host — making memory lookups CPU-intensive.
Since you can configure huge pages on Libvirt, the page table entries are reduced, speeding up memory access from the VM.

It's now clear how huge pages can lessen page table entries and TLB overhead.

Huge pages can have some disadvantages too, as they frequently require manual setup. To address this, [transparent huge pages](https://www.kernel.org/doc/html/next/admin-guide/mm/transhuge.html) are used to manage pages dynamically.

Dynamic page resizing can be an issue when using libvirt since huge pages must be pre-allocated. If huge pages are preferred, making them explicit usually provides performance gains.

Huge pages are harder to manage (especially later in the system's lifetime if memory is fragmented), but they provide a useful boost, especially for large guests.

:::{tip}
When using device passthrough on very large guests, there is an extra benefit of using huge pages, as it is faster to do the initial memory clear on the VFIO {term}`DMA` pin.
:::

### Huge page allocation

Huge pages come in different sizes. A *normal* page is usually 4k and huge pages are either 2M or 1G, but depending on the architecture, other options are possible.

The simplest yet least reliable way to allocate some huge pages is to just echo a value to `sysfs`:

```{terminal}
:copy:
:user:
:host:
:dir:
echo 256 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
```

Be sure to re-check if it worked:

```{terminal}
:copy:
:user:
:host:
:dir:
cat /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

256
```

One of these sizes is the "default huge page size", which is used in the auto-mounted `/dev/hugepages`. Changing the default size requires a reboot and is set via [default_hugepagesz](https://www.kernel.org/doc/html/v5.4/admin-guide/kernel-parameters.html).

You can check the current default size:

```{terminal}
:copy:
:user:
:host:
:dir:
grep Hugepagesize /proc/meminfo

Hugepagesize:       2048 kB
```

However, more than one size can exist at the same time, so it's a good idea to check:

```{terminal}
:copy:
:user:
:host:
:dir:
tail /sys/kernel/mm/hugepages/hugepages-*/nr_hugepages`

==> /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages <==
0
==> /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages <==
2
```

On larger systems, this can be further split per [Numa node](https://www.kernel.org/doc/html/v5.4/vm/numa.html).

You can allocate huge pages at [boot or runtime](https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt), but due to fragmentation there is no guarantee that it works later. The [kernel documentation](https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt) lists details on both ways.

The kernel must allocate huge pages as mentioned above, but to be consumable, they must also be mounted. By default, `systemd` makes `/dev/hugepages` available for the default huge page size.

Add more mount points if you need different sized ones. Query an overview with [`hugeadm`](https://linux.die.net/man/8/hugeadm):

```{terminal}
:copy:
:user:
:host:
:dir:
apt install libhugetlbfs-bin
```
```{terminal}
:copy:
:user:
:host:
:dir:
hugeadm --list-all-mounts

Mount Point          Options
/dev/hugepages       rw,relatime,pagesize=2M
```

A one-stop info for the overall huge page status of the system can be reported with:

```{terminal}
:copy:
:user:
:host:
:dir:
hugeadm --explain
```

### Huge page usage in libvirt

With the above in place, libvirt can map guest memory to huge pages. In a guest definition add the most simple form of:

```xml
<memoryBacking>
  <hugepages/>
</memoryBacking>
```

This allocates the huge pages using the default huge page size from an auto-detected mount point.
For more control, e.g., how memory is spread over [Numa nodes](https://www.kernel.org/doc/html/v5.4/vm/numa.html) or which page size to use, see the [libvirt memory backing documentation](https://libvirt.org/formatdomain.html#memory-backing).

## Controlling addressing bits

This is a topic that rarely matters on a single computer with virtual machines for generic use; libvirt will automatically use the hypervisor default, which in the case of QEMU is 40 bits. This default aims for compatibility since it will be the same on all systems, which simplifies migration between them and usually is compatible even with older hardware.

However, it can be very important when driving more advanced use cases. If you need larger guest sizes with more than a terabyte of memory, then controlling the addressing bits is crucial.

### `-hpb` machine types

Since Ubuntu 18.04 LTS, the QEMU in Ubuntu has {lpbug}`provided special machine-types <1776189>`. These include machine types like `pc-q35-jammy` or `pc-i440fx-jammy`, but with a `-hpb` suffix. The "{term}`HPB`" abbreviation stands for "host-physical-bits", which is the QEMU option that this represents.

For example, by using `pc-q35-jammy-hpb`, the guest would use the number of physical bits that the Host CPU has available.

Providing the configuration that a guest should use more address bits as a machine type has the benefit that many higher-level management stacks (for example, OpenStack) can already control it through libvirt.

You can check the bits available to a given CPU via the `procfs`:

```{terminal}
:copy:
:user:
:host:
:dir:
cat /proc/cpuinfo | grep '^address sizes'

...
# an older server with a E5-2620
address sizes   : 46 bits physical, 48 bits virtual
# a laptop with an i7-8550U
address sizes   : 39 bits physical, 48 bits virtual
```

### maxphysaddr guest configuration

Since libvirt version 8.7.0 (>= Ubuntu 22.10 Lunar), you can control `maxphysaddr` via the [CPU model and topology section](https://libvirt.org/formatdomain.html#cpu-model-and-topology) of the guest configuration.
If you need a large guest (as with the `-hpb` types), use the following libvirt guest `xml` configuration:

```xml
  <maxphysaddr mode='passthrough' />
```

Since libvirt 9.2.0 and 9.3.0 (>= Ubuntu 23.10 Mantic), you can specify an explicit number of emulated bits or a limit to the passthrough. Combined, this pairing is useful for computing clusters where the CPUs have different hardware physical addressing 
bits. Without these features, guests could be large but potentially unable to migrate freely between all nodes since not all systems support the same number of addressing bits.

You can either set a fixed value of addressing bits:

```xml
  <maxphysaddr mode='emulate' bits='42'/>
```

Or, use the best available by a given hardware without exceeding a certain limit to retain some compute node compatibility.

```xml
  <maxphysaddr mode='passthrough' limit='41/>
```

## AppArmor isolation

By default, libvirt will spawn QEMU guests using AppArmor isolation for enhanced security. The [AppArmor rules for a guest](https://gitlab.com/apparmor/apparmor/-/wikis/Libvirt#implementation-overview) will consist of multiple elements:

- A static part that all guests share => `/etc/apparmor.d/abstractions/libvirt-qemu`
- A dynamic part created at guest start time and modified on hotplug/unplug => `/etc/apparmor.d/libvirt/libvirt-f9533e35-6b63-45f5-96be-7cccc9696d5e.files`

Of the above, the `libvirt-daemon` package provides and updates the former, and the system generates the latter on guest start. Do not manually edit either of these files. By default, they cover the vast majority of use cases and work fine. However, certain cases exist where users want to:

- Further lock down the guest, e.g. by explicitly denying access that usually would be allowed.
- Open up the guest isolation. Most of the time this is needed if the setup on the local machine does not follow the commonly used paths.

Two files are available for this purpose. Both are local overrides which allow you to modify them without getting them clobbered or seeing file prompts on package upgrades.

- `/etc/apparmor.d/local/abstractions/libvirt-qemu`
  This will be applied to every guest. Therefore, it is a powerful (if rather blunt) tool and a useful place to add additional [deny rules](https://gitlab.com/apparmor/apparmor/-/wikis/FAQ#what-is-default-deny-allow-listing).
- `/etc/apparmor.d/local/usr.lib.libvirt.virt-aa-helper`
  The above-mentioned *dynamic part* that is individual per guest is generated by a tool called `libvirt.virt-aa-helper`. That is under AppArmor isolation as well. This is most commonly used if you want to use uncommon paths as it allows one to have those uncommon paths in the [guest XML](https://libvirt.org/formatdomain.html) (see `virsh edit`) and have those paths rendered to the per-guest dynamic rules.

## Sharing files between Host<->Guest

To be able to exchange data, allocate the guest memory as "shared". To do so, add the following to the guest config:

```xml
<memoryBacking>
  <access mode='shared'/>
</memoryBacking>
```

For performance reasons (it helps `virtiofs`, but is generally wise to consider), using huge pages is recommended, which would look like:

```xml
<memoryBacking>
  <hugepages>
    <page size='2048' unit='KiB'/>
  </hugepages>
  <access mode='shared'/>
</memoryBacking>
```

In the guest definition, you can add `filesystem` sections to specify host paths to share with the guest. The *target dir* is special as it is not really a directory -- instead, it is a *tag* that the guest can use to access this particular `virtiofs` instance.

```xml
<filesystem type='mount' accessmode='passthrough'>
  <driver type='virtiofs'/>
  <source dir='/var/guests/h-virtiofs'/>
  <target dir='myfs'/>
</filesystem>
```

In the guest, you can now use this based on the tag `myfs`:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo mount -t virtiofs myfs /mnt/
```

Compared to other Host/Guest file sharing options -- commonly Samba, NFS, or 9P -- `virtiofs` is usually much faster and also more compatible with usual file system semantics.

See the [libvirt domain/filesystem documentation](https://libvirt.org/formatdomain.html#filesystems) for further details.

:::{note}
While `virtiofs` works with >=20.10 (Groovy), >=21.04 (Hirsute) made it more convenient, especially in small environments (no hard requirement to specify guest Numa topology or use huge pages). If you need to set up on 20.10 or want more details, the libvirt [knowledge-base about `virtiofs`](https://libvirt.org/kbase/virtiofs.html) provides additional information.
:::

## Resources

- See the [KVM home page](https://linux-kvm.org/page/Main_Page) for more details.

- For more information on libvirt see the [libvirt home page](https://libvirt.org/).

  - XML configuration of [domains](https://libvirt.org/formatdomain.html) and [storage](https://libvirt.org/formatstorage.html) are the most often used libvirt reference.

- Another good resource is the [Ubuntu Wiki KVM](https://help.ubuntu.com/community/KVM) page.

- For basics on how to assign VT-d devices to QEMU/KVM, please see the [linux-kvm](https://www.linux-kvm.org/page/How_to_assign_devices_with_VT-d_in_KVM#Assigning_the_device) page.

- [Introduction to Memory Management in Linux](https://www.youtube.com/watch?v=7aONIVSXiJ8)
