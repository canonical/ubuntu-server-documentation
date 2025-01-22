(introduction-to-networking)=
# Introduction to networking

Networks consist of two or more devices, such as computer systems, printers, and related equipment, which are connected by either physical cabling or wireless links for the purpose of sharing and distributing information among the connected devices.

In this overview, we'll take a look at some of the key principles involved in networks, and at some of the most popular tools available to help you manage your networks.

## Networking key concepts

If you're new to networking, our explanatory {ref}`Networking key concepts <networking-key-concepts>` section provides an overview of some important concepts. It includes detailed discussion of the popular network protocols: TCP/IP; IP routing; TCP and UDP; and ICMP.

## Network configuration with Netplan

Network configuration on Ubuntu is handled through [Netplan](https://netplan.io/), which provides a high-level, distribution-agnostic way to define how the network on your system should be set up via a [YAML configuration file](https://netplan.readthedocs.io/en/stable/netplan-yaml/). 
 
Read {ref}`more about Netplan <about-netplan>`, or check out our explanatory guide on {ref}`configuring networks" <configuring-networks>`, which is geared toward server administrators.

## Network tools and services

### DHCP

The Dynamic Host Configuration Protocol (DHCP) enables host computers to be automatically assigned settings from a server. To learn more about DHCP and how configuration works, we have {ref}`an explanatory guide <about-dhcp>`.

There are two DHCP servers available on Ubuntu. We have instructions on how to {ref}`install and configure isc-dhcp-server <install-isc-dhcp-server>`, and how to {ref}`install its replacement, isc-kea <install-isc-kea>` (available from 23.04 onwards). 

### Time synchronisation

Synchronising time over a network is handled by the Network Time Protocol (NTP). It is a networking protocol that synchronises time between all computers on a network to within a few milliseconds of Coordinated Universal Time (UTC). This explanation guide will tell you {ref}`more about time synchronisation <about-time-synchronisation>`.

In Ubuntu, time synchronisation is primarily handled by `timedatectl` and `timesyncd`, which are installed by default as part of `systemd`. To find out how to configure this service, {ref}`read our how-to guide <timedatectl-and-timesyncd>`.

If you want to set up a server to *provide* NTP information, then we have a guide on {ref}`how to serve NTP using chrony <serve-ntp-with-chrony>`.	

### The DPDK library

The [Data Plane Development Kit (DPDK)](https://www.dpdk.org/) provides a set of libraries that accelerate packet processing workloads. If you would like to find out more {ref}`about DPDK and its use in Ubuntu <about-dpdk>`, refer to our explanation page. 

One popular piece of software that makes use of DPDK is Open vSwitch (OVS), which can be run inside a VM and provides access to all virtual machines in the server hypervisor layer. Check out our guide to find out {ref}`how to use DPDK with Open vSwitch <dpdk-with-open-vswitch>`.

## Other networking functionality

- **Samba**
  If you need to network together both Ubuntu and Microsoft machines, you will want to make use of Samba. To get started, check out our {ref}`introduction to Samba <introduction-to-samba>`.
