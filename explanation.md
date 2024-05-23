# Ubuntu Server explanation guides

Our explanatory and conceptual guides are written to provide a better understanding of how Ubuntu Server works and how it can be used and configured. They enable you to expand your knowledge, making the operating system easier to use.

## Introduction to...
If you're not sure how or where to get started with a topic, these introductory pages will give you a high-level overview and relevant links (with context!) to help you navigate easily to the guides and other materials of most interest to you. 

|||
|--|--|
| Virtualization ||
|| [Introduction to virtualization](explanation/introduction-to-virtualization.md) |
|Networks||
|| [Introduction to networking](explanation/introduction-to-networking.md) |
|| [Introduction to Samba](explanation/introduction-to-samba.md) |
|| [Introduction to Active Directory integration](explanation/introduction-to-active-directory-integration.md/) |
|| [Introduction to device mapper multipathing](explanation/introduction-to-device-mapper-multipathing.md) |
| Authentication and access ||
|| [Introduction to Kerberos](explanation/introduction-to-kerberos.md) ||
|| [Introduction to SSSD](explanation/introduction-to-network-user-authentication-with-sssd.md) ||
|| [Introduction to OpenLDAP](explanation/introduction-to-openldap.md) | 
| Security ||
|| [Introduction to security](explanation/introduction-to-security.md) |
|| [Introduction to crypto libraries](explanation/introduction-to-crypto-libraries.md) |
|| [Introduction to Wireguard VPN](explanation/introduction-to-wireguard-vpn.md)
| Useful services ||
|| [Introduction to mail servers](explanation/introduction-to-mail-services.md) |
|| [Introduction to web servers](explanation/introduction-to-web-servers.md)
|| [Introduction to backups](explanation/introduction-to-backups.md) |
|| [Introduction to databases](explanation/introduction-to-databases.md) |
| High availability ||
|| [Introduction to high availability](explanation/introduction-to-high-availability.md) ||
|||

## Virtualisation and containers
|||
|--|--|
| About virtual machines ||
|| [Overview of VM tools in Ubuntu](explanation/vm-tools-in-the-ubuntu-space.md) |
| Using virtual machines ||
|| [Using QEMU for microVMs](explanation/using-qemu-for-microvms.md)
|| [Upgrading the machine type of your VM](explanation/upgrading-the-machine-type-of-your-vm.md) |
| About containers ||
|| [Overview of container tools in Ubuntu](explanation/container-tools-in-the-ubuntu-space.md) |
| Other virtualization tools ||
|| [About OpenStack](explanation/about-openstack.md) |
|||

## Networking

|||
|--|--|
| Networking ||
|| [Networking key concepts](explanation/networking-key-concepts.md) |
|| [Configuring networks](explanation/configuring-networks.md) |
|| [About DHCP](explanation/about-dynamic-host-configuration-protocol-dhcp.md) |
|| [Time synchronisation](explanation/about-time-synchronisation.md) |
|| [The DPDK library](explanation/about-dpdk.md) |
|||

## Active Directory integration

|||
|--|--|
|| [Choosing an integration method](explanation/choosing-an-integration-method.md) |
|| [Security identifiers (SIDs)](explanation/security-identifiers-sids.md) |
|| [Identity mapping backends](explanation/identity-mapping-idmap-backends.md) |
|| [The *rid* idmap backend](explanation/the-rid-idmap-backend.md) |
|| [The *autorid* idmap backend](explanation/the-autorid-idmap-backend.md) |
|||

## Security

|||
|--|--|
|| [OpenVPN clients](explanation/openvpn-client-implementations.md) |
|| [Certificates](explanation/certificates.md) |
| Cryptography ||
|| [OpenSSL](explanation/openssl.md) |
|| [GnuTLS](explanation/gnutls.md) |
|| [Network Security Services (NSS)](explanation/network-security-services-nss.md) |
|| [Java cryptography configuration](explanation/java-cryptography-configuration.md) |
|| [BIND 9 DNSSEC cryptography selection](explanation/bind-9-dnssec-cryptography-selection.md) |
|| [OpenSSH crypto configuration](explanation/openssh-crypto-configuration.md) |
|| [Troubleshooting TLS/SSL](explanation/troubleshooting-tls-ssl.md) |
|||

