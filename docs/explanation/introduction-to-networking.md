(introduction-to-networking)=
# Networking

Networks consist of two or more devices, such as computer systems, printers, and related equipment, which are connected by either physical cabling or wireless links for the purpose of sharing and distributing information among the connected devices.

In this overview, we'll take a look at some of the key principles involved in networks, and at some of the most popular tools available to help you manage your networks.

## Networking key concepts

If you're new to networking, our explanatory ["Networking key concepts"](networking-key-concepts.md) section provides an overview of some important concepts. It includes detailed discussion of the popular network protocols: TCP/IP; IP routing; TCP and UDP; and ICMP.

## Configuring networks

Ubuntu ships with a number of graphical utilities to configure your network devices. Our explanatory guide on ["configuring networks"](configuring-networks.md) is geared toward server administrators focuses on managing your network on the command line.

## Network tools and services

### DHCP

The Dynamic Host Configuration Protocol (DHCP) enables host computers to be automatically assigned settings from a server. To learn more about DHCP and how configuration works, we have [an explanatory guide](about-dynamic-host-configuration-protocol-dhcp.md).

There are two DHCP servers available on Ubuntu. We have instructions on how to [install and configure `isc-dhcp-server`](../how-to/how-to-install-and-configure-isc-dhcp-server.md), and how to [install its replacement, `isc-kea`](../how-to/how-to-install-and-configure-isc-kea.md) (available from 23.04 onwards). 

### Time synchronisation

Synchronising time over a network is handled by the Network Time Protocol (NTP). It is a networking protocol that syncronises time between all computers on a network to within a few milliseconds of Coordinated Universal Time (UTC). This explanation guide will tell you [more about time synchronisation](about-time-synchronisation.md).

In Ubuntu, time synchronisation is primarily handled by `timedatectl` and `timesyncd`, which are installed by default as part of `systemd`. To find out how to configure this service, [read our how-to guide](about-time-synchronisation.md).

If you want to set up a server to *provide* NTP information, then we have a guide on [how to serve NTP using `chrony`](../how-to/how-to-serve-the-network-time-protocol-with-chrony.md).	

### The DPDK library

The [Data Plane Development Kit (DPDK)](https://www.dpdk.org/) provides a set of libraries that accelerate packet processing workloads. If you would like to find out more [about DPDK and its use in Ubuntu](about-dpdk.md), refer to our explanation page. 

One popular piece of software that makes use of DPDK is Open vSwitch (OVS), which can be run inside a VM and provides access to all virtual machines in the server hypervisor layer. Check out our guide to find out [how to use DPDK with Open vSwitch](../how-to/how-to-use-dpdk-with-open-vswitch.md).

## Other networking functionality

- **Samba**
  If you need to network together both Ubuntu and Microsoft machines, you will want to make use of Samba. To get started, check out our [introduction to Samba](introduction-to-samba.md).
