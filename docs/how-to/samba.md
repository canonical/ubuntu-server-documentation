---
myst:
  html_meta:
    description: Configure Samba on Ubuntu Server as an Active Directory Domain Controller, file server, or print server with share access controls.
---

(how-to-samba)=
# Samba

A Samba server can be deployed as a full Active Directory Domain Controller (Samba AD/DC), providing authentication to domain users -- whether Linux or Windows. 

```{toctree}
:titlesonly:

Set up a Samba AD Domain Controller <samba/provision-samba-ad-controller>
Join an Active Directory domain <samba/member-server-in-an-ad-domain>
```

## Set up sharing services

Samba can be configured as a file server or print server, to share files and printers with Windows clients.

```{toctree}
:titlesonly:

Set up a file server <samba/file-server>
Set up a print server <samba/print-server>
```

## Access controls

```{toctree}
:titlesonly:

Share access controls <samba/share-access-controls>
Create AppArmor profile <samba/apparmor-profile>
Mount CIFS shares permanently <samba/mount-cifs-shares-permanently>
```

## Legacy options

These options are now deprecated, but still available. 

```{toctree}
:titlesonly:

NT4 domain controller <samba/nt4-domain-controller-legacy>
OpenLDAP backend <samba/openldap-backend-legacy>
```

## See also

* Explanation: {ref}`introduction-to-samba`
