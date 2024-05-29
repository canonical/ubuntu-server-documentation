# Member server in an Active Directory domain

A Samba server needs to join the Active Directory (AD) domain before it can serve files and printers to Active Directory users. This is different from [Network User Authentication with SSSD](https://discourse.ubuntu.com/t/service-sssd/11579), where we integrate the AD users and groups into the local Ubuntu system as if they were local. 

For Samba to authenticate these users via Server Message Block (SMB) authentication protocols, we need both for the remote users to be "seen", and for Samba itself to be aware of the domain. In this scenario, Samba is called a Member Server or Domain Member.

> **See also**:
> Samba itself has the necessary tooling to join an Active Directory domain. It requires a sequence of manual steps and configuration file editing, which is [thoroughly documented on the Samba wiki](https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Domain_Member). It's useful to read that documentation to get an idea of the steps necessary, and the decisions you will need to make.

## Use `realmd` to join the Active Directory domain

For this guide, though, we are going to use the `realmd` package and instruct it to use the Samba tooling for joining the AD domain. This package will make certain decisions for us which will work for most cases, but more complex setups involving multiple or very large domains might require additional tweaking.

### Install `realmd`

First, let's install the necessary packages:

```bash
sudo apt install realmd samba
```

In order to have the joined machine registered in the AD DNS, it needs to have an FQDN set. You might have that already, if running the `hostname -f` command returns a full hostname with domain. If it doesn't, then set the hostname as follows:

```bash
sudo hostnamectl hostname <yourfqdn>
```

For this guide, we will be using `j1.internal.example.fake`, and the AD domain will be `internal.example.fake`.

### Verify the AD server

Next, we need to verify that the AD server is both reachable and known by running the following command:

```bash
sudo realm discover internal.example.fake
```

This should provide an output like this, given our setup:

```text
internal.example.fake
  type: kerberos
  realm-name: INTERNAL.EXAMPLE.FAKE
  domain-name: internal.example.fake
  configured: no
  server-software: active-directory
  client-software: sssd
  required-package: sssd-tools
  required-package: sssd
  required-package: libnss-sss
  required-package: libpam-sss
  required-package: adcli
  required-package: samba-common-bin
```

`realm` is suggesting a set of packages for the discovered domain, but we will override that and select the Samba tooling for this join, because we want Samba to become a Member Server.

### Join the AD domain

Let's join the domain in verbose mode so we can see all the steps:

```bash
sudo realm join -v --membership-software=samba --client-software=winbind  internal.example.fake
```

This should produce the following output for us:

```text
 * Resolving: _ldap._tcp.internal.example.fake
 * Performing LDAP DSE lookup on: 10.0.16.5
 * Successfully discovered: internal.example.fake
Password for Administrator:
 * Unconditionally checking packages
 * Resolving required packages
 * Installing necessary packages: libnss-winbind samba-common-bin libpam-winbind winbind
 * LANG=C LOGNAME=root /usr/bin/net --configfile /var/cache/realmd/realmd-smb-conf.A53NO1 -U Administrator --use-kerberos=required ads join internal.example.fake
Password for [INTEXAMPLE\Administrator]:
Using short domain name -- INTEXAMPLE
Joined 'J1' to dns domain 'internal.example.fake'
 * LANG=C LOGNAME=root /usr/bin/net --configfile /var/cache/realmd/realmd-smb-conf.A53NO1 -U Administrator ads keytab create
Password for [INTEXAMPLE\Administrator]:
 * /usr/sbin/update-rc.d winbind enable
 * /usr/sbin/service winbind restart
 * Successfully enrolled machine in realm
```

> **Note**:
> This command also installed the `libpam-winbind` package, **which allows AD users to authenticate to other services on this system via PAM, like SSH or console logins**. For example, if your SSH server allows password authentication (`PasswordAuthentication yes` in `/etc/ssh/sshd_config`), then the domain users will be allowed to login remotely on this system via SSH.
> If you don't expect or need AD users to log into this system (unless it's via Samba or Windows), then it's safe and probably best to remove the `libpam-winbind` package.

Until [bug #1980246](https://bugs.launchpad.net/ubuntu/+source/realmd/+bug/1980246) is fixed, one extra step is needed:
- Configure `/etc/nsswitch.conf` by adding the word `winbind` to the `passwd` and `group` lines as shown below:

  ```text 
  passwd:         files systemd winbind
  group:          files systemd winbind
  ```

  Now you will be able to query users from the AD domain. Winbind adds the short domain name as a prefix to domain users and groups:

  ```
  $ getent passwd INTEXAMPLE\\Administrator
  INTEXAMPLE\administrator:*:2000500:2000513::/home/administrator@INTEXAMPLE:/bin/bash
  ```
  
  You can find out the short domain name in the `realm` output shown earlier, or inspect the `workgroup` parameter of `/etc/samba/smb.conf`.

### Common installation options

When domain users and groups are brought to the Linux world, a bit of translation needs to happen, and sometimes new values need to be created. For example, there is no concept of a "login shell" for AD users, but it exists in Linux.

The following are some common `/etc/samba/smb.conf` options you are likely to want to tweak in your installation. The [`smb.conf(5)` man page](https://manpages.ubuntu.com/manpages/jammy/man5/smb.conf.5.html) explains the `%` variable substitutions and other details:

- **home directory** 
`template homedir = /home/%U@%D`
(Another popular choice is `/home/%D/%U`)

- **login shell** 
`template shell = /bin/bash`

- `winbind separator = \`
This is the `\` character between the short domain name and the user or group name that we saw in the `getent passwd` output above.

- `winbind use default domain`
If this is set to `yes`, then the domain name will not be part of the users and groups. Setting this to `yes` makes the system more friendly towards Linux users, as they won't have to remember to include the domain name every time a user or group is referenced. However, if multiple domains are involved, such as in an AD forest or other form of domain trust relationship, then leave this setting at `no` (default).

To have the home directory created automatically the first time a user logs in to the system, and if you haven't removed `libpam-winbind`, then enable the `pam_mkhomedir` module via this command:

```bash
sudo pam-auth-update --enable mkhomedir
```

Note that this won't apply to logins via Samba: this only creates the home directory for system logins like those via `ssh` or the console.

### Export shares

Shares can be exported as usual. Since this is now a Member Server, there is no need to deal with user and group management. All of this is integrated with the Active Directory server we joined.

For example, let's create a simple `[storage]` share. Add this to the `/etc/samba/smb.conf` file:

```text
[storage]
    path = /storage
    comment = Storage share
    writable = yes
    guest ok = no
```

Then create the `/storage` directory. Let's also make it `1777` so all users can use it, and then ask samba to reload its configuration:

```bash
sudo mkdir -m 1777 /storage
sudo smbcontrol smbd reload-config
```

With this, users from the AD domain will be able to access this share. For example, if there is a user `ubuntu` the following command would access the share from another system, using the domain credentials:

```
$ smbclient //j1.internal.example.fake/storage -U INTEXAMPLE\\ubuntu
Enter INTEXAMPLE\ubuntu's password:
Try "help" to get a list of possible commands.
smb: \>
```

And `smbstatus` on the member server will show the connected user:

```
$ sudo smbstatus

Samba version 4.15.5-Ubuntu
PID     Username     Group        Machine                                   Protocol Version  Encryption           Signing