# How to mount CIFS shares permanently

Common Internet File System (CIFS) shares are a file-sharing protocol used (mainly) in Windows for accessing files and resources (such as printers) over a network.

Permanently mounting CIFS shares involves configuring your system to automatically connect to these shared resources when the system boots, which is useful when network users need consistent and regular access to them.

In this guide, we will show you how to permanently mount and access CIFS shares. The shares can be hosted on a Windows computer/server, or on a Linux/UNIX server running [Samba](https://discourse.ubuntu.com/t/samba-introduction/11888). If you want to know how to host shares, you will need to use [Samba](https://discourse.ubuntu.com/t/samba-introduction/11888).

## Prerequisites

In order to use this guide, you will need to ensure that your network connections have been configured properly. Throughout this guide, we will use the following naming conventions:

* The local (Ubuntu) username is `ubuntuusername`
* The share username on the Windows computer is `msusername`
* The share password on the Windows computer is `mspassword`
* The Windows computer's name is `servername` (this can be either an IP address or an assigned name)
* The name of the share is `sharename`
* The shares are to be mounted in `/media/windowsshare`

## Install CIFS

To install CIFS, run the following command:

```bash
sudo apt-get install cifs-utils
```

## Mount unprotected (guest) network folders

First, let's create the mount directory. You will need a separate directory for each mount:

```bash
sudo mkdir /media/windowsshare
```

Then edit your `/etc/fstab` file (with root privileges) to add this line:

```text
//servername/sharename /media/windowsshare cifs guest,uid=1000 0 0
```

Where:

* `servername` is the server hostname or IP address,
* `guest` indicates you don't need a password to access the share,
* `uid=1000` makes the Linux user (specified by the ID) the owner of the mounted share, allowing them to rename files, and
* If there is any space in the server path, you need to replace it by `\040`, for example:
   `//servername/My\040Documents`

After you add the entry to `/etc/fstab`, type:

```bash
sudo mount /media/windowsshare
```

## Mount password-protected network folders

To auto-mount a password-protected share, you can edit `/etc/fstab` (with root privileges), and add this line:

```text
//servername/sharename /media/windowsshare cifs username=msusername,password=mspassword 0 0
```

This is not a good idea however: `/etc/fstab` is readable by everyone -- and so is your Windows password within it. The way around this is to use a credentials file. This is a file that contains just the username and password.

### Create a credentials file

Using a text editor, create a file for your remote server’s logon credential:

```bash
gedit ~/.smbcredentials
```

Enter your Windows username and password in the file:

```text
username=msusername

password=mspassword
```

Save the file and exit the editor.

Change the permissions of the file to prevent unwanted access to your credentials:

```bash
chmod 600 ~/.smbcredentials
```

Then edit your `/etc/fstab` file (with root privileges) to add this line (replacing the insecure line in the example above, if you added it):

```text
//servername/sharename /media/windowsshare cifs credentials=/home/ubuntuusername/.smbcredentials 0 0
```

Save the file and exit the editor.

Finally, test mounting the share by running:

```bash
sudo mount /media/windowsshare
```

If there are no errors, you should test how it works after a reboot. Your remote share should mount automatically. However, if the remote server goes offline, the boot process could present errors because it won't be possible to mount the share.

## Changing the share ownership

If you need to change the owner of a share, you'll need to add a **UID** (short for 'User ID') or **GID** (short for 'Group ID') parameter to the share's mount options:

```text
//servername/sharename /media/windowsshare cifs uid=ubuntuusername,credentials=/home/ubuntuusername/.smbcredentials 0 0
```

## Mount password-protected shares using `libpam-mount`

In addition to the initial assumptions, we're assuming here that your username and password are the same on both the Ubuntu machine and the network drive.

### Install `libpam-mount`

```bash
sudo apt-get install libpam-mount
```

Edit `/etc/security/pam_mount.conf.xml` using your preferred text editor.

```bash
sudo gedit /etc/security/pam_mount.conf.xml
```

First, we're moving the user-specific config parts to a file which users can actually edit themselves. 

Remove the commenting tags `(<!--` and `-->)` surrounding the section called `<luserconf name=".pam_mount.conf.xml" />`. We also need to enable some extra mount options to be used. For that, edit the "`<mntoptions allow=...`" tag and add `uid,gid,dir_mode,credentials` to it.

Save the file when done. With this in place, users can create their own `~/.pam_mount.conf.xml`.

```bash
gedit ~/.pam_mount.conf.xml
```

Add the following:

```text
<?xml version="1.0" encoding="utf-8" ?>

<pam_mount>

<volume options="uid=%(USER),gid=100,dir_mode=0700,credentials=/home/ubuntuusername/.smbcredentials,nosuid,nodev" user="*" mountpoint="/media/windowsshare" path="sharename" server="servername" fstype="cifs" />

</pam_mount>
```

## Troubleshooting

### Login errors

If you get the error "mount error(13) permission denied", then the server denied your access. Here are the first things to check:

* Are you using a valid username and password? Does that account really have access to this folder?
* Do you have blank space in your credentials file? It should be `password=mspassword`, not `password = mspassword`.
* Do you need a domain? For example, if you are told that your username is `SALES\sally`, then actually your username is `sally` and your domain is `SALES`. You can add a `domain=SALES` line to the `~/.credentials` file.
* The security and version settings are interrelated. SMB1 is insecure and no longer supported. At first, try to not specify either security or version: do not specify `sec=` or `vers=`. If you still have authentication errors then you may need to specify either `sec=` or `vers=` or both. You can try the options listed at the [mount.cifs man page](https://manpages.ubuntu.com/manpages/en/man8/mount.cifs.8.html).

### Mount after login instead of boot

If for some reason, such as networking problems, the automatic mounting during boot doesn't work, you can add the `noauto` parameter to your CIFS `fstab` entry and then have the share mounted at login.

In `/etc/fstab`:

```text
//servername/sharename /media/windowsshare cifs noauto,credentials=/home/ubuntuusername/.smbpasswd 0 0
```

You can now manually mount the share after you log in. If you would like the share to be automatically mounted after each login, please see the section above about `libpam-mount`.
