(introduction-to-security)=
# Introduction to security

Security should always be considered when you install, deploy, and use an
Ubuntu system. While a fresh installation of Ubuntu is usually safe for
immediate use, your system's security posture will be very important depending
on how it is used after it is deployed. You should always employ a layered
approach to security so that that your system does not rely on a single
point of defense.

## Server security guidance

Since Ubuntu is endlessly customizable like most Linux distributions, this 
introduction cannot serve as a full guide to security hardening. However, 
you can apply certain good practices and security-related packages to almost
any Ubuntu system. Our {ref}`security suggestions <security-suggestions>` 
page contains an overview of the good habits and practices that can
make any Ubuntu system more secure. You may not want to apply every 
suggestion -- and the list is not exhaustive by any means -- but 
each suggestion can provide an extra layer of security.

If your Ubuntu setup is more advanced or more complex than others, you may 
need to do more research into your security outlook. There are specific 
packages available for Ubuntu Servers that can provide additional security, and
we suggest some packages in the {ref}`advanced security <advanced-security>` 
section that you might want to investigate. Again, the list in this section
is not  intended to be exhaustive, but rather a starting point.

To read the most thorough treatment of security in Ubuntu, go to the
[Ubuntu Security documentation](https://ubuntu.com/security).

When you are considering security for your Ubuntu system, you should
think about using Canonical's services--Ubuntu Pro, Expanded Security 
Maintenance, and Livepatch.

## Ubuntu Pro

If you want someone to provide security, compliance and support services,
Canonical can provide them through the [Ubuntu Pro](https://ubuntu.com/pro)
subscription. Ubuntu Pro is available for free on up to 5 machines (for 
business or personal use). Although the compliance and certification 
features of Ubuntu Pro are likely to be of more interest to enterprise
users, the enhanced security coverage is great for anyone using Ubuntu.

All of the Ubuntu Pro features can be managed on the command line via the
[Ubuntu Pro Client](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/)
utility, which has an API that provides easier automation to users.

### Vulnerability management

In a standard Ubuntu LTS release, security support is provided for packages in
the [Main repository](https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/#components)
for 5 years. This service, known as Expanded Security Maintenance ({term}`ESM`), 
is recommended for every Ubuntu system. Learn more [about ESM here](https://ubuntu.com/security/esm).

When you are using Ubuntu Pro, the ESM level of support is expanded 
to 10 years, and also includes patching for medium, high and critival severity
[vulnerabilities](https://ubuntu.com/security/cves/about) for the Universe
repository.

### Kernel application hardening

We also recommend that you use Canonical's Livepatch service for 
every Ubuntu system, which applies kernel patches for high and 
critical severity vulnerabilities while the system is running without 
the need for an immediate reboot -- which reduces downtime. Learn more
[about Livepatch here](https://ubuntu.com/security/livepatch).

### Security Compliance and Certification

For enterprise users who must ensure compliance with specific standards, such as
[FIPS](https://ubuntu.com/security/certifications/docs/fips),
[CIS](https://ubuntu.com/security/certifications/docs/usg) and
[DISA STIG](https://ubuntu.com/security/certifications/docs/disa-stig), Ubuntu
also provides profile benchmarking. See our
[security and compliance documentation](https://ubuntu.com/security/certifications/docs)
for more details.
 
## Reporting vulnerabilities

If you need to report a security issue, refer to the security
[disclosure policy](https://ubuntu.com/security/disclosure-policy).

