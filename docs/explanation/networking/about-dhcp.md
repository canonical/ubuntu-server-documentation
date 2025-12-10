---
myst:
  html_meta:
    description: "Learn how Dynamic Host Configuration Protocol (DHCP) automatically assigns network settings to host computers, including IP addresses and gateway configurations."
---

(about-dhcp)=
# About DHCP

The Dynamic Host Configuration Protocol (DHCP) is a network service that enables host computers to be automatically assigned settings from a server as opposed to manually configuring each network host. Computers configured to be DHCP clients have no control over the settings they receive from the DHCP server, and the configuration is transparent to the computer's user.

The most common settings provided by a DHCP server to DHCP clients include:

  - IP address and netmask

  - IP address of the default-gateway to use

  - IP addresses of the {term}`DNS` servers to use

However, a DHCP server can also supply configuration properties such as:

  - {term}`Hostname`

  - Domain name

  - Time server

  - Print server

The advantage of using DHCP is that any changes to the network, such as a change in the DNS server address, only need to be changed at the DHCP server, and all network hosts will be reconfigured the next time their DHCP clients poll the DHCP server. As an added advantage, it is also easier to integrate new computers into the network, as there is no need to check for the availability of an IP address. Conflicts in IP address allocation are also reduced.

## DHCP configuration 

A DHCP server can provide configuration settings using the following methods:

### Manual allocation (MAC address) 

This method uses DHCP to identify the unique hardware address of each network card connected to the network, and then supplies a static configuration each time the DHCP client makes a request to the DHCP server using that network device. This ensures that a particular address is assigned automatically to that network card, based on its MAC address.

### Dynamic allocation (address pool)  
 In this method, the DHCP server assigns an IP address from a pool of addresses (sometimes also called a range or scope) for a period of time (known as a lease) configured on the server, or until the client informs the server that it doesn't need the address anymore. This way, the clients receive their configuration properties dynamically and on a "first come, first served" basis. When a DHCP client is no longer on the network for a specified period, the configuration is expired and released back to the address pool for use by other DHCP clients. After the lease period expires, the client must renegotiate the lease with the server to maintain use of the same address.

### Automatic allocation
Using this method, the DHCP automatically assigns an IP address permanently to a device, selecting it from a pool of available addresses. Usually, DHCP is used to assign a temporary address to a client, but a DHCP server can allow an infinite lease time.

The last two methods can be considered "automatic" because in each case the DHCP server assigns an address with no extra intervention needed. The only difference between them is in how long the IP address is leased; in other words, whether a client's address varies over time.

## Available servers

Ubuntu makes two DHCP servers available:

- `isc-dhcp-server`:
  This server installs `dhcpd`, the dynamic host configuration protocol daemon. Although Ubuntu still supports `isc-dhcp-server`, this software is [no longer supported by its vendor](https://www.isc.org/blogs/isc-dhcp-eol/).

  Find out {ref}`how to install and configure isc-dhcp-server <install-isc-dhcp-server>`.

- `isc-kea`:
  [Kea](https://www.isc.org/kea/) was created by ISC to replace `isc-dhcp-server` -- It is supported in Ubuntu releases from 23.04 onward.

  Find out {ref}`how to install and configure isc-kea <install-isc-kea>`.


## References

- The [`isc-dhcp-server` Ubuntu Wiki](https://help.ubuntu.com/community/isc-dhcp-server) page has more information.

- For more `/etc/dhcp/dhcpd.conf` options see the {manpage}`dhcpd.conf(5)` manual page

- [ISC `dhcp-server`](https://www.isc.org/software/dhcp)

- [ISC Kea Documentation](https://kb.isc.org/docs/kea-administrator-reference-manual)