## Server installation

|||
|--|--|
| | [Choosing between the arm64 and arm64+largemem installer options](explanation/choosing-between-the-arm64-and-arm64-largemem-installer-options.md) |
|||

## Storage

|||
|--|--|
|| [About LVM](explanation/about-logical-volume-management-lvm.md) |
|| [iSCSI](explanation/iscsi-initiator-or-client.md) |
|||

## Managing software

|||
|--|--|
| Software ||
|| [About 'apt upgrade' and phased updates](explanation/about-apt-upgrade-and-phased-updates.md) |
|| [Third party repository usage](explanation/third-party-repository-usage.md) |
|| [Changing package files](explanation/changing-package-files.md) |
|||

## Web servers
|||
|--|--|
| Details and key concepts... ||
|| [About web servers](explanation/about-web-servers.md)
|| [About Squid proxy servers](explanation/about-squid-proxy-servers.md) |
|||

## System tuning
|||
|--|--|
| Useful tools ||
| | [TuneD](explanation/tuned.md) |
|||

## High availability

|||
|--|--|
|| [Pacemaker resource agents](explanation/pacemaker-resource-agents.md) |
|| [Pacemaker fence agents](explanation/pacemaker-fence-agents.md) |
|||

## Multipath

|||
|--|--|
|| [Configuration options and overview](explanation/configuring-device-mapper-multipathing.md) |
|| [Configuration examples](explanation/multipath-configuration-examples.md) |
|| [Common tasks and procedures](explanation/common-multipath-tasks-and-procedures.md) |
|||


```{toctree}
:hidden:
explanation/introduction-to-virtualization.md
explanation/introduction-to-networking.md
explanation/introduction-to-samba.md
explanation/introduction-to-active-directory-integration.md
explanation/introduction-to-device-mapper-multipathing.md
explanation/introduction-to-kerberos.md
explanation/introduction-to-network-user-authentication-with-sssd.md
explanation/introduction-to-openldap.md
explanation/introduction-to-security.md
explanation/introduction-to-crypto-libraries.md
explanation/introduction-to-wireguard-vpn.md
explanation/introduction-to-mail-services.md
explanation/introduction-to-web-servers.md
explanation/introduction-to-backups.md
explanation/introduction-to-databases.md
explanation/introduction-to-high-availability.md
explanation/vm-tools-in-the-ubuntu-space.md
explanation/using-qemu-for-microvms.md
explanation/upgrading-the-machine-type-of-your-vm.md
explanation/container-tools-in-the-ubuntu-space.md
explanation/about-openstack.md
explanation/networking-key-concepts.md
explanation/configuring-networks.md
explanation/about-dynamic-host-configuration-protocol-dhcp.md
explanation/about-time-synchronisation.md
explanation/about-dpdk.md
explanation/choosing-an-integration-method.md
explanation/security-identifiers-sids.md
explanation/identity-mapping-idmap-backends.md
explanation/the-rid-idmap-backend.md
explanation/the-autorid-idmap-backend.md
explanation/openvpn-client-implementations.md
explanation/certificates.md
explanation/openssl.md
explanation/gnutls.md
explanation/network-security-services-nss.md
explanation/java-cryptography-configuration.md
explanation/bind-9-dnssec-cryptography-selection.md
explanation/openssh-crypto-configuration.md
explanation/troubleshooting-tls-ssl.md
explanation/choosing-between-the-arm64-and-arm64-largemem-installer-options.md
explanation/about-logical-volume-management-lvm.md
explanation/iscsi-initiator-or-client.md
explanation/about-apt-upgrade-and-phased-updates.md
explanation/third-party-repository-usage.md
explanation/changing-package-files.md
explanation/about-web-servers.md
explanation/about-squid-proxy-servers.md
explanation/tuned.md
explanation/pacemaker-resource-agents.md
explanation/pacemaker-fence-agents.md
explanation/configuring-device-mapper-multipathing.md
explanation/multipath-configuration-examples.md
explanation/common-multipath-tasks-and-procedures.md
```