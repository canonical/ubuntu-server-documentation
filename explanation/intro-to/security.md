(introduction-to-security)=
# Introduction to security

Security should always be considered when installing, deploying, and using any
Ubuntu system. Although a fresh installation of Ubuntu is relatively safe for
immediate use, it is important to have a balanced understanding of your
system's security posture based on how it will be used after deployment. It's
important to take a layered approach so that your system's security is not
dependent on a single point of defense.

## Server security guidance

Since Ubuntu is so endlessly customizable, a full guide to security hardening
is beyond the scope of this documentation.
However, there are good practices and security-related packages that could be
applied to almost any Ubuntu system. See our
{ref}`security suggestions <security-suggestions>` page for an overview of the
good habits and practices that can be adopted by anyone running an Ubuntu
system to make it more secure. It's not necessary to apply every suggestion --
and the list is not exhaustive by any means -- but each one used creates an
extra layer of security.

In a more advanced or complex setup, you may need to go further in your
security outlook. There are specific packages available for your Server
that will help with this, and we suggest some in the
{ref}`advanced security <advanced-security>` section that you might want to
consider for your use-case. Again, the list is not intended to be exhaustive,
but rather a starting point.

For a more thorough treatment of security in Ubuntu, we also recommend checking
out the [Ubuntu Security documentation](https://ubuntu.com/security).

## Ubuntu Pro

Canonical offers security, compliance and support services through the
[Ubuntu Pro](https://ubuntu.com/pro) subscription. Ubuntu Pro is available
for free on up to 5 machines (for business or personal use). Although the
compliance and certification features of Ubuntu Pro are likely to be of more
interest to enterprise users, the enhanced security coverage is great for
anyone using Ubuntu.

All of the Ubuntu Pro features can be managed on the command line via the
[Ubuntu Pro Client](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/)
utility, which also has an API for easier automation.

### Vulnerability management

In a standard Ubuntu LTS release, security support is provided for packages in
the [Main repository](https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/#components)
for 5 years. With Ubuntu Pro, this is expanded to 10 years, and also includes
patching for medium, high and critival severity
[vulnerabilities](https://ubuntu.com/security/cves/about) for the Universe
repository.

This service, known as [Expanded Security Maintenance (ESM)](https://documentation.ubuntu.com/server/reference/glossary/#term-ESM), is recommended for
every Ubuntu system. Learn more [about ESM](https://ubuntu.com/security/esm).

### Kernel application hardening

The second service recommended for every Ubuntu system is Canonical's Livepatch
service, which applies kernel patches for high and critical severity
vulnerabilities while the system is running, and without the need for an
immediate reboot -- reducing downtime. Learn more
[about Livepatch](https://ubuntu.com/security/livepatch).

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

