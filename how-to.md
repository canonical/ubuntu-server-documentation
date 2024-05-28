# Ubuntu Server how-to guides


If you have a specific goal, but are already familiar with Ubuntu Server, our **how-to guides** have more in-depth detail than our tutorials and can be applied to a broader set of applications. They’ll help you achieve an end result but may require you to understand and adapt the steps to fit your specific requirements.

## Server installation

The following installation guides are more advanced than our getting started tutorial, but can be applied to specific scenarios. If you are looking for a more straightforward installation, refer to our [basic installation tutorial](tutorial/basic-installation.md).
 
|||
|--|--|
|AMD||
|| [amd64 netboot install](how-to/how-to-netboot-the-server-installer-on-amd64.md) |
| ARM ||
|| [arm64 netboot install](how-to/netboot-the-server-installer-via-uefi-pxe-on-arm-aarch64-arm64-and-x86-64-amd64.md) |
| ppc64el ||
|| [ppc64el netboot install](how-to/netboot-the-live-server-installer-on-ibm-power-ppc64el-with-petitboot.md) |
|| [Virtual CD-ROM and Petitboot on ppc64el](how-to/how-to-start-a-live-server-installation-on-ibm-power-ppc64el-with-a-virtual-cd-rom-and-petitboot.md) |
| s390x ||
|| [s390x install via z/VM](how-to/interactive-live-server-installation-on-ibm-z-vm-s390x.md) |
|| [IBM z/VM autoinstall on s390x](how-to/non-interactive-ibm-z-vm-autoinstall-s390x.md) |
|| [s390x install via LPAR](how-to/interactive-live-server-installation-on-ibm-z-lpar-s390x.md) |
|| [IBM LPAR autoinstall on s390x](how-to/non-interactive-ibm-z-lpar-autoinstall-s390x.md) |
|||

The Ubuntu installer now has its own documentation for automatic (or "hands-off" installations). For more guidance on auto-installing Ubuntu with the installer, you can refer to these guides from the Ubuntu installer documentation (note: these pages will redirect you outside of the Server Guide).

