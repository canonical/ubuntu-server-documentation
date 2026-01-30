---
myst:
  html_meta:
    description: Install and configure Kerberos authentication on Ubuntu Server including KDC setup, service principals, and OpenLDAP backend integration.
---

(how-to-kerberos)=
# Kerberos

This section assumes you have some familiarity with the terms and concepts used in Kerberos.

You will need a properly configured DNS server set up before you begin. See the {ref}`install-dns` page for instructions on how to set this up.

We recommend following this set of how-to guides in the order presented for best results.

```{toctree}
:titlesonly:

Install a Kerberos server <kerberos/install-a-kerberos-server>
Configure service principals <kerberos/configure-service-principals>
Kerberos encryption types <kerberos/kerberos-encryption-types>
Set up secondary KDC <kerberos/set-up-secondary-kdc>
Basic workstation authentication <kerberos/basic-workstation-authentication>
Kerberos with OpenLDAP backend <kerberos/kerberos-with-openldap-backend>
```
    
## See also

* Explanation: {ref}`introduction-to-kerberos`
