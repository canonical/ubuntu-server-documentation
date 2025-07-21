(ldap-replication)=
# OpenLDAP replication

The LDAP service becomes increasingly important as more networked systems begin to depend on it. In such an environment, it is standard practice to build redundancy ({term}`high availability <HA>`) into LDAP to prevent disruption should the LDAP server become unresponsive. This is done through **LDAP replication**.

Replication is achieved via the Sync replication engine, **syncrepl**. This allows changes to be synchronised using a *Consumer - Provider* model. A detailed description of this replication mechanism can be found in the [OpenLDAP administrator's guide](https://openldap.org/doc/admin24/guide.html#LDAP%20Sync%20Replication) and in its defining [RFC 4533](http://www.rfc-editor.org/rfc/rfc4533.txt).

There are two ways to use this replication:

- **Standard replication**: Changed entries are sent to the consumer in their entirety. For example, if the `userPassword` attribute of the `uid=john,ou=people,dc=example,dc=com` entry changed, then the whole entry is sent to the consumer.

- **Delta replication**: Only the actual change is sent, instead of the whole entry.

The delta replication sends less data over the network, but is more complex to set up. We will show both in this guide.

```{important}
You **must** have Transport Layer Security (TLS) enabled already before proceeding with this guide. Please consult the [LDAP with TLS guide](ldap-and-tls.md) for details of how to set this up.
```

## Provider configuration - replication user

Both replication strategies will need a replication user, as well as updates to the {term}`ACL`s and limits regarding this user. To create the replication user, save the following contents to a file called `replicator.ldif`:

```text
dn: cn=replicator,dc=example,dc=com
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: replicator
description: Replication user
userPassword: {CRYPT}x
```

Then add it with `ldapadd`:

```bash
$ ldapadd -x -ZZ -H ldap://ldap01.example.com -D cn=admin,dc=example,dc=com -W -f replicator.ldif
Enter LDAP Password:
adding new entry "cn=replicator,dc=example,dc=com"
```

Now set a password for it with `ldappasswd`:

```bash
$ ldappasswd -x -ZZ -H ldap://ldap01.example.com -D cn=admin,dc=example,dc=com -W -S cn=replicator,dc=example,dc=com
New password:
Re-enter new password:
Enter LDAP Password:
```

```{note}
Please adjust the server URI in the `-H` parameter if needed to match your deployment.
```

The next step is to give this replication user the correct privileges, i.e.:

- Read access to the content that we want replicated
- No search limits on this content

For that we need to update the ACLs on the provider. Since ordering matters, first check what the existing ACLs look like on the `dc=example,dc=com` tree:

```bash
$ sudo ldapsearch -Q -Y EXTERNAL -H ldapi:/// -LLL -b cn=config '(olcSuffix=dc=example,dc=com)' olcAccess
dn: olcDatabase={1}mdb,cn=config
olcAccess: {0}to attrs=userPassword by self write by anonymous auth by * none
olcAccess: {1}to attrs=shadowLastChange by self write by * read
olcAccess: {2}to * by * read
```

What we need is to insert a new rule before the first one, and also adjust the limits for the replicator user. Prepare the `replicator-acl-limits.ldif` file with this content:

```text
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcAccess
olcAccess: {0}to *
  by dn.exact="cn=replicator,dc=example,dc=com" read
  by * break
-
add: olcLimits
olcLimits: dn.exact="cn=replicator,dc=example,dc=com"
  time.soft=unlimited time.hard=unlimited
  size.soft=unlimited size.hard=unlimited
```

And add it to the server:

```bash
$ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f replicator-acl-limits.ldif
modifying entry "olcDatabase={1}mdb,cn=config"
```

## Provider configuration - standard replication

The remaining configuration for the provider using standard replication is to add the `syncprov` overlay on top of the `dc=example,dc=com` database.

Create a file called `provider_simple_sync.ldif` with this content:

```text
# Add indexes to the frontend db.
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: entryCSN eq
-
add: olcDbIndex
olcDbIndex: entryUUID eq

#Load the syncprov module.
dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: syncprov

# syncrepl Provider for primary db
dn: olcOverlay=syncprov,olcDatabase={1}mdb,cn=config
changetype: add
objectClass: olcOverlayConfig
objectClass: olcSyncProvConfig
olcOverlay: syncprov
olcSpCheckpoint: 100 10
olcSpSessionLog: 100
```

```{warning}
The LDIF above has some parameters that you should review before deploying in production on your directory. In particular -- `olcSpCheckpoint` and `olcSpSessionLog`.
Please see the {manpage}`slapo-syncprov(5)` manual page. In general, `olcSpSessionLog` should be equal to (or preferably larger than) the number of entries in your directory. Also see [ITS #8125](https://www.openldap.org/its/index.cgi/?findid=8125) for details on an existing bug.
```

Add the new content:

```bash
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f provider_simple_sync.ldif
```

The Provider is now configured.

## Consumer configuration - standard replication

Install the software by going through [the installation steps](install-openldap.md). Make sure schemas and the database suffix are the same, and [enable TLS](ldap-and-tls.md).

Create an LDIF file with the following contents and name it `consumer_simple_sync.ldif`:

```text
dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: syncprov

dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: entryUUID eq
-
add: olcSyncrepl
olcSyncrepl: rid=0
  provider=ldap://ldap01.example.com
  bindmethod=simple
  binddn="cn=replicator,dc=example,dc=com" credentials=<secret>
  searchbase="dc=example,dc=com"
  schemachecking=on
  type=refreshAndPersist retry="60 +"
  starttls=critical tls_reqcert=demand
-
add: olcUpdateRef
olcUpdateRef: ldap://ldap01.example.com
```

Ensure the following attributes have the correct values:

- **`provider`**: Provider server's {term}`hostname` -- `ldap01.example.com` in this example -- or IP address. It must match what is presented in the provider's SSL certificate.
- **`binddn`**: The bind {term}`DN` for the replicator user.
- **`credentials`**: The password you selected for the replicator user.
- **`searchbase`**: The database suffix you're using, i.e., content that is to be replicated.
- **`olcUpdateRef`**: Provider server's hostname or IP address, given to clients if they try to write to this consumer.
- **`rid`**: Replica ID, a unique 3-digit ID that identifies the replica. Each consumer should have at least one `rid`.

```{note}
A successful encrypted connection via `START_TLS` is being enforced in this configuration, to avoid sending the credentials in the clear across the network. See [LDAP with TLS](ldap-and-tls.md/) for details on how to set up OpenLDAP with trusted SSL certificates.
```

Add the new configuration:

```bash
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f consumer_simple_sync.ldif
```

Now you're done! The `dc=example,dc=com` tree should now be synchronising.

## Provider configuration - delta replication

The remaining provider configuration for delta replication is:

- Create a new database called `accesslog`
- Add the `syncprov` overlay on top of the `accesslog` and `dc=example,dc=com` databases
- Add the `accesslog` overlay on top of the `dc=example,dc=com` database

### Add `syncprov` and `accesslog` overlays and DBs

Create an LDIF file with the following contents and name it `provider_sync.ldif`:

```text
# Add indexes to the frontend db.
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: entryCSN eq
-
add: olcDbIndex
olcDbIndex: entryUUID eq
    
#Load the syncprov and accesslog modules.
dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: syncprov
-
add: olcModuleLoad
olcModuleLoad: accesslog
    
# Accesslog database definitions
dn: olcDatabase={2}mdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcMdbConfig
olcDatabase: {2}mdb
olcDbDirectory: /var/lib/ldap/accesslog
olcSuffix: cn=accesslog
olcRootDN: cn=admin,dc=example,dc=com
olcDbIndex: default eq
olcDbIndex: entryCSN,objectClass,reqEnd,reqResult,reqStart
olcAccess: {0}to * by dn.exact="cn=replicator,dc=example,dc=com" read by * break
olcLimits: dn.exact="cn=replicator,dc=example,dc=com"
  time.soft=unlimited time.hard=unlimited
  size.soft=unlimited size.hard=unlimited
    
# Accesslog db syncprov.
dn: olcOverlay=syncprov,olcDatabase={2}mdb,cn=config
changetype: add
objectClass: olcOverlayConfig
objectClass: olcSyncProvConfig
olcOverlay: syncprov
olcSpNoPresent: TRUE
olcSpReloadHint: TRUE
    
# syncrepl Provider for primary db
dn: olcOverlay=syncprov,olcDatabase={1}mdb,cn=config
changetype: add
objectClass: olcOverlayConfig
objectClass: olcSyncProvConfig
olcOverlay: syncprov
olcSpCheckpoint: 100 10
olcSpSessionLog: 100
    
# accesslog overlay definitions for primary db
dn: olcOverlay=accesslog,olcDatabase={1}mdb,cn=config
objectClass: olcOverlayConfig
objectClass: olcAccessLogConfig
olcOverlay: accesslog
olcAccessLogDB: cn=accesslog
olcAccessLogOps: writes
olcAccessLogSuccess: TRUE
# scan the accesslog DB every day, and purge entries older than 7 days
olcAccessLogPurge: 07+00:00 01+00:00
```

```{warning}
The LDIF above has some parameters that you should review before deploying in production on your directory. In particular -- `olcSpCheckpoint`, `olcSpSessionLog`.
Please see the {manpage}`slapo-syncprov(5)` manpage. In general, `olcSpSessionLog` should be equal to (or preferably larger than) the number of entries in your directory. Also see [ITS #8125](https://www.openldap.org/its/index.cgi/?findid=8125) for details on an existing bug.
For `olcAccessLogPurge`, please check the {manpage}`slapo-accesslog(5)` manpage.
```

Create a directory:

```bash
sudo -u openldap mkdir /var/lib/ldap/accesslog
```

Add the new content:

```bash
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f provider_sync.ldif
```

The Provider is now configured.

## Consumer configuration

Install the software by going through [the installation steps](install-openldap.md). Make sure schemas and the database suffix are the same, and [enable TLS](ldap-and-tls.md).

Create an LDIF file with the following contents and name it `consumer_sync.ldif`:

```text
dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: syncprov
    
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: entryUUID eq
-
add: olcSyncrepl
olcSyncrepl: rid=0
  provider=ldap://ldap01.example.com
  bindmethod=simple
  binddn="cn=replicator,dc=example,dc=com" credentials=<secret>
  searchbase="dc=example,dc=com"
  logbase="cn=accesslog"
  logfilter="(&(objectClass=auditWriteObject)(reqResult=0))"
  schemachecking=on
  type=refreshAndPersist retry="60 +"
  syncdata=accesslog
  starttls=critical tls_reqcert=demand
-
add: olcUpdateRef
olcUpdateRef: ldap://ldap01.example.com
```

Ensure the following attributes have the correct values:

- **`provider`**: Provider server's hostname -- `ldap01.example.com` in this example -- or IP address. It must match what is presented in the provider's SSL certificate.
- **`binddn`**: The bind DN for the replicator user.
- **`credentials`**: The password you selected for the replicator user.
- **`searchbase`**: The database suffix you're using, i.e., content that is to be replicated.
- **`olcUpdateRef`**: Provider server's hostname or IP address, given to clients if they try to write to this consumer.
- **rid**: Replica ID, a unique 3-digit ID that identifies the replica. Each consumer should have at least one `rid`.

```{note}
Note that a successful encrypted connection via `START_TLS` is being enforced in this configuration, to avoid sending the credentials in the clear across the network. See [LDAP with TLS](ldap-and-tls.md/) for details on how to set up OpenLDAP with trusted SSL certificates.
```

Add the new configuration:

```bash
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f consumer_sync.ldif
```

You're done! The `dc=example,dc=com` tree should now be synchronising.

## Testing

Once replication starts, you can monitor it by running:

```bash
$ ldapsearch -z1 -LLL -x -s base -b dc=example,dc=com contextCSN
dn: dc=example,dc=com
contextCSN: 20200423222317.722667Z#000000#000#000000
```

On both the provider and the consumer. Once the `contextCSN` value for both match, both trees are in sync. Every time a change is done in the provider, this value will change and so should the one in the consumer(s).

If your connection is slow and/or your LDAP database large, it might take a while for the consumer's `contextCSN` match the provider's. But, you will know it is progressing since the consumer's `contextCSN` will be steadily increasing.

If the consumer's `contextCSN` is missing or does not match the provider, you should stop and figure out the issue before continuing. Try checking the `slapd` entries in `/var/log/syslog` in the provider to see if the consumer's authentication requests were successful, or that its requests to retrieve data return no errors. In particular, verify that you can connect to the provider from the consumer as the replicator BindDN using `START_TLS`:

```bash
ldapwhoami -x -ZZ -H ldap://ldap01.example.com -D cn=replicator,dc=example,dc=com -W
```

For our example, you should now see the `john` user in the replicated tree:

```bash
$ ldapsearch -x -LLL -H ldap://ldap02.example.com -b dc=example,dc=com '(uid=john)' uid
dn: uid=john,ou=People,dc=example,dc=com
uid: john
```

## References

  - [Replication types, OpenLDAP Administrator's Guide](https://openldap.org/doc/admin24/guide.html#Configuring%20the%20different%20replication%20types)
  - [LDAP Sync Replication - OpenLDAP Administrator's Guide](https://openldap.org/doc/admin24/guide.html#LDAP%20Sync%20Replication)
  - [RFC 4533](http://www.rfc-editor.org/rfc/rfc4533.txt).
