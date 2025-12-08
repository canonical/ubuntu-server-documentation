(introduction-to-security)=
# Introduction to security

Security should always be considered when you install, deploy, and use an
Ubuntu system. While a fresh installation of Ubuntu is usually safe for
immediate use, your system's security posture will be very important depending
on how it is used after it is deployed. You should always employ a layered
approach to security so that that your system does not rely on a single
point of defense.

## Server security guidance

Given Ubuntu has a wide range of customization options, this introduction cannot 
provide a comprehensive security hardening guide. However, the security of nearly any 
Ubuntu system can be enhanced by implementing certain best practices and security-related 
packages. Our {ref}`security suggestions <security-suggestions>` page outlines those best 
practices and packages. While you may not choose to implement every suggestion -- and 
this list is not exhaustive -- each one can contribute an additional layer of security.

If your Ubuntu setup is more advanced or more complex than others, you may 
need to do more research into your security outlook. There are specific 
packages available for Ubuntu Servers that can provide additional security, and
we suggest some packages in the {ref}`advanced security <advanced-security>` 
section that you might want to investigate. Again, the list in this section
is not intended to be exhaustive, but rather a starting point.

For the most thorough treatment of security in Ubuntu, we also recommend reading the [Ubuntu Security documentation](https://ubuntu.com/security).


## Ubuntu Pro

Canonical offers security, compliance and support services through the
[Ubuntu Pro](https://ubuntu.com/pro) subscription. Ubuntu Pro is available
for free on up to 5 machines (for business or personal use). Although the
compliance and certification features of Ubuntu Pro are likely to be of more
interest to enterprise users, the enhanced security coverage is great for
anyone using Ubuntu.

All of the Ubuntu Pro features can be managed on the command line via the
[Ubuntu Pro Client](https://documentation.ubuntu.com/pro-client/en/latest/)
utility, which has an API that provides easier automation to users.

### Vulnerability management

In a standard Ubuntu LTS release, security support is provided 
for packages in the [Main repository](https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/#components)
for 5 years. With Ubuntu Pro, this support is expanded 
to 10 years, and also includes patching for medium, high and critical severity
[vulnerabilities](https://ubuntu.com/security/cves/about) for the Universe
repository. This service, known as Expanded Security Maintenance ({term}`ESM`), is recommended for every Ubuntu system. Learn more
[about ESM here](https://ubuntu.com/security/esm).


### Kernel application hardening

We also recommend Canonical's Livepatch service for 
every Ubuntu system, which applies kernel patches for high and 
critical severity vulnerabilities while the system is running, without 
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

