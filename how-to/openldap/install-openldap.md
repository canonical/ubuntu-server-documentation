(install-openldap)=
# Install and configure LDAP

[Lightweight Directory Access Protocol](https://ldap.com/) (LDAP) is a protocol used for managing hierarchical data. OpenLDAP is the open-source implementation of LDAP used in Ubuntu. For information about OpenLDAP and explanations of the key terminology, see see {ref}`introduction-to-openldap`.

Installing [slapd (the Stand-alone LDAP Daemon)](https://www.openldap.org/software/man.cgi?query=slapd) creates a minimal working configuration with a top level entry, and an administrator's Distinguished Name (DN). 

In particular, it creates a database instance that you can use to store your data. However, the **suffix** (or **base DN**) of this instance will be determined from the domain name of the host. If you want something different, you can change it right after the installation (before it contains any useful data).

```{note}
This guide will use a database suffix of **`dc=example,dc=com`**. You can change this to match your particular setup.
```

## Install slapd

You can install the server and the main command line utilities with the following command:

```console
sudo apt install slapd ldap-utils
```

### Change the instance suffix (optional)

If you want to change your Directory Information Tree ({term}`DIT`) suffix, now would be a good time since changing it discards your existing one. To change the suffix, run the following command:

```console
sudo dpkg-reconfigure slapd
```

To switch your DIT suffix to **`dc=example,dc=com`**, for example, so you can follow this guide more closely, answer `example.com` when asked about the {term}`DNS` domain name.

Throughout this guide we will issue many commands with the LDAP utilities. To save some typing, we can configure the OpenLDAP libraries with certain defaults in `/etc/ldap/ldap.conf` (adjust these entries for your server name and directory suffix):

```text
BASE dc=example,dc=com
URI ldap://ldap01.example.com
```

## Default tree contents

`slapd` is designed to be configured within the service itself by dedicating a separate DIT for that purpose. This allows for dynamic configuration of `slapd` without needing to restart the service or edit config files. This configuration database consists of a collection of text-based LDIF files located under `/etc/ldap/slapd.d`, but these should never be edited directly. This way of working is known by several names: the "slapd-config" method, the "Real Time Configuration (RTC)" method, or the "cn=config" method. You can still use the traditional flat-file method (`slapd.conf`) but that will not be covered in this guide.

Right after installation, you will get two databases, or suffixes: one for your data, which is based on your host's domain (**`dc=example,dc=com`**), and one for your configuration, with its root at **`cn=config`**. To change the data on each we need different credentials and access methods:

- **`dc=example,dc=com`**
The administrative user for this suffix is `cn=admin,dc=example,dc=com` and its password is the one selected during the installation of the `slapd` package.

- **`cn=config`** 
The configuration of `slapd` itself is stored under this suffix. Reading and writing to it can be done by the special {term}`DN` `gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth`. This is how the local system's root user (`uid=0/gid=0`) is seen by the directory when using {term}`SASL` EXTERNAL authentication through the `ldapi:///` transport via the `/run/slapd/ldapi` Unix socket. Essentially what this means is that only the local root user can update the `cn=config` database. More details later.

### Default configuration tree

This is what the `slapd-config` DIT looks like via the LDAP protocol (listing only the DNs):
To see what the `slapd-config` DIT looks like via the LDAP protocol, listing only the DNs, run this command:

```console
sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config dn
```

The command-line options mean the following:

 * `-Q`: Quiet mode for the SASL authentication setup.
 * `-LLL`: Less verbose LDIF output. One "`L`" restricts output to LDIFv1; another disables comments; and the third one removes the LDIF version from the output.
 * `-Y EXTERNAL`: Select the `EXTERNAL` SASL mechanism for authentication.
 * `-H ldapi:///`: The URL to use to contact the server. In this case, it will use a local unix socket.
 * `-b cn=config`: Start the search at the `cn=config` base.
 * `dn`: Only retrieve the `dn` attribute.

The output will be the similar to the following:
```text
dn: cn=config
dn: cn=module{0},cn=config
dn: cn=schema,cn=config
dn: cn={0}core,cn=schema,cn=config
dn: cn={1}cosine,cn=schema,cn=config
dn: cn={2}nis,cn=schema,cn=config
dn: cn={3}inetorgperson,cn=schema,cn=config
dn: olcDatabase={-1}frontend,cn=config
dn: olcDatabase={0}config,cn=config
dn: olcDatabase={1}mdb,cn=config
```

Where the entries mean the following:
- **`cn=config`**: Global settings
- **`cn=module{0},cn=config`**: A dynamically loaded module
- **`cn=schema,cn=config`**: Contains hard-coded system-level schema
- **`cn={0}core,cn=schema,cn=config`**: The hard-coded *core* schema
- **`cn={1}cosine,cn=schema,cn=config`**: The Cosine schema
- **`cn={2}nis,cn=schema,cn=config`**: The Network Information Services (NIS) schema
- **`cn={3}inetorgperson,cn=schema,cn=config`**: The InetOrgPerson schema
- **`olcDatabase={-1}frontend,cn=config`**: {term}`Frontend` database, default settings for other databases
- **`olcDatabase={0}config,cn=config`**: `slapd` configuration database (`cn=config`)
- **`olcDatabase={1}mdb,cn=config`**: Your database instance (`dc=example,dc=com`)

Since the configuration is located under the `cn=config` suffix, we can use LDAP commands to inspect or modify it.

To see all the configuration, run this command:

```console
sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config
```

The output is too large to show here, but it will start like this:
```text
dn: cn=config
objectClass: olcGlobal
cn: config
olcArgsFile: /var/run/slapd/slapd.args
olcLogLevel: none
...
```

### Default "data" tree

After installing the `slapd` package, a default data tree is configured, based on the detected domain name of the system. Assuming a domain of `example.com`, this command can be run to show what it looks like:

```console    
ldapsearch -x -LLL -H ldap:/// -b dc=example,dc=com dn
```

Here the only new command-line option is `-x`, and we have a new parameter for `-H`:

 * `-x`: Use simple authentication instead of SASL, which is essentially a plain text authentication. Since no **Bind DN** was provided (via `-D`), this becomes an *anonymous* bind. Without `-x`, the default is to use a SASL bind.
 * `-H ldap:///`: Use the LDAP protocol over the network (and not over a unix socket), and since no hostname was provided, it's assumed to be localhost. To access a server on another host, one would use `ldap://server.example.com/` as the URL, for example.

The output will be the top-level entry which represents the base of the DIT.
```text
dn: dc=example,dc=com
```

## Who am I?

A very handy tool to verify the authentication is `ldapwhoami`, which can be used as follows:

```console
ldapwhoami -x
```

The output will say who we connected as:
```text
anonymous
```


Now let's perform an authenticated call, via simple authentication:
```console
ldapwhoami -x -D cn=admin,dc=example,dc=com -W
```
This time we will be shown our authentication DN, after the password prompt:
```text
Enter LDAP Password:
dn:cn=admin,dc=example,dc=com
```

When you use simple bind (`-x`) and specify a Bind DN with `-D` as your authentication DN, the server will look for a `userPassword` attribute in the entry, and use that to verify the credentials. In this particular case above, we used the database **Root DN** entry, i.e., the actual administrator, and that is a special case whose password is set in the configuration when the package is installed.

```{note}
A simple bind without some sort of transport security mechanism is **clear text**, meaning the credentials are transmitted in the clear. You should {ref}`add Transport Layer Security (TLS) support <ldap-and-tls>` to your OpenLDAP server as soon as possible.
```

Let's try some SASL EXTERNAL authentication commands:
```console
ldapwhoami -Y EXTERNAL -H ldapi:/// -Q
```

The authentication DN is quite different from the simple bind one from before:
```text
dn:gidNumber=1000+uidNumber=1000,cn=peercred,cn=external,cn=auth
```

Let's try as root:
```console
sudo ldapwhoami -Y EXTERNAL -H ldapi:/// -Q
```
Notice how the `uidNumber` and `gidNumber` changed:
```text
dn:gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth
```

When using SASL EXTERNAL via the `ldapi:///` transport, the Bind DN becomes a combination of the {term}`uid` and {term}`gid` of the connecting user, followed by the suffix `cn=peercred,cn=external,cn=auth`. The server ACLs know about this, and grant the local root user complete write access to `cn=config` via the SASL mechanism.

```{note}
OpenLDAP ACLs are explained in {ref}`Set up access control <ldap-access-control>`
```

## Populate the directory

Let's introduce some content to our directory. We will add the following:

- A node called **People**, to store users
  - An entry for a user called **john**
- A node called **Groups**, to store groups
  - An entry for a group called **miners**

Create the following LDIF file and call it `add_content.ldif`:

```text
dn: ou=People,dc=example,dc=com
objectClass: organizationalUnit
ou: People

dn: ou=Groups,dc=example,dc=com
objectClass: organizationalUnit
ou: Groups

dn: cn=miners,ou=Groups,dc=example,dc=com
objectClass: posixGroup
cn: miners
gidNumber: 5000
memberUid: john

dn: uid=john,ou=People,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: john
sn: Doe
givenName: John
cn: John Doe
displayName: John Doe
uidNumber: 10000
gidNumber: 5000
userPassword: {CRYPT}x
gecos: John Doe
loginShell: /bin/bash
homeDirectory: /home/john
```

```{note}
It's important that `uid` and `gid` values in your directory do not collide with local Linux users' values as defined in `/etc/passwd` and `/etc/group`. You can use higher number ranges, such as starting at 5000 or even higher.
```

Add the content:

```console
ldapadd -x -D cn=admin,dc=example,dc=com -W -f add_content.ldif
```

The command will ask for the admin password, and then show the entries as they are being added:
```text
Enter LDAP Password: ********
adding new entry "ou=People,dc=example,dc=com"

adding new entry "ou=Groups,dc=example,dc=com"

adding new entry "cn=miners,ou=Groups,dc=example,dc=com"

adding new entry "uid=john,ou=People,dc=example,dc=com"
```

We can check that the information has been correctly added with the `ldapsearch` utility. For example, let's search for the "john" entry, and request the `cn` and `gidnumber` attributes:

```console
ldapsearch -x -LLL -b dc=example,dc=com '(uid=john)' cn gidNumber
```

The output shows the DNs that matched the search criteria, and the requested attributes:
```text
dn: uid=john,ou=People,dc=example,dc=com
cn: John Doe
gidNumber: 5000
```

Here we used an LDAP "filter": `(uid=john)`. LDAP filters are very flexible and can become complex. For example, to list the group names of which **john** is a member, we could use the following command:

```console
ldapsearch -x -LLL -b dc=example,dc=com '(&(objectClass=posixGroup)(memberUid=john))' cn gidNumber
```
And the result tells us that "john" is a member of the "miners" group:
```text
dn: cn=miners,ou=Groups,dc=example,dc=com
cn: miners
gidNumber: 5000
```

That filter is a logical "AND" (signalled by the "`&`" character in the filter expression) between two attributes: `objectClass=posixGroup` AND `memberUid=john`. Filters are very important in LDAP and mastering their syntax is extremely helpful. They are used for simple queries like this, but can also select what content is to be replicated to a secondary server, or even in complex ACLs. The full specification is defined in [RFC 4515](http://www.rfc-editor.org/rfc/rfc4515.txt).

Notice we set the `userPassword` field for the "john" entry to the cryptic value `{CRYPT}x`. This essentially is an invalid password, because no hashing will produce just `x`. It's a common pattern when adding a user entry without a default password. To change the password to something valid, you can now use `ldappasswd`:

```console
ldappasswd -x -D cn=admin,dc=example,dc=com -W -S uid=john,ou=people,dc=example,dc=com
```

We will be prompted for the new password twice, and at the end for the bind password corresponding to the bind DN specified via `-D`:
```text
New password:
Re-enter new password:
Enter LDAP Password:
```

To verify the change, we can use `ldapwhoami` with simple bind authentication using john's DN as the bind DN:
```console
ldapwhoami -x -D uid=john,ou=people,dc=example,dc=com -W
```

If the new password worked, the output will show that we authenticated as the `uid=john,ou=People,dc=example,dc=com` DN:
```text
Enter LDAP Password:
dn:uid=john,ou=People,dc=example,dc=com
```

```{note}
Remember that simple binds are insecure and you should {ref}`add TLS support <ldap-and-tls>` to your server as soon as possible!
```

<h2 id="heading--modifying-slapd-config">Change the configuration</h2>

The `slapd-config` DIT can also be queried and modified. Here are some common operations.

### Which "admin" DN to use?

Throughout this guide so far, we have used two different authentication mechanisms to make changes to the directory. Which one is needed for what kind of change?

Each directory tree suffix has its own specific administrative DN. This is the DN that can make changes to the tree and is not subject to ACLs. It is stored in the `olcRootDN` attribute under the `cn=config` configuration tree, and the corresponding password is in the `olcRootPW` attribute.

Besides this specific administrator entry, ACLs can also grant such privileges to any other DN in the directory. All of this is setup by the `slapd` package when it is installed. This results in the following DNs that can be used to make changes to each directory suffix:


| Suffix            | DN for making changes      | Authentication mechanism          |
|-------------------|----------------------------|-----------------------------------|
| cn=config         | cn=admin,cn=config         | absent                            |
| cn=config         | gidNumber=0+uidNumber=0,<br>cn=peercred,cn=external,cn=auth    | SASL EXTERNAL as root via ldapi:// |
| dc=example,dc=com | cn=admin,dc=example,dc=com | Simple bind with password<br>set during install or reconfigure         |


### Change the "admin" password
There is really only one administrative DN that has an associated password, and it's the one created at install (or reconfigure) time. To locate it in the `cn=config` suffix, run this command:
```console
sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config '(olcSuffix=dc=example,dc=com)' olcSuffix olcRootDN olcRootPW
```
The output will be the configuration entry for the `dc=example,dc=com` suffix, and show only the selected attributes in the response:
```text
dn: olcDatabase={1}mdb,cn=config
olcSuffix: dc=example,dc=com
olcRootDN: cn=admin,dc=example,dc=com
olcRootPW: {SSHA}Y0UjBUUmf08TC25ePVc6waI/mfvPNktk
```
Since the `olcRootPW` password attribute we want to change is located under the `cn=config` suffix, we will also have to use the SASL EXTERNAL authentication to modify it, according to the table shown earlier.

```{note}
Even though this `olcRootDN` is the administrative DN for the `dc=example,dc=com` suffix, it is stored under the `cn=config` suffix!
```

To change the password associated with the `olcRootDN` administrative DN, we need to replace the value of the `olcRootPW` attribute. That value is not the literal password, but the hash of the password, using a specific hash algorithm.

To obtain the hash of a password, suitable to be used as the value of `olcRootPW`, run the `slappasswd` command and type the password you want, with a confirmation. The output will be the hash for that password, which we will need for the next step:

```text
New password:
Re-enter new password:
{SSHA}VKrYMxlSKhONGRpC6rnASKNmXG2xHXFo
```

Now prepare a `changerootpw.ldif` file with this content, which includes the hashed password from the output above:

```text
dn: olcDatabase={1}mdb,cn=config
changetype: modify
replace: olcRootPW
olcRootPW: {SSHA}VKrYMxlSKhONGRpC6rnASKNmXG2xHXFo
```

Finally, run the `ldapmodify` command on this file:

```console
ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f changerootpw.ldif
```

If successful, the output will show the entry that is being modified:
```
modifying entry "olcDatabase={1}mdb,cn=config"
```

### Add an index

Like in other database types, having an index for attributes commonly used in searches can speed up such searches dramatically, specially on large trees. The default installation of OpenLDAP already creates several common indexes, but depending on your data and queries, other indexes might be helpful.

Use `ldapmodify` to add an "Index" to your `{1}mdb,cn=config` database definition (for **`dc=example,dc=com`**). In this example, we will add an "equality" and a "substring" index to the `mail` attribute. Create a file called `add_index.ldif`, and add the following contents:

```text
dn: olcDatabase={1}mdb,cn=config
add: olcDbIndex
olcDbIndex: mail eq,sub
```

Then issue the command:

```console
sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f add_index.ldif
```

The output will show the modifications being done:
```text
modifying entry "olcDatabase={1}mdb,cn=config"
```

You can confirm the change with a search:

```console
ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config '(olcDatabase={1}mdb)' olcDbIndex
```

And the result will include all instances of the `olcDbIndex` attribute:
```text
dn: olcDatabase={1}mdb,cn=config
olcDbIndex: objectClass eq
olcDbIndex: cn,uid eq
olcDbIndex: uidNumber,gidNumber eq
olcDbIndex: member,memberUid eq
olcDbIndex: mail eq,sub
```

```{seealso}
To learn more about OpenLDAP indexes, check the upstream documentation at https://www.openldap.org/doc/admin26/tuning.html#Indexes
```

### Add a schema

Schemas can only be added to `cn=config` if they are in LDIF format. If not, they will first have to be converted. You can find unconverted schemas in addition to converted ones in the `/etc/ldap/schema` directory.

```{note}
It is not trivial to remove a schema from the slapd-config database. Practice adding schemas on a test system.
```

In the following example we'll add one of the pre-installed policy schemas in `/etc/ldap/schema/`. The pre-installed schemas exists in both converted (`.ldif`) and native (`.schema`) formats, so we don't have to convert them and can use `ldapadd` directly:

```console
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/corba.ldif
```

The output will confirm the new schema being added:
```
adding new entry "cn=corba,cn=schema,cn=config"
```

If the schema you want to add does not exist in LDIF format, a nice conversion tool that can be used is provided in the `schema2ldif` package.

## Logging

Activity logging for `slapd` is very useful when implementing an OpenLDAP-based solution -- and it must be manually enabled after software installation. Otherwise, only rudimentary messages will appear in the logs. Logging, like any other such configuration, is enabled via the `slapd-config` database.

OpenLDAP comes with multiple logging levels, with each level containing the lower one (additive). A good level to try is **stats**. The {manpage}`slapd-config(5)` manual page has more to say on the different subsystems.

### Example logging with the stats level 

Create the file `logging.ldif` with the following contents:

```text
dn: cn=config
changetype: modify
replace: olcLogLevel
olcLogLevel: stats
```

Run `ldapmodify` to implement the change:

```console
sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f logging.ldif
```

Depending on how active your OpenLDAP server is, this will produce a significant amount of logging. It is recommended to revert back to a less verbose level once the need for this detailed logging isn't there anymore.

While in this verbose mode your host's syslog engine (rsyslog) may have a hard time keeping up. If you see log message like this, it means some messages were dropped:

```text
rsyslogd-2177: imuxsock lost 228 messages from pid 2547 due to rate-limiting
```

You may consider a change to rsyslog's configuration. In `/etc/rsyslog.conf`, add:

```text
# Disable rate limiting
# (default is 200 messages in 5 seconds; below we make the 5 become 0)
$SystemLogRateLimitInterval 0
```

And then restart the rsyslog daemon:

```console
sudo systemctl restart syslog.service
```

## Next steps

Now that you have successfully installed LDAP, you may want to {ref}`set up users and groups <ldap-users-and-groups>`, or find out more {ref}`about access control <ldap-access-control>`.
