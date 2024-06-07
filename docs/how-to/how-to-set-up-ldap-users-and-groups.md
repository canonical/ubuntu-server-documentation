(how-to-set-up-ldap-users-and-groups)=
# LDAP users and groups


Once you [have a working LDAP server](install-and-configure-ldap.md), you will need to install libraries on the client that know how and when to contact it. On Ubuntu, this was traditionally done by installing the `libnss-ldap` package, but nowadays you should use the [System Security Services Daemon (SSSD)](../explanation/introduction-to-network-user-authentication-with-sssd.md). To find out how to use LDAP with SSSD, refer to [our SSSD and LDAP](https://discourse.ubuntu.com/t/sssd-and-ldap/27895) guide.

## User and group management - `ldapscripts`

A common use case for an LDAP server is to store UNIX user and group information in the directory. There are many tools out there, and big deployments will usually develop their own. However, as a quick and easy way to get started with storing user and group information in OpenLDAP, you can use the `ldapscripts` package.

### Install ldapscripts

You can install `ldapscripts` by running the following command:

```bash
sudo apt install ldapscripts
```

Then edit the file `/etc/ldapscripts/ldapscripts.conf` to arrive at something similar to the following:

```text
SERVER=ldap://ldap01.example.com
LDAPBINOPTS="-ZZ"
BINDDN='cn=admin,dc=example,dc=com'
BINDPWDFILE="/etc/ldapscripts/ldapscripts.passwd"
SUFFIX='dc=example,dc=com'
GSUFFIX='ou=Groups'
USUFFIX='ou=People'
MSUFFIX='ou=Computers'
```

> **Note**:
> Adjust **SERVER** and related **SUFFIX** options to suit your directory structure.
> Here, we are forcing use of **START_TLS** (`-ZZ` parameter). Refer to [LDAP with TLS](ldap-and-transport-layer-security-tls.md) to learn how to set up the server with TLS support.

Store the `cn=admin` password in the `/etc/ldapscripts/ldapscripts.passwd` file and make sure it's only readable by the *root* local user:

```bash
 echo -n 'password' | sudo tee /etc/ldapscripts/ldapscripts.passwd
sudo chmod 400 /etc/ldapscripts/ldapscripts.passwd
```

>**Note**:
> The password file must contain exactly and only the password characters, no end-of-line or anything else. The `echo` command above with the `-n` parameter achieves that by suppressing the *EOL* character `\n`. And in order to prevent the password from appearing in the shell history, the *echo* command line is prefixed by a space.

The scripts are now ready to help manage your directory.

## Manage users and groups with ldapscripts

Here are some brief examples you can use to manage users and groups using `ldapscripts`. 

### Create a new user

```bash
sudo ldapaddgroup george
sudo ldapadduser george george
```
    
This will create a group and user with name "george" and set the user's primary group (*gid*) to "george" as well.

### Change a user's password

```bash
$ sudo ldapsetpasswd george

Changing password for user uid=george,ou=People,dc=example,dc=com
New Password: 
Retype New Password: 
Successfully set password for user uid=george,ou=People,dc=example,dc=com
```

## Delete a user

```bash
sudo ldapdeleteuser george
```

Note that this won't delete the user's primary group, but will remove the user from supplementary ones.

## Add a group

```bash
sudo ldapaddgroup qa
```

## Delete a group

```bash
sudo ldapdeletegroup qa
```

## Add a user to a group

```bash    
sudo ldapaddusertogroup george qa
```

You should now see a `memberUid` attribute for the `qa` group with a value of `george`.

## Remove a user from a group

```bash
sudo ldapdeleteuserfromgroup george qa
```

The `memberUid` attribute should now be removed from the `qa` group.

## Manage user attributes with `ldapmodifyuser`

The `ldapmodifyuser` script allows you to add, remove, or replace a user's attributes. The script uses the same syntax as the `ldapmodify` utility. For example:

```bash    
sudo ldapmodifyuser george
# About to modify the following entry :
dn: uid=george,ou=People,dc=example,dc=com
objectClass: account
objectClass: posixAccount
cn: george
uid: george
uidNumber: 10001
gidNumber: 10001
homeDirectory: /home/george
loginShell: /bin/bash
gecos: george
description: User account
userPassword:: e1NTSEF9eXFsTFcyWlhwWkF1eGUybVdFWHZKRzJVMjFTSG9vcHk=
        
# Enter your modifications here, end with CTRL-D.
dn: uid=george,ou=People,dc=example,dc=com
replace: gecos
gecos: George Carlin
```
    
The user's `gecos` should now be “George Carlin”.

## `ldapscripts` templates

A nice feature of `ldapscripts` is the template system. Templates allow you to customise the attributes of user, group, and machine objects. For example, to enable the `user` template, edit `/etc/ldapscripts/ldapscripts.conf` by changing:

```text    
UTEMPLATE="/etc/ldapscripts/ldapadduser.template"
```
    
There are sample templates in the `/usr/share/doc/ldapscripts/examples` directory. Copy or rename the `ldapadduser.template.sample` file to `/etc/ldapscripts/ldapadduser.template`:

```bash    
sudo cp /usr/share/doc/ldapscripts/examples/ldapadduser.template.sample \
/etc/ldapscripts/ldapadduser.template
```
    
Edit the new template to add the desired attributes. The following will create new users with an `objectClass` of `inetOrgPerson`:

```text    
dn: uid=<user>,<usuffix>,<suffix>
objectClass: inetOrgPerson
objectClass: posixAccount
cn: <user>
sn: <ask>
uid: <user>
uidNumber: <uid>
gidNumber: <gid>
homeDirectory: <home>
loginShell: <shell>
gecos: <user>
description: User account
title: Employee
```
    
Notice the `<ask>` option used for the **sn** attribute. This will make `ldapadduser` prompt you for its value.

There are utilities in the package that were not covered here. This command will output a list of them:

```bash
dpkg -L ldapscripts | grep /usr/sbin
```

## Next steps

Now that you know how to set up and modify users and groups, it's a good idea to secure your LDAP communication by [setting up Transport Layer Security (TLS)](ldap-and-transport-layer-security-tls.md).
