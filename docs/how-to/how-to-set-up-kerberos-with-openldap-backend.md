(how-to-set-up-kerberos-with-openldap-backend)=
# How to set up Kerberos with OpenLDAP backend

Kerberos supports a few different database backends. The default one (which we have used in our other Kerberos guides so far) is called `db2`. The [DB types documentation](https://web.mit.edu/kerberos/krb5-latest/doc/admin/dbtypes.html) shows all the options, one of which is LDAP.

## Why use LDAP?

There are several reasons why one would want to have the Kerberos principals stored in LDAP as opposed to a local on-disk database. There are also cases when it is not a good idea. Each site has to evaluate the pros and cons. Here are a few:

- Pros:
  - OpenLDAP replication is faster and more robust than the native Kerberos one, based on a cron job
  - If you already have OpenLDAP set up for other things, such as storing users and groups, adding the Kerberos attributes can be beneficial, providing an integrated story
- Cons:
  - Setting up the LDAP backend isn't a trivial task and shouldn't be attempted by administrators without prior knowledge of OpenLDAP
  - As highlighted in the [LDAP section of DB types](https://web.mit.edu/kerberos/krb5-latest/doc/admin/dbtypes.html#ldap-module-kldap), since `krb5kdc` is single-threaded there may be higher latency in servicing requests when using the OpenLDAP backend

## In this guide

In this section we'll configure a primary and secondary Kerberos server to use OpenLDAP for the principal database. Note that as of version 1.18, the Key Distribution Center (KDC) from MIT Kerberos [does not support](https://krbdev.mit.edu/rt/Ticket/Display.html?id=7754#) a primary KDC using a read-only consumer (secondary) LDAP server. What we have to consider here is that a primary KDC is read-write, and it needs a read-write backend. The secondary KDCs can use both a read-write and read-only backend, because they are expected to be read-only. Therefore there are only some possible layouts we can use:

1. **Simple case**:
   - Primary KDC connected to primary OpenLDAP
   - Secondary KDC connected to both primary and secondary OpenLDAP
1. **Extended simple case**:
   - Multiple primary KDCs connected to one primary OpenLDAP
   - Multiple secondary KDCs connected to primary and secondary OpenLDAP
1. **OpenLDAP with multi-master replication**:
   - Multiple primary KDCs connected to all primary OpenLDAP servers

We haven't covered OpenLDAP multi-master replication in this guide, so we will show the **simple case** only. The second scenario is an extension: just add another primary KDC to the mix, talking to the same primary OpenLDAP server.

## Configure OpenLDAP

We are going to install the OpenLDAP server on the same host as the KDC, to simplify the communication between them. In such a setup, we can use the `ldapi:///` transport, which is via a UNIX socket, and we don't need to set up SSL certificates to secure the communication between the Kerberos services and OpenLDAP. Note, however, that SSL is still needed for the OpenLDAP replication. See [LDAP with TLS](ldap-and-transport-layer-security-tls.md) for details.

If you want to use an existing OpenLDAP server, that's also possible, but keep in mind that you should then use SSL for the communication between the KDC and this OpenLDAP server.

First, the necessary **schema** needs to be loaded on an OpenLDAP server that has network connectivity to both the **primary** and **secondary** KDCs. The rest of this section assumes that you also have LDAP replication configured between at least two servers. For information on setting up OpenLDAP see [OpenLDAP Server](install-and-configure-ldap.md).

> **Note**:
> `cn=admin,dc=example,dc=com` is a default admin user that is created during the installation of the `slapd` package (the OpenLDAP server). The domain component will change for your server, so adjust accordingly.

- Install the necessary packages (it's assumed that OpenLDAP is already installed):
   
  ```bash 
  sudo apt install krb5-kdc-ldap krb5-admin-server
  ```

- Next, extract the `kerberos.schema.gz` file:

  ```bash
  sudo cp /usr/share/doc/krb5-kdc-ldap/kerberos.schema.gz /etc/ldap/schema/
  sudo gunzip /etc/ldap/schema/kerberos.schema.gz
  ```

- The **Kerberos schema** needs to be added to the `cn=config` tree. This schema file needs to be converted to LDIF format before it can be added. For that we will use a helper tool, called `schema2ldif`, provided by the package of the same name which is available in the Universe archive:

  ```bash
  sudo apt install schema2ldif
  ```

- To import the Kerberos schema, run:

  ```bash
  $ sudo ldap-schema-manager -i kerberos.schema
  SASL/EXTERNAL authentication started
  SASL username: gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth
  SASL SSF: 0
  executing 'ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/kerberos.ldif'
  SASL/EXTERNAL authentication started
  SASL username: gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth
  SASL SSF: 0
  adding new entry "cn=kerberos,cn=schema,cn=config"
  ```

- With the new schema loaded, let's index an attribute often used in searches:
  ```bash
  $ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// <<EOF
  dn: olcDatabase={1}mdb,cn=config
  add: olcDbIndex
  olcDbIndex: krbPrincipalName eq,pres,sub
  EOF

  modifying entry "olcDatabase={1}mdb,cn=config"
  ```

- Let's create LDAP entries for the Kerberos administrative entities that will contact the OpenLDAP server to perform operations. There are two:
  - **`ldap_kdc_dn`**: needs to have read rights on the realm container, principal container and realm sub-trees. If **`disable_last_success`** and **`disable_lockout`** are not set, however, then **`ldap_kdc_dn`** needs write access to the Kerberos container just like the admin DN below.
  - **`ldap_kadmind_dn`**: needs to have read and write rights on the realm container, principal container and realm sub-trees

  Here is the command to create these entities:
  ```bash
  $ ldapadd -x -D cn=admin,dc=example,dc=com -W <<EOF
  dn: uid=kdc-service,dc=example,dc=com
  uid: kdc-service
  objectClass: account
  objectClass: simpleSecurityObject
  userPassword: {CRYPT}x
  description: Account used for the Kerberos KDC

  dn: uid=kadmin-service,dc=example,dc=com
  uid: kadmin-service
  objectClass: account
  objectClass: simpleSecurityObject
  userPassword: {CRYPT}x
  description: Account used for the Kerberos Admin server
  EOF
  Enter LDAP Password: 
  adding new entry "uid=kdc-service,dc=example,dc=com"

  adding new entry "uid=kadmin-service,dc=example,dc=com"
  ```

  Now let's set a password for them. Note that first the tool asks for the password you want for the specified user DN, and then for the password of the **`cn=admin`** DN:

  ```bash
  $ ldappasswd -x -D cn=admin,dc=example,dc=com -W -S uid=kdc-service,dc=example,dc=com
  New password:   <-- password you want for uid-kdc-service 
  Re-enter new password: 
  Enter LDAP Password:  <-- password for the dn specified with the -D option
  ```

  Repeat for the `uid=kadmin-service` dn. These passwords will be needed later.

  You can test these with `ldapwhoami`:

  ```bash
  $ ldapwhoami -x -D uid=kdc-service,dc=example,dc=com -W
  Enter LDAP Password: 
  dn:uid=kdc-service,dc=example,dc=com
  ```
      
- Finally, update the Access Control Lists (ACL). These can be tricky, as it highly depends on what you have defined already. By default, the `slapd` package configures your database with the following ACLs:

  ```text
  olcAccess: {0}to attrs=userPassword by self write by anonymous auth by * none
  olcAccess: {1}to attrs=shadowLastChange by self write by * read
  olcAccess: {2}to * by * read
  ```

  We need to insert new rules before the final `to * by * read` one, to control access to the Kerberos related entries and attributes:

  ```bash
  $ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// <<EOF
  dn: olcDatabase={1}mdb,cn=config
  add: olcAccess
  olcAccess: {2}to attrs=krbPrincipalKey
    by anonymous auth
    by dn.exact="uid=kdc-service,dc=example,dc=com" read
    by dn.exact="uid=kadmin-service,dc=example,dc=com" write
    by self write
    by * none
  -
  add: olcAccess
  olcAccess: {3}to dn.subtree="cn=krbContainer,dc=example,dc=com"
    by dn.exact="uid=kdc-service,dc=example,dc=com" read
    by dn.exact="uid=kadmin-service,dc=example,dc=com" write
    by * none
  EOF

  modifying entry "olcDatabase={1}mdb,cn=config"

  This will make the existing {2} rule become {4}. Check with sudo slapcat -b cn=config (the output below was reformatted a bit for clarity):

  olcAccess: {0}to attrs=userPassword
	  by self write
	  by anonymous auth
	  by * none
  olcAccess: {1}to attrs=shadowLastChange
	  by self write
	  by * read
  olcAccess: {2}to attrs=krbPrincipalKey by anonymous auth
  	by dn.exact="uid=kdc-service,dc=example,dc=com" read
  	by dn.exact="uid=kadmin-service,dc=example,dc=com" write
  	by self write
  	by * none
  olcAccess: {3}to dn.subtree="cn=krbContainer,dc=example,dc=com"
  	by dn.exact="uid=kdc-service,dc=example,dc=com" read
  	by dn.exact="uid=kadmin-service,dc=example,dc=com" write
  	by * none
  olcAccess: {4}to * by * read

    ```

Your LDAP directory is now ready to serve as a Kerberos principal database.

## Primary KDC configuration (LDAP)

With OpenLDAP configured it is time to configure the KDC. In this example we are doing it in the same OpenLDAP server to take advantage of local UNIX socket communication.

- Reconfigure the `krb5-config` package if needed to get a good starting point with `/etc/krb5.conf`:
  
  ```bash   
  sudo dpkg-reconfigure krb5-config
  ```

- Now edit `/etc/krb5.conf` adding the `database_module` option to the `EXAMPLE.COM` realm section:

  ```text    
  [realms]
          EXAMPLE.COM = {
                  kdc = kdc01.example.com
                  kdc = kdc02.example.com
                  admin_server = kdc01.example.com
                  default_domain = example.com
                  database_module = openldap_ldapconf
          }
  ```
  Then also add these new sections:

  ```text
  [dbdefaults]
          ldap_kerberos_container_dn = cn=krbContainer,dc=example,dc=com

  [dbmodules]
          openldap_ldapconf = {
                  db_library = kldap

  				# if either of these is false, then the ldap_kdc_dn needs to
  				# have write access
  				disable_last_success = true
  				disable_lockout  = true

                  # this object needs to have read rights on
                  # the realm container, principal container and realm sub-trees
                  ldap_kdc_dn = "uid=kdc-service,dc=example,dc=com"

                  # this object needs to have read and write rights on
                  # the realm container, principal container and realm sub-trees
                  ldap_kadmind_dn = "uid=kadmin-service,dc=example,dc=com"

                  ldap_service_password_file = /etc/krb5kdc/service.keyfile
                  ldap_servers = ldapi:///
                  ldap_conns_per_server = 5
          }
  ```

- Next, use the `kdb5_ldap_util` utility to create the realm:

  ```bash
  $ sudo kdb5_ldap_util -D cn=admin,dc=example,dc=com create -subtrees dc=example,dc=com -r EXAMPLE.COM -s -H ldapi:///
  Password for "cn=admin,dc=example,dc=com": 
  Initializing database for realm 'EXAMPLE.COM'
  You will be prompted for the database Master Password.
  It is important that you NOT FORGET this password.
  Enter KDC database master key: 
  Re-enter KDC database master key to verify: 
  ```

- Create a stash of the password used to bind to the LDAP server. Run it once for each `ldap_kdc_dn` and `ldap_kadmin_dn`:

  ```bash    
  sudo kdb5_ldap_util -D cn=admin,dc=example,dc=com stashsrvpw -f /etc/krb5kdc/service.keyfile uid=kdc-service,dc=example,dc=com
  sudo kdb5_ldap_util -D cn=admin,dc=example,dc=com stashsrvpw -f /etc/krb5kdc/service.keyfile uid=kadmin-service,dc=example,dc=com
  ```

  > **Note**:
  > The `/etc/krb5kdc/service.keyfile` file now contains clear text versions of the passwords used by the KDC to contact the LDAP server!

- Create a `/etc/krb5kdc/kadm5.acl` file for the admin server, if you haven't already:

  ```text
  */admin@EXAMPLE.COM        *
  ```

- Start the Kerberos KDC and admin server:

  ```bash    
  sudo systemctl start krb5-kdc.service krb5-admin-server.service
  ```

You can now add Kerberos principals to the LDAP database, and they will be copied to any other LDAP servers configured for replication. To add a principal using the `kadmin.local` utility enter:

```bash
$ sudo kadmin.local
Authenticating as principal root/admin@EXAMPLE.COM with password.
kadmin.local:  addprinc ubuntu
WARNING: no policy specified for ubuntu@EXAMPLE.COM; defaulting to no policy
Enter password for principal "ubuntu@EXAMPLE.COM": 
Re-enter password for principal "ubuntu@EXAMPLE.COM": 
Principal "ubuntu@EXAMPLE.COM" created.
kadmin.local:  
```

The above will create an `ubuntu` principal with a DN of `krbPrincipalName=ubuntu@EXAMPLE.COM,cn=EXAMPLE.COM,cn=krbContainer,dc=example,dc=com`.

Let's say, however, that you already have a user in your directory, and it's in `uid=testuser1,ou=People,dc=example,dc=com`. How can you add the Kerberos attributes to it? You use the `-x` parameter to specify the location. For the `ldap_kadmin_dn` to be able to write to it, we first need to update the ACLs:

```bash
$ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// <<EOF
dn: olcDatabase={1}mdb,cn=config
add: olcAccess
olcAccess: {4}to dn.subtree=“ou=People,dc=example,dc=com”
    by dn.exact=”uid=kdc-service,dc=example,dc=com” read
    by dn.exact=”uid=kadmin-service,dc=example,dc=com” write
    by * break
EOF
```

And now we can specify the new location:

```bash
$ sudo kadmin.local
Authenticating as principal root/admin@EXAMPLE.COM with password.
kadmin.local:  addprinc -x dn=uid=testuser1,ou=People,dc=example,dc=com testuser1
WARNING: no policy specified for testuser1@EXAMPLE.COM; defaulting to no policy
Enter password for principal "testuser1@EXAMPLE.COM": 
Re-enter password for principal "testuser1@EXAMPLE.COM": 
Principal "testuser1@EXAMPLE.COM" created.
```

Since the specified DN already exists, `kadmin.local` will just add the required Kerberos attributes to this existing entry. If it didn't exist, it would be created from scratch, with only the Kerberos attributes, just like what happened with the `ubuntu` example above, but in the specified location.

> **Note**:
> The `ldap_kadmin_dn` DN (`uid=kadmin-service` in our example) does not have write access to the location specified by the `-x` parameter, you will get an `Insufficient access` error.

Both places are visible for `kinit`, since, when the realm was created with `kdb5_ldap_util`, the default value for the search scope and base were taken: `subtree`, and `dc=example,dc=com`.

## Secondary KDC configuration (LDAP)

The setup of the secondary KDC (and its OpenLDAP replica) is very similar. Once you have the OpenLDAP replication setup, repeat these steps on the secondary:

- Install `krb5-kdc-ldap`, `ldap-utils`. Do **not** install `krb5-admin-server`.
- Load the Kerberos schema using `schema2ldif`.
- Add the index for `krbPrincipalName`.
- Add the ACLs.
- Configure `krb5.conf` in the same way, initially. If you want to, and if you configured SSL properly, you can add `ldaps://kdc01.example.com` to the `ldap_servers` list after `ldapi:///`, so that the secondary KDC can have two LDAP backends at its disposal.
- **DO NOT** run `kdb5_ldap_util`. There is no need to create the database since it's being replicated from the primary.
- Copy over the following files from the primary KDC and place them in the same location on the secondary:
  - `/etc/krb5kdc/stash`
  - `/etc/krb5kdc/service.keyfile`
- Start the KDC: `sudo systemctl start krb5-kdc.service`

## Resources

- [Configuring Kerberos with OpenLDAP back-end](https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_ldap.html#conf-ldap)

- [MIT Kerberos backend types](https://web.mit.edu/kerberos/krb5-latest/doc/admin/dbtypes.html)
