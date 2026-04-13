---
myst:
  html_meta:
    description: Official Ubuntu Server documentation - comprehensive guides for installation, configuration, security, networking, databases, virtualization, and system administration.
---

# Ubuntu Server documentation

**Ubuntu Server** is a version of the Ubuntu operating system designed and engineered as a backbone for the internet.

Ubuntu Server brings economic and technical scalability to your data center, public or private. Whether you want to deploy an OpenStack cloud, a Kubernetes cluster or a 50,000-node render farm, Ubuntu Server delivers the best value scale-out performance available.

This documentation always targets the latest LTS version of Ubuntu. When there are differences towards older LTS releases, they are noted in the guide.

## In this documentation

### Getting started

The tutorial walks you through a fresh installation and the first steps of operating an Ubuntu Server.

* **Installation**: {ref}`System requirements <system-requirements>` • {ref}`Basic installation <basic-installation>` • {ref}`Ubuntu Pro subscription <attach-your-ubuntu-pro-subscription>`
* **System basics**: {ref}`Managing software <managing-software>` • {ref}`Customizing package files <changing-package-files>` • {ref}`third-party-repository-usage`


### Networking

Configure network interfaces, provide name and address services, share resources, and synchronize time.

* **Understanding networks**: {ref}`Key concepts <networking-key-concepts>` • {ref}`About Netplan <about-netplan>` • {ref}`Time synchronization <about-time-synchronisation>`
* **Configuration**: {ref}`Using Netplan <configuring-networks>` • {ref}`DNS <install-dns>` • {ref}`DHCP <install-isc-kea>`
* **With Windows systems**: {ref}`Samba <how-to-samba>` • {ref}`Windows Active Directory <how-to-active-directory-integration>`
* **Sharing**: {ref}`Files with NFS <install-nfs>` • {ref}`Printers with CUPS <cups-print-server>`


### Security

Protect your system with access controls, firewalls, encrypted communications, and network authentication.

* **Understanding security**: {ref}`Introduction <introduction-to-security>` • {ref}`security-suggestions` • {ref}`DNS Security Extensions (DNSSEC) <dnssec>`
* **Basic security**: {ref}`User management <user-management>` • {ref}`Firewalls <firewalls>` • {ref}`AppArmor <apparmor>`
* **Authentication**: {ref}`Install Kerberos <install-a-kerberos-server>` • {ref}`Set up SSSD with LDAP <sssd-with-ldap>` • {ref}`Smart cards <smart-card-authentication>`
* **Cryptography**: {ref}`Cryptographic libraries <introduction-to-crypto-libraries>` • {ref}`Install OpenSSH <openssh-server>`
* **VPNs**: {ref}`OpenVPN <install-openvpn>` • {ref}`WireGuard VPN <wireguard-on-an-internal-system>`


### Managing your system

Install, update, upgrade, and troubleshoot the software packages running on your system.

* **Managing software**: {ref}`Package management <package-management>` • {ref}`etckeeper <install-etckeeper>` • {ref}`Get older package versions using snapshots <snapshot-service>`
* **Update considerations**: {ref}`Automatic updates <automatic-updates>` • {ref}`Phased updates <about-apt-upgrade-and-phased-updates>` • {ref}`Testing updates in advance <advance-testing-of-updates-in-best-practice-server-deployments>`
* **Upgrade Ubuntu version**: {ref}`Release upgrades <upgrade-your-release>` • {ref}`Upgrade a virtual machine <upgrading-the-machine-type-of-your-vm>`
* **Troubleshooting**: {ref}`Report a bug <report-a-bug>` • {ref}`Debugging with debuginfod <about-debuginfod>` • {ref}`kernel-crash-dump`


### Data and storage

Store and manage data using directory services, databases, logical volumes, and backup tools.

* **Databases**: {ref}`MySQL <install-mysql>` • {ref}`PostgreSQL <install-postgresql>`
* **Directory services**: {ref}`introduction-to-openldap` • {ref}`Install OpenLDAP <install-openldap>` • {ref}`ldap-replication`
* **Device mapper multipathing**: {ref}`Intro to multipathing <introduction-to-multipath>` • {ref}`configuring-multipath`
* **Storage**: {ref}`About LVM <about-lvm>` • {ref}`Manage logical volumes <manage-logical-volumes>` • {ref}`Sharing data storage with iSCSI <iscsi-initiator-or-client>`
* **Version control**: {ref}`gitolite <install-gitolite>`


### Web and mail services

Serve web content, proxy traffic, write server-side applications, and handle email.

