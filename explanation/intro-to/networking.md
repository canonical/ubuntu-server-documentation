(introduction-to-networking)=
# Introduction to networking

Networks consist of two or more devices which are connected by either physical cabling or wireless links for the purpose of sharing information. Devices can be computer systems, printers, and related equipment.

In this overview, we'll take a look at some of the key principles involved in networks, and some of the most popular tools available to help you manage your networks.

## Networking key concepts

If you're new to networking, our explanatory {ref}`Networking key concepts <networking-key-concepts>` section provides an overview of some important concepts. It includes detailed discussion of the popular network protocols: TCP/IP, IP routing, TCP and UDP, and ICMP.

## Network configuration with Netplan

Ubuntu uses [Netplan](https://netplan.io/) to configure networks. Netplan is a high-level, distribution-agnostic tool which uses a [YAML configuration file](https://netplan.readthedocs.io/en/stable/netplan-yaml/) to define your network.
 
Read {ref}`more about Netplan <about-netplan>`. 

If you are a server administrator, check out our explanatory guide on {ref}`configuring networks" <configuring-networks>`.

## Network tools and services

### DHCP

The Dynamic Host Configuration Protocol (DHCP) enables host computers to be automatically assigned settings from a server.

To learn more about DHCP and how configuration works, we have {ref}`an explanatory guide <about-dhcp>`.

There are two DHCP servers available on Ubuntu.  
 * **isc-kea** (available from 23.04 onwards)
 * **isc-dhcp-server** (no longer supported by vendor)

Learn how to {ref}`install isc-kea <install-isc-kea>` or {ref}`install and configure isc-dhcp-server <install-isc-dhcp-server>`.

### Time synchronisation

Network Time Protocol (NTP) synchronizes time over a network to within a few milliseconds of Coordinated Universal Time (UTC). Learn more about {ref}`time synchronisation <about-time-synchronisation>`.

Time is synchronized in Ubuntu by `timedatectl` and `timesyncd`. Both utilities are available by default as part of `systemd`. To find out how to configure this service, {ref}`read our how-to guide <timedatectl-and-timesyncd>`.

If you want to set up a server to *provide* NTP information, we suggest chrony. Learn {ref}`how to serve NTP using chrony <serve-ntp-with-chrony>` with this guide.

### The DPDK library

The [Data Plane Development Kit (DPDK)](https://www.dpdk.org/) is a set of libraries that improve network performance. Learn more {ref}`about DPDK and its use in Ubuntu <about-dpdk>`

One popular piece of software that uses DPDK is Open vSwitch (OVS). OVS runs inside a virtual machine (VM) and allows access to all virtual machines with a hypervisor. Check out our guide to find out {ref}`how to use DPDK with Open vSwitch <dpdk-with-open-vswitch>`.

## Other networking functionality

### Samba
  If you need to network Ubuntu and Microsoft devices together, use Samba. To get started, check out our {ref}`introduction to Samba <introduction-to-samba>`.
