(about-dpdk)=
# About DPDK


The Data Plane Development Kit (DPDK) is a set of libraries and drivers for fast packet processing, which runs mostly in Linux userland. This set of libraries provides the so-called "Environment Abstraction Layer" (EAL). The EAL hides the details of the environment and provides a standard programming interface. Common use cases are around special solutions, such as network function virtualisation and advanced high-throughput network switching. 

The DPDK uses a run-to-completion model for fast data plane performance and accesses devices via polling to eliminate the latency of interrupt processing, albeit with the tradeoff of higher CPU consumption. It was designed to run on any processor. The first supported CPU was Intel x86 and it is now extended to IBM PPC64 and ARM64.

Ubuntu provides some additional infrastructure to increase DPDK's usability.

## Prerequisites

This package is currently compiled for the lowest possible CPU requirements allowed by upstream. Starting with [DPDK 17.08](https://git.dpdk.org/dpdk/commit/?id=f27769f796a0639368117ce22fb124b6030dbf73), that means it requires at least SSE4_2 and for anything else activated by -march=corei7 (in GCC) to be supported by the CPU.

The list of upstream DPDK-supported network cards can be found at [supported NICs](http://dpdk.org/doc/nics). However, a lot of those are disabled by default in the upstream project as they are not yet in a stable state. The subset of network cards that DPDK has enabled in the package (as available in Ubuntu 16.04) is:

DPDK has "userspace" drivers for the cards called PMDs.
The packages for these follow the pattern of `librte-pmd-<type>-<version>`. Therefore the example for an Intel e1000 in 18.11 would be `librte-pmd-e1000-18.11`.

The more commonly used, tested and fully supported drivers are installed as dependencies of `dpdk`. But there are [many more "in-universe"](https://help.ubuntu.com/community/Repositories/Ubuntu#The_Four_Main_Repositories) that follow the same naming pattern.

## <h2 id="heading--unassign-default-kernel-drivers">Unassign the default kernel drivers </a>

Cards must be unassigned from their kernel driver and instead be assigned to `uio_pci_generic` of `vfio-pci`. `uio_pci_generic` is older and it's (usually) easier to get it to work. However, it also has fewer features and less isolation.

The newer VFIO-PCI requires that you activate the following kernel parameters to enable the input-output memory management unit (IOMMU):

``` 
iommu=pt intel_iommu=on          
```

Alternatively, on AMD:

``` 
amd_iommu=pt
```

On top of VFIO-PCI, you must also configure and assign the IOMMU groups accordingly. This is mostly done in firmware and by hardware layout -- you can check the group assignment the kernel probed in `/sys/kernel/iommu_groups/`.

> **Note**: 
> VirtIO is special. DPDK can directly work on these devices without `vfio_pci`/`uio_pci_generic`. However, to avoid issues that might arise from the kernel and DPDK managing the device, you still need to unassign the kernel driver.

Manual configuration and status checks can be done via `sysfs`, or with the tool `dpdk_nic_bind`:

```
dpdk_nic_bind.py --help
```

## Usage

```
dpdk-devbind.py [options] DEVICE1 DEVICE2 ....

where DEVICE1, DEVICE2 etc, are specified via PCI "domain:bus:slot.func" syntax
or "bus:slot.func" syntax. For devices bound to Linux kernel drivers, they may
also be referred to by Linux interface name e.g. eth0, eth1, em0, em1, etc.

Options:
--help, --usage:
    Display usage information and quit

-s, --status:
    Print the current status of all known network, crypto, event
    and mempool devices.
    For each device, it displays the PCI domain, bus, slot and function,
    along with a text description of the device. Depending upon whether the
    device is being used by a kernel driver, the igb_uio driver, or no
    driver, other relevant information will be displayed:
    * the Linux interface name e.g. if=eth0
    * the driver being used e.g. drv=igb_uio
    * any suitable drivers not currently using that device
        e.g. unused=igb_uio
    NOTE: if this flag is passed along with a bind/unbind option, the
    status display will always occur after the other operations have taken
    place.

--status-dev:
    Print the status of given device group. Supported device groups are:
    "net", "crypto", "event", "mempool" and "compress"

-b driver, --bind=driver:
    Select the driver to use or "none" to unbind the device

-u, --unbind:
    Unbind a device (Equivalent to "-b none")

--force:
    By default, network devices which are used by Linux - as indicated by
    having routes in the routing table - cannot be modified. Using the
    --force flag overrides this behavior, allowing active links to be
    forcibly unbound.
    WARNING: This can lead to loss of network connection and should be used
    with caution.

Examples:
---------

To display current device status:
    dpdk-devbind.py --status

To display current network device status:
    dpdk-devbind.py --status-dev net

To bind eth1 from the current driver and move to use igb_uio
    dpdk-devbind.py --bind=igb_uio eth1

To unbind 0000:01:00.0 from using any driver
    dpdk-devbind.py -u 0000:01:00.0

To bind 0000:02:00.0 and 0000:02:00.1 to the ixgbe kernel driver
    dpdk-devbind.py -b ixgbe 02:00.0 02:00.1
```

## DPDK device configuration

<a name="unassigndrivers"></a>

The package `dpdk` provides *init* scripts that ease configuration of device assignment and huge pages. It also makes them persistent across reboots.

The following is an example of the file `/etc/dpdk/interfaces` configuring two ports of a network card: one with `uio_pci_generic` and the other with `vfio-pci`.

``` 
# <bus>         Currently only "pci" is supported
# <id>          Device ID on the specified bus
# <driver>      Driver to bind against (vfio-pci or uio_pci_generic)
#
# Be aware that the two DPDK compatible drivers uio_pci_generic and vfio-pci are
# part of linux-image-extra-<VERSION> package.
# This package is not always installed by default - for example in cloud-images.
# So please install it in case you run into missing module issues.
#
# <bus> <id>     <driver>
pci 0000:04:00.0 uio_pci_generic
pci 0000:04:00.1 vfio-pci     
```

Cards are identified by their PCI-ID. If you are need to check, you can use the tool `dpdk_nic_bind.py` to show the currently available devices -- and the drivers they are assigned to. For example, running the command `dpdk_nic_bind.py --status` provides the following details:

``` 
Network devices using DPDK-compatible driver
============================================
0000:04:00.0 'Ethernet Controller 10-Gigabit X540-AT2' drv=uio_pci_generic unused=ixgbe

Network devices using kernel driver
===================================
0000:02:00.0 'NetXtreme BCM5719 Gigabit Ethernet PCIe' if=eth0 drv=tg3 unused=uio_pci_generic *Active*
0000:02:00.1 'NetXtreme BCM5719 Gigabit Ethernet PCIe' if=eth1 drv=tg3 unused=uio_pci_generic
0000:02:00.2 'NetXtreme BCM5719 Gigabit Ethernet PCIe' if=eth2 drv=tg3 unused=uio_pci_generic
0000:02:00.3 'NetXtreme BCM5719 Gigabit Ethernet PCIe' if=eth3 drv=tg3 unused=uio_pci_generic
0000:04:00.1 'Ethernet Controller 10-Gigabit X540-AT2' if=eth5 drv=ixgbe unused=uio_pci_generic

Other network devices
=====================
<none>
```

## DPDK hugepage configuration

DPDK makes heavy use of hugepages to eliminate pressure on the translation lookaside buffer (TLB). Therefore, hugepages need to be configured in your system. The `dpdk` package has a config file and scripts that try to ease hugepage configuration for DPDK in the form of `/etc/dpdk/dpdk.conf`.

If you have more consumers of hugepages than just DPDK in your system -- or very special requirements for how your hugepages will be set up -- you likely want to allocate/control them yourself. If not, this can be a great simplification to get DPDK configured for your needs.

As an example, we can specify a configuration of 1024 hugepages of 2M each and four 1G pages in `/etc/dpdk/dpdk.conf` by adding:

``` 
NR_2M_PAGES=1024
NR_1G_PAGES=4
```

This supports configuring 2M and the larger 1G hugepages (or a mix of both). It will make sure there are proper `hugetlbfs` mountpoints for DPDK to find both sizes -- no matter what size your default hugepage is. The config file itself holds more details on certain corner cases and a few hints if you want to allocate hugepages manually via a kernel parameter.

The size you want depends on your needs: 1G pages are certainly more effective regarding TLB pressure, but there have been reports of them fragmenting inside the DPDK memory allocations. Also, it can be harder to find enough free space to set up a certain number of 1G pages later in the life-cycle of a system.

## Compile DPDK applications

Currently, there are not many consumers of the DPDK library that are stable and released. Open vSwitch DPDK is an exception to that (see below) and more are appearing, but in general it may be that you will want to compile an app against the library.

You will often find guides that tell you to fetch the DPDK sources, build them to your needs and eventually build your application based on DPDK by setting values `RTE_*` for the build system. Since Ubuntu provides an already-compiled DPDK for you can can skip all that.

DPDK provides a [valid pkg-config file](https://people.freedesktop.org/~dbn/pkg-config-guide.html) to simplify setting the proper variables and options:

``` 
sudo apt-get install dpdk-dev libdpdk-dev
gcc testdpdkprog.c $(pkg-config --libs --cflags libdpdk) -o testdpdkprog
```

An example of a complex (auto-configure) user of pkg-config of DPDK including fallbacks to older non pkg-config style can be seen in the [Open vSwitch build system](https://github.com/openvswitch/ovs/blob/master/acinclude.m4#L283).

Depending on what you are building, it may be a good idea to install all DPDK build dependencies before the make. On Ubuntu, this can be done automatically with the following command:

``` 
sudo apt-get install build-dep dpdk
```

## DPDK in KVM guests

Even if you have no access to DPDK-supported network cards, you can still work with DPDK by using its support for VirtIO. To do so, you must create guests backed by hugepages (see above). In addition, you will also need to have *at least* Streaming SIMD Extensions 3 (SSE3).

The default CPU model used by QEMU/libvirt is only up to SSE2. So, you will need to define a model that passes the proper feature flags (or use `host-passthrough`). As an example, you can add the following snippet to your virsh XML (or the equivalent virsh interface you use).

``` 
<cpu mode='host-passthrough'>
```

Nowadays, VirtIO supports multi-queue, which DPDK in turn can exploit for increased speed. To modify a normal VirtIO definition to have multiple queues, add the following snippet to your interface definition. 

``` 
<driver name="vhost" queues="4"/>
```

This will enhance a normal VirtIO NIC to have multiple queues, which can later be consumed by e.g., DPDK in the guest.

## Use DPDK

Since DPDK itself is only a (massive) library, you most likely will continue to {ref}`Open vSwitch DPDK <dpdk-with-open-vswitch>` as an example to put it to use.

## Resources

  - [DPDK documentation](http://dpdk.org/doc)

  - [Release Notes matching the version packages in Ubuntu 16.04](http://dpdk.org/doc/guides/rel_notes/release_2_2.html)

  - [Linux DPDK user getting started](http://dpdk.org/doc/guides/linux_gsg/index.html)

  - [EAL command-line options](http://dpdk.org/doc/guides/testpmd_app_ug/run_app.html)

  - [DPDK API documentation](http://dpdk.org/doc/api/)

  - [Open vSwitch DPDK installation](https://github.com/openvswitch/ovs/blob/branch-2.5/INSTALL.DPDK.md)

  - [Wikipedia definition of DPDK](https://en.wikipedia.org/wiki/Data_Plane_Development_Kit)