* **Web servers**: {ref}`About web servers <about-web-servers>` • {ref}`Apache2 <install-apache2>` • {ref}`nginx <install-nginx>`
* **Squid proxy server**: {ref}`About Squid proxy <about-squid-proxy-servers>` • {ref}`Install a Squid proxy server <install-a-squid-server>`
* **Mail services**: {ref}`Postfix <install-postfix>` • {ref}`Exim4 <install-exim4>` • {ref}`Dovecot <install-dovecot>`


### Virtualisation and containers

Run workloads in virtual machines and containers using lightweight and full-virtualisation tooling.

* **Understanding virtualization**: {ref}`Intro to virtualisation <introduction-to-virtualization>` • {ref}`VM tools <vm-tools-in-the-ubuntu-space>` • {ref}`Container tools <container-tools-in-the-ubuntu-space>`
* **Virtual machines**: {ref}`Multipass <create-vms-with-multipass>` • {ref}`QEMU <qemu>` • {ref}`qemu-microvm`
* **VM tooling**: {ref}`libvirt and virsh <libvirt>` • {ref}`virt-manager <virtual-machine-manager>` • {ref}`Nested virtualization <enable-nested-virtualisation>`
* **Containers**: {ref}`Docker for system admins <docker-for-system-admins>` • {ref}`docker-storage-networking-and-logging` • {ref}`run-rocks-on-your-server`
* **Deployment**: {ref}`Find cloud images <cloud-images>` • {ref}`Introduction to cloud-init <introduction-to-cloud-init>` • {ref}`LXD <lxd>`
* **Confidential computing**: {ref}`AMD SEV <sev-snp>` • {ref}`Intel TDX <intel-tdx>`


### Performance

Set up GPU resources and optimize system performance.

* **GPU resources**: {ref}`Install Nvidia drivers <nvidia-drivers-installation>` • {ref}`GPU virtualization <gpu-virtualization-with-qemu-kvm>`
* **Performance**:  • {ref}`CPU P-states <perf-p-states>` • {ref}`perf-tune-hwloc`
* **Optimization**: {ref}`CPU power management <perf-tune-cpupower>` • {ref}`perf-tune-tuned` • {ref}`Profile-Guided Optimization <perf-pgo>`
* **High availability**: {ref}`introduction-to-high-availability` • {ref}`Set up DRBD <install-drbd>` • {ref}`migrate-from-crmsh-to-pcs`


## How this documentation is organized

This documentation uses the [Diátaxis documentation structure](https://diataxis.fr/).
* The {ref}`Tutorial <tutorial>` takes you step-by-step through installing and setting up your first Ubuntu Server system.
* {ref}`How-to guides <how-to>` assume basic familiarity with Ubuntu Server and walk you through specific tasks.
* {ref}`Reference <reference>` provides system requirements, a glossary, and other technical specifications.
* {ref}`Explanation <explanation>` includes topic overviews, background and context, and detailed discussion of key concepts.


## Project and community

Ubuntu Server is a member of the Ubuntu family. It's an open source project
that welcomes community projects, contributions, suggestions, fixes and
constructive feedback.

* [Read our Code of Conduct](https://ubuntu.com/community/docs/ethos/code-of-conduct)
* [Get community support](https://ubuntu.com/support/community-support)
* [Join the Discourse forum](https://discourse.ubuntu.com/c/project/server/17)
* {matrix}`Chat to us on Matrix <server>`
* {ref}`Contribute to this documentation <contribute>`

If you find any errors or have suggestions for improvements, please use the
"Give feedback" button at the top of every page. This will take you to
GitHub where you can share your comments or let us know about bugs with any
page.

**Releases**
: [Download Ubuntu Server](https://ubuntu.com/download/server)
: [Ubuntu Release Notes](https://documentation.ubuntu.com/release-notes/)

**PDF versions of this documentation**
: [Current PDF](https://ubuntu.com/server/docs/_/downloads/en/latest/pdf/) (for Ubuntu 20.04 LTS onward)
: [Ubuntu 18.04 LTS PDF](https://assets.ubuntu.com/v1/8f8ea0cf-18-04-serverguide.pdf) (and earlier)

**Commercial support**
: Thinking about using Ubuntu Server for your next project? [Get in touch!](https://ubuntu.com/server/contact-us?product=server)


```{toctree}
:hidden:
:maxdepth: 2

Tutorial <tutorial/index.md>
How-to guides <how-to/index.md>
Reference <reference/index.md>
Explanation <explanation/index.md>
```

```{toctree}
:hidden:
:maxdepth: 2

Contributing <contributing/index.md>
```
