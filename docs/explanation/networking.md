(explanation-networking)=
# Networking

This section contains introductions to (and more details about) various aspects of networking in Ubuntu. 

## Introduction

If you are new to networking, you should start with these pages to obtain an understanding of the key terms and concepts.

```{toctree}
:titlesonly:

intro-to/networking
Networking key concepts <networking/networking-key-concepts>
```

## Configuration

Network configuration in Ubuntu is handled through Netplan. Find out more {ref}`About Netplan <about-netplan>` or get started with our walkthrough on {ref}`network configuration <configuring-networks>` which gives a practical demonstration.

```{toctree}
:hidden:

About Netplan <networking/about-netplan>
Configuring networks <networking/configuring-networks>
```

## Network tools

In our how-to section we show to set up virtual switching using Open vSwitch (OVS) and the Data Plane Development Kit (DPDK) library. This page discusses DPDK in more detail.

* {ref}`about-dpdk` discusses DPDK in more detail

```{toctree}
:hidden:

The DPDK library <networking/about-dpdk>
```

## DHCP

The Dynamic Host Configuration Protocol (DHCP) handles automatic IP address assignment.

* {ref}`About DHCP <about-dhcp>` gives detail about DHCP and how it works

```{toctree}
:hidden:

About DHCP <networking/about-dhcp>
```

## Time synchronisation

* {ref}`About time synchronisation <about-time-synchronisation>` discusses the Network Time Protocol (NTP) and how it works

```{toctree}
:hidden:

Time synchronisation <networking/about-time-synchronisation>
```

## Network shares

Samba and Active Directory are two tools you will need if you want to share resources and directories between Linux and Windows systems.

* {ref}`introduction-to-samba` will talk you through the key concepts you will need to be able to follow our how-to guides on Samba
* Our {ref}`explanation-active-directory-integration` section has both an introduction and in-depth discussion about Active Directory integration

```{toctree}
:hidden:

intro-to/samba
active-directory
```

## See also

* How-to: {ref}`Networking section <how-to-networking>`
