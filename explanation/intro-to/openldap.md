(introduction-to-openldap)=
# Introduction to OpenLDAP

The Lightweight Directory Access Protocol, or LDAP, is a protocol for querying and modifying an X.500-based directory service running over TCP/IP. The current LDAP version is LDAPv3, as defined in [RFC 4510](http://tools.ietf.org/html/rfc4510), and the implementation used in Ubuntu is OpenLDAP.

The LDAP protocol *accesses* directories. It's common to refer to a directory as an *LDAP directory* or *LDAP database* as a shorthand -- although technically incorrect, this shorthand is so widely used
that it's understood as such. 

## Key concepts and terms

- A **directory** is a tree of data **entries** that is hierarchical in nature; it is called the Directory Information Tree (DIT).

- An **entry** consists of a set of **attributes**.

- An **attribute** has a **key** (a name or description) and one or more **values**. Every attribute must be defined in at least one **`objectClass`**.

- Attributes and `objectClasses` are defined in **schemas** (an `objectClass` is considered a special kind of attribute).

- Each entry has a unique identifier: its **Distinguished Name** (DN or dn). This, in turn, consists of a **Relative Distinguished Name** (RDN) followed by the parent entry's DN.

- The entry's DN is not an attribute. It is not considered part of the entry itself.

> **Note**:
> The terms **object**, **container**, and **node** have certain connotations but they all essentially mean the same thing as **entry** (the technically correct term).

For example, below we have a single entry consisting of 11 attributes where the following is true:

- DN is `cn=John Doe,dc=example,dc=com`

- RDN is `cn=John Doe`

- parent DN is `dc=example,dc=com`

```text
 dn: cn=John Doe,dc=example,dc=com
 cn: John Doe
 givenName: John
 sn: Doe
 telephoneNumber: +1 888 555 6789
 telephoneNumber: +1 888 555 1232
 mail: john@example.com
 manager: cn=Larry Smith,dc=example,dc=com
 objectClass: inetOrgPerson
 objectClass: organizationalPerson
 objectClass: person
 objectClass: top
```

The above entry is in **LDAP Data Interchange Format** format (LDIF). Any information that you feed into your DIT must also be in such a format. It is defined in [RFC 2849](https://datatracker.ietf.org/doc/html/rfc2849).

A directory accessed via LDAP is good for anything that involves a large number of access requests to a mostly-read, attribute-based (name:value) backend, and that can benefit from a hierarchical structure. Examples include an address book, company directory, a list of email addresses, and a mail server's configuration.

## Our OpenLDAP guide

For users who want to set up OpenLDAP, we recommend following our series of guides in this order:

* {ref}`Install and configure LDAP <install-openldap>`
* {ref}`LDAP Access Control <ldap-access-control>`
* {ref}`LDAP users and groups <ldap-users-and-groups>`
* {ref}`SSL/TLS <ldap-and-tls>`
* {ref}`Replication <ldap-replication>`
* {ref}`Backup and restore <ldap-backup-and-restore>`

## References

- The [OpenLDAP administrators guide](https://openldap.org/doc/admin25/)
- [RFC 4515: LDAP string representation of search filters](http://www.rfc-editor.org/rfc/rfc4515.txt)
- Zytrax's [LDAP for Rocket Scientists](http://www.zytrax.com/books/ldap/); a less pedantic but comprehensive treatment of LDAP
Older references that might still be useful:
- O'Reilly's [LDAP System Administration](http://www.oreilly.com/catalog/ldapsa/) (textbook; 2003)
- Packt's [Mastering OpenLDAP](http://www.packtpub.com/OpenLDAP-Developers-Server-Open-Source-Linux/book) (textbook; 2007)
