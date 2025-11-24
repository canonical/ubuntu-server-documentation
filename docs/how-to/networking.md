(how-to-networking)=
# Networking

This section contains how-to guides on most aspects of networking in Ubuntu. If you would like a broader overview of these topics before getting started, refer to our {ref}`introduction to networking <introduction-to-networking>`.

## Configuration

Network configuration in Ubuntu is handled through Netplan. See our general walkthrough on {ref}`configuring-networks`, or refer to [the Netplan documentation](https://netplan.readthedocs.io/en/stable/) for more specific instructions.

## Network tools

The File Transfer Protocol (FTP) can be set up to provide files for download.

```{toctree}
:titlesonly:

File transfers with FTP <networking/ftp>
```

The Domain Name Service (DNS) maps IP addresses to fully qualified domain names (FQDN). The DNS Security Extensions (DNSSEC) allow DNS data to be verified.

```{toctree}
:titlesonly:

Set up a name server (DNS) <networking/install-dns>
Set up DNS Security Extensions (DNSSEC) <networking/install-dnssec>
DNSSEC Troubleshooting <networking/dnssec-troubleshooting>
```

Open vSwitch (OVS) with the Data Plane Development Kit (DPDK) provides virtual switching for network automation in virtualized environments. 

```{toctree}
:titlesonly:

Use Open vSwitch with DPDK <networking/dpdk-with-open-vswitch>
```

## DHCP

Set up Dynamic Host Configuration Protocol (DHCP) for automatic IP address assignment for devices on your network. There are two DHCP servers available in Ubuntu: `isc-kea` is the most modern, and is available from 23.04 onwards.

```{toctree}
:titlesonly:

Install DHCP isc-kea <networking/install-isc-kea>
Install DHCP isc-dhcp-server <networking/install-isc-dhcp-server>
```

## Time synchronization

The Network Time Protocol (NTP) synchronizes time over a network. Ubuntu uses `chrony` by default to handle this. However, users can install and use `timedatectl`/`timesyncd` instead if preferred.

```{toctree}
:titlesonly:

Time sync with chrony <networking/chrony-client>
Time sync with timedatectl and timesyncd <networking/timedatectl-and-timesyncd>
Serving time with chrony <networking/serve-ntp-with-chrony>
```

## Network shares

Sharing files and resources across a network is a common requirement - this is where the Network File System (NFS) comes in.

```{toctree}
:titlesonly:

Network File System (NFS) sharing <networking/install-nfs>
```

If you need to share network resources between Linux and Windows systems, see our sections on Samba and Active Directory.

```{toctree}
:titlesonly:
:hidden:

Samba <samba>
Active Directory integration <active-directory>
```

* {ref}`Samba <how-to-samba>`
* {ref}`Active Directory integration <how-to-active-directory-integration>`

## Printing

The Common UNIX Printing System (CUPS) is the most common way to manage print services in Ubuntu. 

```{toctree}
:titlesonly:

Set up a CUPS print server <networking/cups-print-server>
```

## See also

* Explanation: {ref}`Networking section <explanation-networking>`
