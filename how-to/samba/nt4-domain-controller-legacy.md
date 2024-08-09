(nt4-domain-controller-legacy)=
# NT4 domain controller (legacy)

> **Note**:
> This section is flagged as *legacy* because nowadays, Samba can be deployed in full Active Directory domain controller mode, and the old-style NT4 Primary Domain Controller is deprecated.

A Samba server can be configured to appear as a Windows NT4-style domain controller. A major advantage of this configuration is the ability to centralise user and machine credentials. Samba can also use multiple backends to store the user information.

## Primary domain controller

In this section, we'll install and configure Samba as a Primary Domain Controller (PDC) using the default `smbpasswd` backend.

### Install Samba

First, we'll install Samba, and `libpam-winbind` (to sync the user accounts), by entering the following in a terminal prompt:

```bash
sudo apt install samba libpam-winbind
```

### Configure Samba

Next, we'll configure Samba by editing `/etc/samba/smb.conf`. The *security* mode should be set to *user*, and the *workgroup* should relate to your organization:

```text 
workgroup = EXAMPLE
...
security = user
```

In the commented “Domains” section, add or uncomment the following (the last line has been split to fit the format of this document):

```text 
domain logons = yes
logon path = \\%N\%U\profile
logon drive = H:
logon home = \\%N\%U
logon script = logon.cmd
add machine script = sudo /usr/sbin/useradd -N -g machines -c Machine -d
      /var/lib/samba -s /bin/false %u
```

> **Note**:
> If you wish to not use *Roaming Profiles* leave the `logon home` and `logon path` options commented out.

- `domain logons`
Provides the `netlogon` service, causing Samba to act as a domain controller.

- `logon path`
Places the user's Windows profile into their home directory. It is also possible to configure a *\[profiles\]* share placing all profiles under a single directory.

- `logon drive`
Specifies the home directory local path.

- `logon home` 
Specifies the home directory location.

- `logon script`
Determines the script to be run locally once a user has logged in. The script needs to be placed in the *\[netlogon\]* share.

- `add machine script`
A script that will automatically create the *Machine Trust Account* needed for a workstation to join the domain.
    
In this example the *machines* group will need to be created using the `addgroup` utility (see {ref}`Security - Users: Adding and Deleting Users <user-management>` for details).

### Mapping shares

Uncomment the *\[homes\]* share to allow the `logon home` to be mapped:

```text
[homes]
   comment = Home Directories
   browseable = no
   read only = no
   create mask = 0700
   directory mask = 0700
   valid users = %S
```

When configured as a domain controller, a *\[netlogon\]* share needs to be configured. To enable the share, uncomment:

```text
[netlogon]
   comment = Network Logon Service
   path = /srv/samba/netlogon
   guest ok = yes
   read only = yes
   share modes = no
```

> **Note**:
> The original `netlogon` share path is `/home/samba/netlogon`, but according to the Filesystem Hierarchy Standard (FHS), [/srv is the correct location](http://www.pathname.com/fhs/pub/fhs-2.3.html#SRVDATAFORSERVICESPROVIDEDBYSYSTEM) for site-specific data provided by the system.

Now create the `netlogon` directory, and an empty (for now) `logon.cmd` script file:

```bash
sudo mkdir -p /srv/samba/netlogon
sudo touch /srv/samba/netlogon/logon.cmd
```

You can enter any normal Windows logon script commands in `logon.cmd` to customise the client's environment.

Restart Samba to enable the new domain controller, using the following command:

```bash
sudo systemctl restart smbd.service nmbd.service
```

### Final setup tasks
 
Lastly, there are a few additional commands needed to set up the appropriate rights.

Since *root* is disabled by default, a system group needs to be mapped to the Windows *Domain Admins* group in order to join a workstation to the domain. Using the `net` utility, from a terminal enter:

```bash
sudo net groupmap add ntgroup="Domain Admins" unixgroup=sysadmin rid=512 type=d
```

You should change *sysadmin* to whichever group you prefer. Also, the user joining the domain needs to be a member of the *sysadmin* group, as well as a member of the system *admin* group. The *admin* group allows `sudo` use.

If the user does not have Samba credentials yet, you can add them with the `smbpasswd` utility. Change the *sysadmin* username appropriately:

```bash
sudo smbpasswd -a sysadmin
```

Also, rights need to be explicitly provided to the *Domain Admins* group to allow the *add machine script* (and other admin functions) to work. This is achieved by executing:

```bash
net rpc rights grant -U sysadmin "EXAMPLE\Domain Admins" SeMachineAccountPrivilege \
SePrintOperatorPrivilege SeAddUsersPrivilege SeDiskOperatorPrivilege \
SeRemoteShutdownPrivilege
```

You should now be able to join Windows clients to the Domain in the same manner as joining them to an NT4 domain running on a Windows server.

## Backup domain controller

With a Primary Domain Controller (PDC) on the network it is best to have a Backup Domain Controller (BDC) as well. This will allow clients to authenticate in case the PDC becomes unavailable.

When configuring Samba as a BDC you need a way to sync account information with the PDC. There are multiple ways of accomplishing this; secure copy protocol (SCP), `rsync`, or by using LDAP as the `passdb` backend.

Using LDAP is the most robust way to sync account information, because both domain controllers can use the same information in real time. However, setting up an LDAP server may be overly complicated for a small number of user and computer accounts. See [Samba - OpenLDAP Backend](openldap-backend-legacy.md) for details.

First, install `samba` and `libpam-winbind`. From a terminal enter:

```bash
sudo apt install samba libpam-winbind
```

Now, edit `/etc/samba/smb.conf` and uncomment the following in the *\[global\]*:

```text 
workgroup = EXAMPLE
...
security = user
```

In the commented *Domains* uncomment or add:

```text 
domain logons = yes
domain master = no
```

Make sure a user has rights to read the files in `/var/lib/samba`. For example, to allow users in the *admin* group to SCP the files, enter:

```bash
sudo chgrp -R admin /var/lib/samba
```

Next, sync the user accounts, using SCP to copy the `/var/lib/samba` directory from the PDC:

```bash
sudo scp -r username@pdc:/var/lib/samba /var/lib
```

You can replace *username* with a valid username and *pdc* with the hostname or IP address of your actual PDC.

Finally, restart samba:

```bash
sudo systemctl restart smbd.service nmbd.service
```

You can test that your Backup Domain Controller is working by first stopping the Samba daemon on the PDC -- then try to log in to a Windows client joined to the domain.

Another thing to keep in mind is if you have configured the `logon home` option as a directory on the PDC, and the PDC becomes unavailable, access to the user's *Home* drive will also be unavailable. For this reason it is best to configure the `logon home` to reside on a separate file server from the PDC and BDC.

## Further reading

  - For in depth Samba configurations see the [Samba HOWTO Collection](https://www.samba.org/samba/docs/old/Samba3-HOWTO/).

  - The guide is also available [in printed format](http://www.amazon.com/exec/obidos/tg/detail/-/0131882228).

  - O'Reilly's [Using Samba](http://www.oreilly.com/catalog/9780596007690/) is also a good reference.

  - [Chapter 4](https://www.samba.org/samba/docs/old/Samba3-HOWTO/samba-pdc.html) of the Samba HOWTO Collection explains setting up a Primary Domain Controller.

  - [Chapter 5](https://www.samba.org/samba/docs/old/Samba3-HOWTO/samba-bdc.html) of the Samba HOWTO Collection explains setting up a Backup Domain Controller.

  - The [Ubuntu Wiki Samba](https://help.ubuntu.com/community/Samba) page.
