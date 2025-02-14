(ldap-saslauthd-kerberos)=
# How to configure OpenLDAP with pass-through SASL authentication using Kerberos
There exists applications that can only use "simple" username and password [Lightweight Directory Access Protocol](https://ldap.com/) (LDAP) authentication. Pass-though password authentication is a solution to this problem.

## Before you begin
It is assumed you are starting with a working OpenLDAP server, with a hostname of `ldap-server.example.com`. If not, follow this guide {ref}`Install and configure OpenLDAP<install-openldap>` to set it up. It is also assumed that the `EXAMPLE.COM` realm is set up, and the Kerberos client tools (krb5-user) are installed on the ldap server. You will need to create an ubuntu principal. See {ref}`How to install a Kerberos server <install-a-kerberos-server>`. You should also know how to create service principals. See {ref}`How to configure Kerberos service principals <configure-service-principals>`.
All the following configuration will be on `ldap-server.example.com`.
> **Note**:
> This process is not the same as using [Generic Security Services Application Programming Interface](https://www.openldap.org/doc/admin26/sasl.html#GSSAPI) (GSSAPI) to log into the LDAP server.
> Rather it is using [simple authentication](https://www.openldap.org/doc/admin26/security.html#%22simple%22%20method) with the OpenLDAP server so this should be over a [Transport Layer Security](https://datatracker.ietf.org/wg/tls/documents/) (TLS) connection.
> This process also does not require the Kerberos backend to be OpenLDAP server, the default Keberberos backend if sufficient.
> The test user we will be using is `ubuntu@EXAMPLE.COM` which must exist in the Kerberos database


## Package installation
Install saslauthd

```bash
sudo apt install sasl2-bin
```
## Saslauthd service principal
It is assumed you have an admin principal set up in the realm. We will use `ubuntu/admin@EXAMPLE.COM`.
Next a principal who will be querying Kerberos is needed. The default for saslauthd is "host"/"hostname.domain"@"REALM". For the basic case, it is important that the hostname and domain be what nslookup on your IP number says it is.

## Check the hostname
Get the hostname from the server
```bash
hostname
```
Which should give you the hostname of:
```text
ldap-server
```
Next check what nslookup gives as the full canonical name
```bash
nslookup ldap-server
```
Which should look something like this.
```text
Non-authoritative answer:
Name:   ldap-server.example.com
Address: (your IP)
```
Finally, check the hostname and domain using a reverse lookup.
```bash
nslookup (your IP)
```
Check the name in the reply
```text
(PI ruoy).in-addr.arpa      name = ldap-server.example.com. (PI ruoy) is (your IP) in reverse
```
If the result is the same as your host's canonical name them all is well. If the domain is missing, the [Fully Qualified Domain Name](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) (FQDN) can be entered in the `/etc/hosts` file.
```bash
sudo vi /etc/hosts
```
Add the FQDN before the short hostname.
```text
(your IP) ldap-server.example.com ldap-server
```
## Create the saslauthd principal

The hostname portion of the principal must be in lowercase. You won't be creating a password for this principal so you will need to ask the kadmin tool to store the key in an external file on the LDAP server. The default location is `/etc/krb5.keytab` so you need to run the kadmin command as sudo.

```bash
sudo kadmin -p ubuntu/admin
Authenticating as principal ubuntu/admin with password.
Password for ubuntu/admin@EXAMPLE.COM
kadmin: addprinc -randkey host/ldap-server.example.com
No policy specified for host/ldap-server.example.com@EXAMPLE.COM; defaulting to no policy
Principal "host/ldap-server.example.com@EXAMPLE.COM" created.
kadmin: ktadd host/ldap-server.example.com
Entry for principal host/ldap-server.example.com with kvno 2, encryption type aes256-cts-hmac-sha1-96 added to keytab FILE:/etc/krb5.keytab.
Entry for principal host/ldap-server.example.com with kvno 2, encryption type aes128-cts-hmac-sha1-96 added to keytab FILE:/etc/krb5.keytab.
kadmin: q
```
To check our principals enter:
```bash
sudo klist -k
```
You should see the following.
```text
Keytab name: FILE:/etc/krb5.keytab
KVNO Principal
---- --------------------------------------------------------------------------
   2 host/ldap-server.example.com@EXAMPLE.COM
   2 host/ldap-server.example.com@EXAMPLE.COM
```
## Configure saslauthd
Next look at the default saslauthd file located in `/etc/default/saslauthd`
```bash
sudo cat /etc/default/saslauthd
```
Here is the default config.
```text
#
# Settings for saslauthd daemon
# Please read /usr/share/doc/sasl2-bin/README.Debian for details.
#

# Description of this saslauthd instance. Recommended.
# (suggestion: SASL Authentication Daemon)
DESC="SASL Authentication Daemon"

# Short name of this saslauthd instance. Strongly recommended.
# (suggestion: saslauthd)
NAME="saslauthd"

# Which authentication mechanisms should saslauthd use? (default: pam)
#
# Available options in this Debian package:
# getpwent  -- use the getpwent() library function
# kerberos5 -- use Kerberos 5
# pam       -- use PAM
# rimap     -- use a remote IMAP server
# shadow    -- use the local shadow password file
# sasldb    -- use the local sasldb database file
# ldap      -- use LDAP (configuration is in /etc/saslauthd.conf)
#
# Only one option may be used at a time. See the saslauthd man page
# for more information.
#
# Example: MECHANISMS="pam"
MECHANISMS="pam"

# Additional options for this mechanism. (default: none)
# See the saslauthd man page for information about mech-specific options.
MECH_OPTIONS=""

# How many saslauthd processes should we run? (default: 5)
# A value of 0 will fork a new process for each connection.
THREADS=5

# Other options (default: -c -m /var/run/saslauthd)
# Note: You MUST specify the -m option or saslauthd won't run!
#
# WARNING: DO NOT SPECIFY THE -d OPTION.
# The -d option will cause saslauthd to run in the foreground instead of as
# a daemon. This will PREVENT YOUR SYSTEM FROM BOOTING PROPERLY. If you wish
# to run saslauthd in debug mode, please run it by hand to be safe.
#
# See /usr/share/doc/sasl2-bin/README.Debian for Debian-specific information.
# See the saslauthd man page and the output of 'saslauthd -h' for general
# information about these options.
#
# Example for chroot Postfix users: "-c -m /var/spool/postfix/var/run/saslauthd"
# Example for non-chroot Postfix users: "-c -m /var/run/saslauthd"
#
# To know if your Postfix is running chroot, check /etc/postfix/master.cf.
# If it has the line "smtp inet n - y - - smtpd" or "smtp inet n - - - - smtpd"
# then your Postfix is running in a chroot.
# If it has the line "smtp inet n - n - - smtpd" then your Postfix is NOT
# running in a chroot.
OPTIONS="-c -m /var/run/saslauthd"
```
Two changes are needed to use Kerberos, update MECHANISMS to kerberos5 and add START=yes

```bash
sudo vi /etc/default/saslauthd
```
Make these changes.
```text
...
# Which authentication mechanisms should saslauthd use? (default: pam)
#
# Available options in this Debian package:
# getpwent  -- use the getpwent() library function
# kerberos5 -- use Kerberos 5
# pam       -- use PAM
# rimap     -- use a remote IMAP server
# shadow    -- use the local shadow password file
# sasldb    -- use the local sasldb database file
# ldap      -- use LDAP (configuration is in /etc/saslauthd.conf)
#
# Only one option may be used at a time. See the saslauthd man page
# for more information.
#
# Example: MECHANISMS="pam"
MECHANISMS="kerberos5"
START=yes
...
```
## Enable and start saslauthd
Continue by enabling the saslauthd service.

```bash
sudo systemctl enable saslauthd
```
The final step for saslauthd is to start the saslauthd service.

```bash
sudo systemctl start saslauthd
```
## Configure OpenLDAP

The OpenLDAP service needs its own Kerberos principal.
```bash
sudo kadmin -p ubuntu/admin
Authenticating as principal ubuntu/admin with password.
Password for ubuntu/admin@EXAMPLE.COM
kadmin: addprinc -randkey ldap/ldap-server.example.com
No policy specified for ldap/ldap-server.example.com@EXAMPLE.COM; defaulting to no policy
Principal "ldap/ldap-server.example.com@EXAMPLE.COM" created.
kadmin: ktadd -k /etc/ldap/ldap.keytab ldap/ldap-server.example.com
Entry for principal ldap/ldap-server.example.com with kvno 2, encryption type aes256-cts-hmac-sha1-96 added to keytab WRFILE:/etc/ldap/ldap.keytab.
Entry for principal ldap/ldap-server.example.com with kvno 2, encryption type aes128-cts-hmac-sha1-96 added to keytab WRFILE:/etc/ldap/ldap.keytab.
kadmin: q
```
The permissions of the keytab file need to be secure. Change the group and permissions to allow the slapd process to read the file.
```bash
sudo chown root:openldap /etc/ldap/ldap.keytab
sudo chmod 640 /etc/ldap/ldap.keytab
```
OpenLDAP needs to know where to look for the keytab file, what password check method to use, and where to find saslauthd socket. This can be done using the sasl config file for the slapd.
```bash
sudo vi usr/lib/sasl2/slapd.conf
```
Add this to the file.
```text
keytab: /etc/ldap/ldap.keytab
pwcheck_method: saslauthd
saslauthd_path: /var/run/saslauthd/mux
```
Restart slapd.
```bash
sudo systemctl restart slapd
```
## Change the user password
The user we will be testing with is called ubuntu. You can add the user to the OpenLDAP directory by using the ldapadd command. Remember that the ubuntu principal exists in the Kerberos database.

```bash
ldapadd -x -D cn=admin,dc=example,dc=com -W <<LDIF
dn: uid=ubuntu,ou=People,dc=example,dc=com
objectClass: posixAccount
objectClass: inetOrgPerson
uid: ubuntu
cn: ubuntu
sn: ubuntu
userPassword: {SASL}ubuntu@EXAMPLE.COM
uidNumber: 10050
gidNumber: 10050
loginShell: /bin/bash
homeDirectory: /home/ubuntu

dn: cn=ubuntu,ou=Groups,dc=example,dc=com
objectClass: posixGroup
cn: ubuntu
gidNumber: 10050
memberUid: ubuntu
LDIF
```

## Test the user
Test the new user with ldapsearch.
```bash
ldapsearch -D uid=ubuntu,ou=People,dc=example,dc=com -W -x
```
The reply should begin like this.
```text
Enter LDAP Password:
# extended LDIF
#
# LDAPv3
# base <dc=example,dc=com> (default) with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#
...
```
If you see search results then it worked, confirm using ldapwhoami
```bash
ldapwhoami -D uid=ubuntu,ou=People,dc=example,dc=com -W -x
Enter LDAP Password:
dn:uid=ubuntu,ou=People,dc=example,dc=com
```
These LDAP users can now be used with external applications that only support "simple" username and password authentication.

## References

  - [OpenLDAP Pass-through Authentication](https://www.openldap.org/doc/admin26/security.html#Pass-Through%20authentication)
  - [Cyrus SASL Password Verification](https://www.cyrusimap.org/sasl/sasl/components.html#password-verification-services)
  - [Cyrus SASL Slapd Configuration File](https://www.cyrusimap.org/sasl/sasl/faqs/openldap-sasl-gssapi.html)
  - [Kerberos Client Hostname Requirements](https://web.mit.edu/kerberos/krb5-1.12/doc/admin/princ_dns.html)
