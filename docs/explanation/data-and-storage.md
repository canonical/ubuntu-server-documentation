---
myst:
  html_meta:
    description: Understanding data management and storage in Ubuntu Server including OpenLDAP directory services, databases, and storage solutions.
---

(explanation-data-and-storage)=
# Data and storage

The following sections provide details on various topics related to storing, managing and accessing data.

## Data management

OpenLDAP is a popular implementation of the Lightweight Directory Access Protocol (LDAP), used for managing hierarchical data. It offers a way to store, organize and manage an organization's data such as employee accounts and computers. It facilitates centralised authentication and authorisation management.

```{toctree}
:titlesonly:

intro-to/openldap
```

Databases are also a common data management tool in any setup.

```{toctree}
:titlesonly:

intro-to/databases
```

## Storage

* Our {ref}`explanation-storage` section contains more detail about LVM and iSCSI
* Our {ref}`explanation-multipath` section explains the key concepts and common configuration setups for Device Mapper Multipathing

```{toctree}
:hidden:

storage
multipath
```

## See also

* How-to: {ref}`how-to-data-and-storage`
* Our {ref}`Backup section <how-to-backups-and-version-control>` discusses various backup strategies to protect your data