|||
|--|--|
| Autoinstallation with the Server installer ||
|| [Introduction to Automated Server installer](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) |
|| [Autoinstall quickstart](https://canonical-subiquity.readthedocs-hosted.com/en/latest/howto/autoinstall-quickstart.html) |
|| [Autoinstall quickstart on s390x](https://canonical-subiquity.readthedocs-hosted.com/en/latest/howto/autoinstall-quickstart-s390x.html) |
|||

## Virtualisation

|||
|--- | ---|
|Virtual machines (VMs) | |
|| [QEMU](how-to/virtualisation-with-qemu.md)|
|| [Create QEMU VMs with up to 1024 vCPUs](how-to/create-qemu-vms-with-up-to-1024-vcpus.md)|
|| [Boot ARM64 virtual machines on QEMU](how-to/boot-arm64-virtual-machines-on-qemu.md) |
|| [Create VMs with Multipass](how-to/how-to-create-a-vm-with-multipass.md)|
|| [Create cloud image VMs with UVtool](how-to/create-cloud-image-vms-with-uvtool.md)|
|VM tooling | |
|| [How to use the libvirt library with virsh](how-to/libvirt.md)|
|| [How to use virt-manager and other virt* tools](how-to/virtual-machine-manager.md)|
|| [How to enable nested virtualisation](how-to/how-to-enable-nested-virtualization.md)|
|Containers | |
|| [LXC](how-to/lxc-containers.md)|
|| [LXD](how-to/lxd-containers.md)|
|| [Docker for system admins](how-to/docker-for-system-admins.md)|
|Ubuntu in other virtual environments | |
|| [Setting up Ubuntu on Hyper-V (Windows 11)](how-to/how-to-set-up-ubuntu-on-hyper-v.md)|
|||

## Networking

If you would like a broader overview into these topics before getting started, you can refer to our [introduction to networking](explanation/introduction-to-networking.md), and our [introduction to Samba](explanation/introduction-to-samba.md). 

|||
|--|--|
|| [Network File System (NFS)](how-to/network-file-system-nfs.md) |
|| [File Transfer Protocol (FTP)](how-to/set-up-an-ftp-server.md) |
| Networking tools ||
|| [DHCP: Install `isc-kea`](how-to/how-to-install-and-configure-isc-kea.md) |
|| [DHCP: Install `isc-dhcp-server`](how-to/how-to-install-and-configure-isc-dhcp-server.md) |
|| [Time sync: Using timedatectl and timesyncd](how-to/use-timedatectl-and-timesyncd.md) |
|| [Time sync: Serve the Network Time Protocol](how-to/how-to-serve-the-network-time-protocol-with-chrony.md)|
|| [Install Open vSwitch with DPDK](how-to/how-to-use-dpdk-with-open-vswitch.md) |
|| [Domain Name Service (DNS)](how-to/domain-name-service-dns.md) |
| Samba ||
|| [Join Active Directory](how-to/member-server-in-an-active-directory-domain.md) |
|| [Set up a file server](how-to/samba-as-a-file-server.md) |
|| [Set up a print server](how-to/samba-as-a-print-server.md) |
|| [Set up share access controls](how-to/share-access-controls.md) |
|| [Create an AppArmor profile](how-to/samba-apparmor-profile.md) |
|| [Mount CIFS shares permanently](how-to/how-to-mount-cifs-shares-permanently.md) |
|| [NT4 domain controller (legacy)](how-to/nt4-domain-controller-legacy.md) |
|| [OpenLDAP backend (legacy)](how-to/openldap-backend-legacy.md) |
|||

## Authentication and access

|||
|--|--|
| Kerberos ||
|| [Install a Kerberos server](how-to/how-to-install-a-kerberos-server.md) |
|| [Configure service principals](how-to/how-to-configure-kerberos-service-principals.md) |
|| [Kerberos encryption types](how-to/kerberos-encryption-types.md) |
|| [Set up a secondary KDC](how-to/how-to-set-up-a-secondary-kdc.md) |
|| [Basic workstation authentication](how-to/how-to-set-up-basic-workstation-authentication.md) |
|| [Kerberos with OpenLDAP backend](how-to/how-to-set-up-kerberos-with-openldap-backend.md) |
| Set up network user authentication with SSSD and... ||
|| [Active directory](how-to/how-to-set-up-sssd-with-active-directory.md) |
|| [LDAP](how-to/how-to-set-up-sssd-with-ldap.md) |
|| [LDAP and Kerberos](how-to/how-to-set-up-sssd-with-ldap-and-kerberos.md) |
|| [How to troubleshoot SSSD](how-to/troubleshooting-sssd.md) |
| OpenLDAP ||
|| [Install and configure OpenLDAP](how-to/install-and-configure-ldap.md) |
|| [Set up access control](how-to/ldap-access-control.md) |
|| [Set up OpenLDAP with replication](how-to/openldap-replication.md) |
|| [Simple LDAP user and group management](how-to/how-to-set-up-ldap-users-and-groups.md) |
|| [OpenLDAP and Transport Layer Security (TLS)](how-to/ldap-and-transport-layer-security-tls.md) |
|| [Backup and restore OpenLDAP](how-to/backup-and-restore-openldap.md) |
| Active Directory integration ||
|| [Prepare to join a domain](how-to/join-a-domain-with-winbind-preparation.md)|
|| [Join a simple domain with the *rid* backend](how-to/join-a-simple-domain-with-the-rid-backend.md) |
|| [Join a forest with the *rid* backend](how-to/join-a-forest-with-the-rid-backend.md) |
|| [Join a forest with the *autorid* backend](how-to/join-a-forest-with-the-autorid-backend.md) |
||| 


## Databases

|||
|--|--|
| Databases ||
|| [Install and configure MySQL](how-to/install-and-configure-a-mysql-server.md) |
|| [Install and configure PostgreSQL](how-to/install-and-configure-postgresql.md) |
|||

## Mail services

|||
|--|--|
|| [Install Postfix](how-to/install-and-configure-postfix.md) |
|| [Install Dovecot](how-to/install-and-configure-dovecot.md) |
|| [Install Exim4](how-to/install-and-configure-exim4.md) |
|||

## Printing

|||
|--|--|
|| [Set up a CUPS print server](how-to/install-and-configure-a-cups-print-server.md)| 
|||

## Backups and version control

|||
|--|--|
|| [Install Bacula](how-to/how-to-install-and-configure-bacula.md) |
|| [Install rsnapshot](how-to/how-to-install-and-configure-rsnapshot.md) |
|| [Backup with shell scripts](how-to/how-to-back-up-using-shell-scripts.md) |
|| [etckeeper](how-to/etckeeper.md) |
|| [Install gitolite](how-to/how-to-install-and-configure-gitolite.md) | 
|||

## Web

|||
|--|--|
| Proxy servers ||
|| [Install a Squid server](how-to/how-to-install-a-squid-server.md) |
| Apache ||
|| [Install Apache2](how-to/how-to-install-apache2.md) |
|| [Configure Apache2](how-to/how-to-configure-apache2-settings.md) |
|| [Extend Apache2 with modules](how-to/how-to-use-apache2-modules.md) |
| Nginx ||
|| [Install nginx](how-to/how-to-install-nginx.md) |
|| [Configure nginx](how-to/how-to-configure-nginx.md) |
|| [Extend nginx with modules](how-to/how-to-use-nginx-modules.md) |
| Web Programming ||
|| [Install PHP](how-to/how-to-install-and-configure-php.md) |
|| [Install Ruby on Rails](how-to/how-to-install-and-configure-ruby-on-rails.md) |
| LAMP applications |
|| [Get started with LAMP applications](how-to/get-started-with-lamp-applications.md) |
|| [Install phpMyAdmin](how-to/how-to-install-and-configure-phpmyadmin.md) |
|| [Install WordPress](how-to/how-to-install-and-configure-wordpress.md) |
|||

## Storage

|||
|--|--|
|| [Manage logical volumes](how-to/how-to-manage-logical-volumes.md) |
|||

## Graphics

|||
|--|--|
| On-system GPU ||
|| [Nvidia driver installation](how-to/nvidia-drivers-installation.md) |
| Virtual GPU ||
|| [Virtualised GPU with QEMU/KVM](how-to/gpu-virtualization-with-qemu-kvm.md) |
|||

## Managing software

|||
|--|--|
|| [Package management](how-to/package-management.md) |
|| [Upgrade your release](how-to/how-to-upgrade-your-release.md) |
|| [Reporting bugs](how-to/how-to-report-a-bug-in-ubuntu-server.md) |
|| [Kernel crash dump](how-to/kernel-crash-dump.md) |
|| [Puppet](how-to/how-to-install-and-use-puppet.md) |
|||

## Security

|||
|--|--|
|| [OpenSSH](how-to/openssh-server.md) |
|| [OpenVPN](how-to/how-to-install-and-use-openvpn.md) |
|| [CA trust store](how-to/install-a-root-ca-certificate-in-the-trust-store.md) |
|| [Firewall](how-to/firewalls.md) |
|| [AppArmor](how-to/apparmor.md) |
|| [Smart card authentication](how-to/smart-card-authentication.md) |
|| [Smart card SSH](how-to/smart-card-authentication-with-ssh.md) |
|| [User management](how-to/user-management.md) |
|| [Console security](how-to/console-security.md) |
| Wireguard VPN ||
|| [Peer-to-site](how-to/wireguard-vpn-peer-to-site.md) |
|| [Peer-to-site (on router)](how-to/wireguard-vpn-peer-to-site-on-router.md) |
|| [Peer-to-site (inside device)](how-to/wireguard-on-an-internal-system.md) |
|| [Site-to-site](how-to/wireguard-vpn-site-to-site.md) |
|| [Default gateway](how-to/using-the-vpn-as-the-default-gateway.md) |
|| [Common tasks](how-to/common-tasks-in-wireguard-vpn.md) |
|| [Security tips](how-to/security-tips-for-wireguard-vpn.md) |
|| [Troubleshooting](how-to/troubleshooting-wireguard-vpn.md) |

## High Availability

|||
|--|--|
|| [Distributed Replicated Block Device (DRBD)](how-to/distributed-replicated-block-device-drbd.md) |

## Observability

|||
|--|--|
|| [Logging, Monitoring and Alerting (LMA)](how-to/set-up-your-lma-stack.md) |
|| [Install Logwatch](how-to/how-to-install-and-configure-logwatch.md) |
|| [Install Munin](how-to/how-to-install-and-configure-munin.md) |
|| [Install Nagios Core 3](how-to/how-to-install-and-configure-nagios-core-3.md) | 
|| [Use Nagios with Munin](how-to/how-to-use-nagios-with-munin.md) |


```{toctree}
:hidden:
how-to/how-to-netboot-the-server-installer-on-amd64.md
how-to/netboot-the-server-installer-via-uefi-pxe-on-arm-aarch64-arm64-and-x86-64-amd64.md
how-to/netboot-the-live-server-installer-on-ibm-power-ppc64el-with-petitboot.md
how-to/how-to-start-a-live-server-installation-on-ibm-power-ppc64el-with-a-virtual-cd-rom-and-petitboot.md
how-to/interactive-live-server-installation-on-ibm-z-vm-s390x.md
how-to/non-interactive-ibm-z-vm-autoinstall-s390x.md
how-to/interactive-live-server-installation-on-ibm-z-lpar-s390x.md
how-to/non-interactive-ibm-z-lpar-autoinstall-s390x.md
how-to/virtualisation-with-qemu.md
how-to/create-qemu-vms-with-up-to-1024-vcpus.md
how-to/boot-arm64-virtual-machines-on-qemu.md
how-to/how-to-create-a-vm-with-multipass.md
how-to/create-cloud-image-vms-with-uvtool.md
how-to/libvirt.md
how-to/virtual-machine-manager.md
how-to/how-to-enable-nested-virtualization.md
how-to/lxc-containers.md
how-to/lxd-containers.md
how-to/docker-for-system-admins.md
how-to/how-to-set-up-ubuntu-on-hyper-v.md
how-to/network-file-system-nfs.md
how-to/set-up-an-ftp-server.md
how-to/how-to-install-and-configure-isc-kea.md
how-to/how-to-install-and-configure-isc-dhcp-server.md
how-to/use-timedatectl-and-timesyncd.md
how-to/how-to-serve-the-network-time-protocol-with-chrony.md
how-to/how-to-use-dpdk-with-open-vswitch.md
how-to/domain-name-service-dns.md
how-to/member-server-in-an-active-directory-domain.md
how-to/samba-as-a-file-server.md
how-to/samba-as-a-print-server.md
how-to/share-access-controls.md
how-to/samba-apparmor-profile.md
how-to/how-to-mount-cifs-shares-permanently.md
how-to/nt4-domain-controller-legacy.md
how-to/openldap-backend-legacy.md
how-to/join-a-domain-with-winbind-preparation.md
how-to/join-a-simple-domain-with-the-rid-backend.md
how-to/join-a-forest-with-the-rid-backend.md
how-to/join-a-forest-with-the-autorid-backend.md
how-to/how-to-install-a-kerberos-server.md
how-to/how-to-configure-kerberos-service-principals.md
how-to/kerberos-encryption-types.md
how-to/how-to-set-up-a-secondary-kdc.md
how-to/how-to-set-up-basic-workstation-authentication.md
how-to/how-to-set-up-kerberos-with-openldap-backend.md
how-to/how-to-set-up-sssd-with-active-directory.md
how-to/how-to-set-up-sssd-with-ldap.md
how-to/how-to-set-up-sssd-with-ldap-and-kerberos.md
how-to/troubleshooting-sssd.md
how-to/install-and-configure-ldap.md
how-to/ldap-access-control.md
how-to/openldap-replication.md
how-to/how-to-set-up-ldap-users-and-groups.md
how-to/ldap-and-transport-layer-security-tls.md
how-to/backup-and-restore-openldap.md
how-to/install-and-configure-a-mysql-server.md
how-to/install-and-configure-postgresql.md
how-to/install-and-configure-postfix.md
how-to/install-and-configure-dovecot.md
how-to/install-and-configure-exim4.md
how-to/install-and-configure-a-cups-print-server.md
how-to/how-to-install-and-configure-bacula.md
how-to/how-to-install-and-configure-rsnapshot.md
how-to/how-to-back-up-using-shell-scripts.md
how-to/etckeeper.md
how-to/how-to-install-and-configure-gitolite.md
how-to/how-to-install-a-squid-server.md
how-to/how-to-install-apache2.md
how-to/how-to-configure-apache2-settings.md
how-to/how-to-use-apache2-modules.md
how-to/how-to-install-nginx.md
how-to/how-to-configure-nginx.md
how-to/how-to-use-nginx-modules.md
how-to/how-to-install-and-configure-php.md
how-to/how-to-install-and-configure-ruby-on-rails.md
how-to/get-started-with-lamp-applications.md
how-to/how-to-install-and-configure-phpmyadmin.md
how-to/how-to-install-and-configure-wordpress.md
how-to/how-to-manage-logical-volumes.md
how-to/nvidia-drivers-installation.md
how-to/gpu-virtualization-with-qemu-kvm.md
how-to/package-management.md
how-to/how-to-upgrade-your-release.md
how-to/how-to-report-a-bug-in-ubuntu-server.md
how-to/kernel-crash-dump.md
how-to/how-to-install-and-use-puppet.md
how-to/openssh-server.md
how-to/how-to-install-and-use-openvpn.md
how-to/install-a-root-ca-certificate-in-the-trust-store.md
how-to/firewalls.md
how-to/apparmor.md
how-to/smart-card-authentication.md
how-to/smart-card-authentication-with-ssh.md
how-to/user-management.md
how-to/console-security.md
how-to/wireguard-vpn-peer-to-site.md
how-to/wireguard-vpn-peer-to-site-on-router.md
how-to/wireguard-on-an-internal-system.md
how-to/wireguard-vpn-site-to-site.md
how-to/using-the-vpn-as-the-default-gateway.md
how-to/common-tasks-in-wireguard-vpn.md
how-to/security-tips-for-wireguard-vpn.md
how-to/troubleshooting-wireguard-vpn.md
how-to/distributed-replicated-block-device-drbd.md
how-to/set-up-your-lma-stack.md
how-to/how-to-install-and-configure-logwatch.md
how-to/how-to-install-and-configure-munin.md
how-to/how-to-install-and-configure-nagios-core-3.md
how-to/how-to-use-nagios-with-munin.md
```