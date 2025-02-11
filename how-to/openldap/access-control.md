(ldap-access-control)=
# Set up LDAP access control


The management of what type of access (read, write, etc) users should be granted for resources is known as **access control**. The configuration directives involved are called **access control lists** or {term}`ACL`s.

When we {ref}`installed the slapd package <install-openldap>`, various ACLs were set up automatically. We will look at a few important consequences of those defaults and, in so doing, we'll get an idea of how ACLs work and how they're configured.

To get the effective ACL for an LDAP query we need to look at the ACL entries of both the database being queried, and those of the special frontend database instance. Note that the ACLs belonging to the frontend database are always appended to the database-specific ACLs, and the first match 'wins'.

## Getting the ACLs

The following commands will give, respectively, the ACLs of the `mdb` database (`dc=example,dc=com`) and those of the frontend database:

```bash
$ sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b \
cn=config '(olcDatabase={1}mdb)' olcAccess
    
dn: olcDatabase={1}mdb,cn=config
olcAccess: {0}to attrs=userPassword by self write by anonymous auth by * none
olcAccess: {1}to attrs=shadowLastChange by self write by * read
olcAccess: {2}to * by * read

$ sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b \
cn=config '(olcDatabase={-1}frontend)' olcAccess
    
dn: olcDatabase={-1}frontend,cn=config
olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external
 ,cn=auth manage by * break
olcAccess: {1}to dn.exact="" by * read
olcAccess: {2}to dn.base="cn=Subschema" by * read
```

> **Note**:
> The Root DN always has full rights to its database and does not need to be included in any ACL.

## Interpreting the results

The first two ACLs are crucial:

```text
olcAccess: {0}to attrs=userPassword by self write by anonymous auth by * none
olcAccess: {1}to attrs=shadowLastChange by self write by * read
```

This can be represented differently for easier reading:

```text
to attrs=userPassword
    by self write
    by anonymous auth
    by * none
    
to attrs=shadowLastChange
    by self write
    by * read
```

These ACLs enforce the following:

- Anonymous 'auth' access is provided to the **userPassword** attribute so that users can authenticate, or **bind**. Perhaps counter-intuitively, 'by anonymous auth' is needed even when anonymous access to the DIT is unwanted, otherwise this would be a chicken-and-egg problem: before authentication, all users are anonymous.

- The 'by self write' ACL grants write access to the **userPassword** attribute to users who authenticated as the DN where the attribute lives. In other words, users can update the **userPassword** attribute of their own entries.

- The **userPassword** attribute is otherwise inaccessible by all other users, with the exception of the Root DN, who always has access and doesn't need to be mentioned explicitly.

- In order for users to change their own password, using `passwd` or other utilities, the user's own **shadowLastChange** attribute needs to be writable. All other directory users get to read this attribute's contents.

This DIT can be searched anonymously because of `to * by * read` in this ACL, which grants read access to everything else, by anyone (including anonymous):

```text
to *
    by * read
```

If this is unwanted then you need to change the ACL. To force authentication during a bind request you can alternatively (or in combination with the modified ACL) use the `olcRequire: authc` directive.

## SASL identity

There is no administrative account ("Root DN") created for the `slapd-config` database. There is, however, a SASL identity that is granted full access to it. It represents the localhost's superuser (`root`/`sudo`). Here it is:

```text
dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth 
```

The following command will display the ACLs of the `slapd-config` database:

```bash
$ sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b \
cn=config '(olcDatabase={0}config)' olcAccess
    
dn: olcDatabase={0}config,cn=config
olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,
              cn=external,cn=auth manage by * break
```

Since this is a SASL identity we need to use a SASL **mechanism** when invoking the LDAP utility in question -- the **EXTERNAL** mechanism (see the previous command for an example). Note that:

- You must use `sudo` to become the root identity in order for the ACL to match.

- The EXTERNAL mechanism works via **Interprocess Communication** (IPC, UNIX domain sockets). This means you must use the `ldapi` URI format.

A succinct way to get all the ACLs is like this:

```bash
$ sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b \
cn=config '(olcAccess=*)' olcAccess olcSuffix
```

## Next steps

See how to {ref}`set up LDAP users and groups <ldap-users-and-groups>`.

## Further reading

- See the man page for [slapd.access](http://manpages.ubuntu.com/manpages/slapd.access.html).
- The [access control topic](https://openldap.org/doc/admin25/guide.html#Access%20Control) in the OpenLDAP administrator's guide.
