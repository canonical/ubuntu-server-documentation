(introduction-to-security)=
# Introduction to security

Security should always be considered when installing, deploying, and using any
type of computer system. Although a fresh installation of Ubuntu is relatively
safe for immediate use on the Internet, it is important to have a balanced
understanding of your system's security posture based on how it will be used
after deployment.

## General guidance for all systems

It is generally good practice to take a proactive and layered approach to
security. These suggestions are good practices for any Ubuntu system.

## Keep your system up-to-date

1. **Regularly update** your Ubuntu Server to keep it protected from known
   vulnerabilities:

   ```bash
   sudo apt update && sudo apt upgrade
   ```

1. **Use the `unattended-upgrade` package** to automatically fetch and install
   security updates and bug fixes:

   ```
   sudo apt install unattended-upgrades
   ```

   By default, `unattended-upgrade` runs daily, but this can be configured. See
   the `unattended-upgrade`
   [manual page](https://manpages.ubuntu.com/manpages/noble/en/man8/unattended-upgrades.8.html)
   for details.

1. **Use Ubuntu Pro**. If you are on an older Ubuntu release and don't want to
   upgrade just yet, Ubuntu Pro provides
   [10 years of security coverage](https://ubuntu.com/security/esm) for all
   packages in the Main and Universe repositories. It is free for personal or
   business use on up to 5 machines.

1. **Remove packages you don't need**, to minimise the
   potential attack surface. See our article on
   {ref}`Package management <package-management>` for more details.

1. It's also a good idea to **use the most up-to-date release** of Ubuntu
   Server. We have instructions on
   {ref}`how to upgrade your release <upgrade-your-release>`.

## Access Control

1. **Use and enforce** the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege):

   * This means creating non-root user accounts with as few privileges as possible
   * Not using `sudo` (root access) except for administration tasks
   * For more details on basic access control, see our {ref}`guide on user management <user-management>` 

1. Use the **Secure Shell (SSH)** protocol to secure remote access. In Ubuntu,
   this is managed through the OpenSSH software. For details on setting up
   OpenSSH, refer to our {ref}`guide to OpenSSH <openssh-server>`.

1. For larger or more complex setups, access control is usually gated through
   tools such as OpenLDAP. Refer to our
   {ref}`introduction to OpenLDAP <introduction-to-openldap>`
   for more details, or see our section
   {ref}`on how to set up OpenLDAP <how-to-openldap>`.

## Network security

1. **Use a firewall**. ufw {ref}`firewalls`

<!--- * Close unused ports: scan
 do we have anything about ports? --->

<!--- Does Network security fall under encryptying data in transit? --->

<!--- Do we need to include our networking content on DNSSEC?
* {ref}`install-dnssec`
--->

<!--- For network authentication/authorisation/user and groups from a variety of network sources, we also have SSSD --->

## Data Protection:

* At rest:

  Tools like LUKS for full-disk encryption <!--- currently only have any mention of LUKS in the subiquity docs --->
  Physical security: Smart card authentication (+ with SSH - overlaps with SSH)
  <!-- missing content about yubikeys -->
  Console security
  <!-- Do we need anything backup policies or disaster recovery plans? redundancy? -->

* In transit

  TLS/SSL for secure communication <!--- We don't have pages on TLS or SSL individually, but we do have:
  
  * {ref}`LDAP and TLS <ldap-and-tls>`
  * {ref}`Troubleshooting TLS/SSL <>`
    --->

Link to - do we have specific pages about this?
- nothing about luks, only referenced in the subiquity pages
- TLS - we have LDAP and TLS, troubleshooting TLS/SSL, GnuTLS
* :ref:``

## Monitoring and Logging:

* Actively monitor server activity and maintain logs using tools like journalctl or centralized logging frameworks. - nothing in logging about this
* Detect and block suspicious behavior with tools like Fail2ban.

detect and block/fail2ban - missing
journalctl - nothing specifically about this


These foundational practices are crucial for any Ubuntu Server deployment, ensuring that the server is resistant to common attack vectors.

## Ubuntu Pro


<!--- We need a trampoline to CVEs/USNs and the disclosure policy --->


* Information about known vulnerabilities:
  * per CVE check out the [CVE overview](https://ubuntu.com/security/cves)
  * per Package have a look at the [Ubuntu Security Notices](https://ubuntu.com/security/notices)
* Reporting a security issue, have a look at the [disclosure policy](https://ubuntu.com/security/disclosure-policy)

### Kernel application hardening:

* [Canonical Livepatch](https://ubuntu.com/security/livepatch) applies kernel
  patches for high and critical severity vulnerabilities, while the system is
  running, and without the need for an immediate reboot.
  
### ESM



# Advanced topics

## Centralised access and identity management

* Lightweight Directory Access Protocol (LDAP)
* Kerberos

## VPNs and network segmentation

* WireGuard VPN

<!--- we don't have anything specifically called out about network segmentation - is it really that important? --->

## Mandatory Access Controls (MAC)

* AppArmor

## Cryptography / cryptographic libraries

* intro to crypto libraries {ref}`crypto-libraries`

## Compliance and auditing:

If you need to adhere to specific industry standards, refer to the Ubuntu
Security Guide.

* FIPS
* CIS/USG

<!--- FOR YANA: what do we have in the security docs that we should link to on this topic? --->
<!--- it's beyond the scope of the server docs to document the different compliance stuff, but we should have a single page trampoline that introduces the concept and provides links --->

