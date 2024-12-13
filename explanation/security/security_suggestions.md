(security-suggestions)=
# Security suggestions

Although a fresh install of Ubuntu is relatively safe for immediate use on the
Internet, in this guide we’ll take a look at some steps you can take to help
keep your Ubuntu system safe and secure.

## For any Ubuntu system

The following suggestions are applicable generally to most Ubuntu systems. It
is not necessary to use all of these steps -- use the ones that are most
relevant for your setup.

### Keep your system up-to-date

1. **Regularly update** your Ubuntu system to keep it protected from known
   vulnerabilities. Run the following command periodically to update your
   system software:

   ```bash
   sudo apt update && sudo apt upgrade
   ```

   You may want to use the `unattended-upgrade` package to fetch and install
   security updates and bug fixes automatically:

   ```
   sudo apt install unattended-upgrades
   ```

   By default, `unattended-upgrade` runs daily, but this can be configured. See
   the `unattended-upgrade`
   [manual page](https://manpages.ubuntu.com/manpages/noble/en/man8/unattended-upgrades.8.html)
   for details.

1. **Manage your software**:

   * Remove packages you don't need, to minimise the potential attack surface
     you are exposing. See our article on
     {ref}`Package management <package-management>` for more details.

   * Avoid using third party repositories. If you need to download a package
     from a third party repository, make sure you
     {ref}`understand the risks and how to minimize them. <third-party-repository-usage>`.

1. **Use the most up-to-date release** of Ubuntu. If you are on an older Ubuntu
   release we have instructions on {ref}`how to upgrade <upgrade-your-release>`.
 
1. **Use [Ubuntu Pro](https://ubuntu.com/pro)**, particularly if you are on an
   older release of Ubuntu. Pro provides Enterprise-level security patching,
   but is free for personal/business use on up to 5 machines. The most useful
   Pro features for *any* Ubuntu Server are:

   * [Expanded Security Maintenance (ESM)](https://ubuntu.com/security/esm)
     which expands the Ubuntu LTS commitment on packages in Main from 5 years
     to 10 years -- and now also covers packages in Ubuntu Universe.
   
   * [Livepatch](https://ubuntu.com/security/livepatch) applies kernel patches
     for high and critical severity vulnerabilities while the system is running.
     This avoids the need for an immediate reboot.

   Most security patches can be fetched and applied automatically through the
   `unattended-upgrade` package. For more details on using and monitoring
   Ubuntu Pro via the command line, refer to the
   [official documentation](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/).

### Access Control

1. **Use and enforce** the
   [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege):

   * This means creating non-root user accounts with as few privileges as possible.
   * Not using `sudo` (root access) except for administration tasks.
   * For more details on basic access control, see our {ref}`guide on user management <user-management>`.

### Network security

1. **Use a firewall**. In Ubuntu, the uncomplicated firewall (`ufw`) tool is
   used to configure firewalls. `ufw` is a wrapper around the `iptables` utility
   (which experienced system admins may prefer to use directly). To get started
   with `ufw`, check out our {ref}`firewalls` guide.

1. **Use the Secure Shell (SSH)** protocol to secure remote access. In Ubuntu,
   this is managed through OpenSSH. For details on setting up OpenSSH, refer to
   our {ref}`guide to OpenSSH <openssh-server>`. 

### Physical security

There are also steps you can take to protect the physical security of your
system. These how-to guides will help you set up these additional precautions:

* {ref}`Smart card authentication <smart-card-authentication>`.
* {ref}`Smart card authentication with SSH <smart-card-authentication-with-ssh>`.
* {ref}`Console security <console-security>`.


(advanced-security)=
## Suggestions for complex setups

The following section will help direct you to the security-related packages for
which we provide documentation. For more discussion about advanced security
considerations, refer to the [Ubuntu Security](https://ubuntu.com/security)
documentation. 

### Advanced Access Control

1. **Lightweight Directory Access Protocol (LDAP)** is the usual way to gate
   access control for larger or more complex setups. In Ubuntu, this is
   implemented through OpenLDAP. Refer to our
   {ref}`introduction to OpenLDAP <introduction-to-openldap>`
   for more details, or see our section
   {ref}`on how to set up OpenLDAP <how-to-openldap>`.
1. **Kerberos** is a network authentication protocol that provides identity
   verification for distributed environments, commonly used in enterprise
   systems. Learn more in our
   {ref}`introduction to Kerberos <introduction-to-kerberos>`, or see our
   section on how to {ref}`set up and use Kerberos <how-to-kerberos>`.
1. **System Security Services Daemon (SSSD)** is a collection of daemons that
   handle authentication, authorisation and user/group information from
   disparate network sources. It integrates with OpenLDAP, Kerberos, and
   Active Directory as we discuss in more detail in our
   {ref}`introduction to SSSD <introduction-to-network-user-authentication-with-sssd>`
   or get started setting it up with our
   {ref}`how-to section <how-to-network-user-authentication-with-sssd>`.

### Virtual Private Networks (VPNs)

1. **WireGuard VPN**

   * {ref}`Introduction to WireGuard VPN <introduction-to-wireguard-vpn>`
   * {ref}`How to set up WireGuard VPN <how-to-wireguard-vpn>`

1. **OpenVPN**
   
   * {ref}`About OpenVPN clients <openvpn-client-implementations>`
   * {ref}`How to install OpenVPN <install-openvpn>`

### Security of communications

1. **TLS/SSL** for secure communication

<!--- We don't have specific pages on TLS or SSL individually, but we do have:
We don't have pages on TLS or SSL individually, but we do have:
How-to: LDAP: {ref}`LDAP and TLS <ldap-and-tls>` (this is the closest we have to a discussion of the topic, and it’s within the how-to LDAP section)
Explanation: Cryptography: {ref}`GnuTLS <gnutls>`
Explanation: Cryptography: {ref}`OpenSSL <openssl>`
Explanation: Cryptography: {ref}`Troubleshooting TLS/SSL <troubleshooting-tls>`
Explanation: security: {ref}`OpenVPN <openvpn-client-implementations>` which is a VPN in the SSL/TLS VPN stack (as opposed to an IPSec VPN)
--->

### Mandatory Access Controls (MAC)

1. **AppArmor**
   
   * {ref}`How to set up AppArmor <apparmor>`

### Cryptography / cryptographic libraries

1. **Crypto libraries**

   * {ref}`introduction-to-crypto-libraries`
   * {ref}`About crypto libraries <explanation-cryptography>`

1. **Certificates**

   * {ref}`About certificates <certificates>`
   * {ref}`Install root CA certificate in the trust store <install-a-root-ca-certificate-in-the-trust-store>`

### Compliance and auditing

If you need to adhere to specific industry standards, or are otherwise operating
in a high security environment, refer to the
[Ubuntu Security documentation](https://ubuntu.com/security/compliance-automation).




