(install-nfs)=
# Network File System (NFS)

NFS allows a system to share directories and files with others over a network. By using NFS, users and programs can access files on remote systems almost as if they were local files.

Some of the most notable benefits that NFS can provide are:

  - Local workstations use less disk space because commonly used data can be stored on a single machine and still remain accessible to others over the network.

  - There is no need for users to have separate home directories on every network machine. Home directories could be set up on the NFS server and made available throughout the network.

  - Storage devices such as floppy disks, CDROM drives, and USB Thumb drives can be used by other machines on the network. This may reduce the number of removable media drives throughout the network.

## Installation

At a terminal prompt enter the following command to install the NFS Server:

    sudo apt install nfs-kernel-server

To start the NFS server, you can run the following command at a terminal prompt:

    sudo systemctl start nfs-kernel-server.service

## Configuration

You can configure the directories to be exported by adding them to the `/etc/exports` file. For example:

    /srv     *(ro,sync,subtree_check)
    /home    *.hostname.com(rw,sync,no_subtree_check)
    /scratch *(rw,async,no_subtree_check,no_root_squash)

Make sure any custom mount points you're adding have been created (/srv and /home will already exist):

    sudo mkdir /scratch

Apply the new config via:

    sudo exportfs -a

You can replace \* with one of the hostname formats. Make the hostname declaration as specific as possible so unwanted systems cannot access the NFS mount.  Be aware that `*.hostname.com` will match` foo.hostname.com` but not `foo.bar.my-domain.com`.

The *sync*/*async* options control whether changes are gauranteed to be committed to stable storage before replying to requests.  *async* thus gives a performance benefit but risks data loss or corruption.  Even though *sync* is the default, it's worth setting since exportfs will issue a warning if it's left unspecified.

*subtree_check* and *no_subtree_check* enables or disables a security verification that subdirectories a client attempts to mount for an exported filesystem are ones they're permitted to do so.  This verification step has some performance implications for some use cases, such as home directories with frequent file renames.  Read-only filesystems are more suitable to enable *subtree_check* on.  Like with sync, exportfs will warn if it's left unspecified.

There are a number of optional settings for NFS mounts for tuning performance, tightening security, or providing conveniences.  These settings each have their own trade-offs so it is important to use them with care, only as needed for the particular use case.  *no_root_squash*, for example, adds a convenience to allow root-owned files to be modified by any client system's root user; in a multi-user environment where executables are allowed on a shared mount point, this could lead to security problems.

## NFS Client Configuration

To enable NFS support on a client system, enter the following command at the terminal prompt:

    sudo apt install nfs-common

Use the mount command to mount a shared NFS directory from another machine, by typing a command line similar to the following at a terminal prompt:

    sudo mkdir /opt/example
    sudo mount example.hostname.com:/srv /opt/example

> **Warning**
> 
> The mount point directory `/opt/example` must exist. There should be no files or subdirectories in the `/opt/example` directory, else they will become inaccessible until the nfs filesystem is unmounted.

An alternate way to mount an NFS share from another machine is to add a line to the `/etc/fstab` file. The line must state the hostname of the NFS server, the directory on the server being exported, and the directory on the local machine where the NFS share is to be mounted.

The general syntax for the line in `/etc/fstab` file is as follows:

    example.hostname.com:/srv /opt/example nfs rsize=8192,wsize=8192,timeo=14,intr

## Advanced Configuration

NFS is comprised of several services, both on the server and the client. Each one of these services can have its own default configuration, and depending on the Ubuntu Server release you have installed, this configuration is done in different files, and with a different syntax.

### Ubuntu Server 22.04 LTS ("jammy")

All NFS related services read a single configuration file: `/etc/nfs.conf`. This is a INI-style config file, see the [`nfs.conf(5)`](http://manpages.ubuntu.com/manpages/jammy/man5/nfs.conf.5.html) manpage for details. Furthermore, there is a `/etc/nfs.conf.d` directory which can hold `*.conf` snippets that can override settings from previous snippets or from the `nfs.conf` main config file itself.

There is a new command-line tool called [`nfsconf(8)`](http://manpages.ubuntu.com/manpages/jammy/man8/nfsconf.8.html) which can be used to query or even set configuration parameters in `nfs.conf`. In particular, it has a `--dump` parameter which will show the effective configuration including all changes done by `/etc/nfs.conf.d/*.conf` snippets.

### For Ubuntu Server 20.04 LTS ("focal") and earlier

Earlier Ubuntu releases use the traditional configuration mechanism for the NFS services via `/etc/defaults/` configuration files. These are `/etc/default/nfs-common` and `/etc/default/nfs/kernel-server`, and are used basically to adjust the command-line options given to each daemon.

Each file has a small explanation about the available settings.

> **Warning**
>
> The `NEED_*` parameters have no effect on systemd-based installations, like Ubuntu 20.04 LTS ("focal") and Ubuntu 18.04 LTS ("bionic").
> In those systems, to control whether a service should be running or not, use `systemctl enable` or `systemctl disable`, respectively.

## Upgrading to Ubuntu 22.04 LTS ("jammy")

The main change to the NFS packages in Ubuntu 22.04 LTS ("jammy") is the configuration file. Instead of multiple files sourced by startup scripts from `/etc/default/nfs-*`, now there is one main configuration file in `/etc/nfs.conf`, with an INI-style syntax.
When upgrading to Ubuntu 22.04 LTS ("jammy") from a release that still uses the `/etc/defaults/nfs-*` configuration files, the following will happen:

 * a default `/etc/nfs.conf` configuration file will be installed
 * if the `/etc/default/nfs-*` files have been modified, a conversion script will be run and it will create `/etc/nfs.conf.d/local.conf` with the local modifications.

If this conversion script fails, then the package installation will fail. This can happen if the `/etc/default/nfs-*` files have an option that the conversion script wasn't prepared to handle, or a syntax error for example. In such cases, please file a bug using this link: [https://bugs.launchpad.net/ubuntu/+source/nfs-utils/+filebug](https://bugs.launchpad.net/ubuntu/+source/nfs-utils/+filebug)

You can run the conversion tool manually to gather more information about the error: it's in `/usr/share/nfs-common/nfsconvert.py` and must be run as `root`.

If all goes well, as it should in most cases, the system will have `/etc/nfs.conf` with the defaults, and `/etc/nfs.conf.d/local.conf` with the changes. You can merge these two together manually, and then delete `local.conf`, or leave it as is. Just keep in mind that `/etc/nfs.conf` is not the whole story: always inspect `/etc/nfs.conf.d` as well, as it may contain files overriding the defaults.

You can always run `nfsconf --dump` to check the final settings, as it merges together all configuration files and shows the resulting non-default settings.

## Restarting NFS services

Since NFS is comprised of several individual services, it can be difficult to determine what to restart after a certain configuration change.

The tables below summarize all available services, which "meta" service they are linked to, and which configuration file each service uses.

| Service     | nfs-utils.service | nfs-server.service | config file (22.04)   | config file (< 22.04) /etc/default/nfs-\*
|-------------|-------------------|--------------------|-----------------------|------------------------------------------
| nfs-blkmap  | PartOf            |                    | nfs.conf              |
| nfs-mountd  |                   | BindsTo            | nfs.conf              | nfs-kernel-server
| nfsdcld     |                   |                    |                       |
| nfs-idmapd  |                   | BindsTo            | nfs.conf, idmapd.conf | idmapd.conf
| rpc-gssd    | PartOf            |                    | nfs.conf              |
| rpc-statd   | PartOf            |                    | nfs.conf              | nfs-common
| rpc-svcgssd | PartOf            | BindsTo            | nfs.conf              | nfs-kernel-server

For example, `systemctl restart nfs-server.service` will restart `nfs-mountd`, `nfs-idmapd` and `rpc-svcgssd` (if running). On the other hand, restarting `nfs-utils.service` will restart `nfs-blkmap`, `rpc-gssd`, `rpc-statd` and `rpc-svcgssd`.

Of course, each service can still be individually restarted with the usual `systemctl restart <service>`.

The [`nfs.systemd(7)`](http://manpages.ubuntu.com/manpages/jammy/man7/nfs.systemd.7.html) manpage has more details on the several systemd units available with the NFS packages.


## NFS with Kerberos

Kerberos with NFS adds an extra layer of security on top of NFS. It can be just a stronger authentication mechanism, or it can also be used to sign and encrypt the NFS traffic.

This section will assume you already have setup a Kerberos server, with a running KDC and admin services. Setting that up is explained elsewhere in the Ubuntu Server Guide.

### NFS server (using kerberos)

The NFS server will have the usual `nfs-kernel-server` package and its dependencies, but we will also have to install kerberos packages. The kerberos packages are not strictly necessary, as the necessary keys can be copied over from the KDC, but it makes things much easier.

For this example, we will use:
 - `.vms` {term}`DNS` domain
 - `VMS` Kerberos realm
 - `j-nfs-server.vms` for the NFS server
 - `j-nfs-client.vms` for the NFS client
 - `ubuntu/admin` principal has admin privileges on the KDC

Adjust these names according to your setup.

First, install the `krb5-user` package:

    sudo apt install krb5-user

Then, with an admin principal, let's create a key for the NFS server:

    $ sudo kadmin -p ubuntu/admin -q "addprinc -randkey nfs/j-nfs-server.vms"

And extract the key into the local keytab:

    $ sudo kadmin -p ubuntu/admin -q "ktadd nfs/j-nfs-server.vms"
    Authenticating as principal ubuntu/admin with password.
    Password for ubuntu/admin@VMS:
    Entry for principal nfs/j-nfs-server.vms with kvno 2, encryption type aes256-cts-hmac-sha1-96 added to keytab FILE:/etc/krb5.keytab.
    Entry for principal nfs/j-nfs-server.vms with kvno 2, encryption type aes128-cts-hmac-sha1-96 added to keytab FILE:/etc/krb5.keytab.

Confirm the key is available:

    $ sudo klist -k
    Keytab name: FILE:/etc/krb5.keytab
    KVNO Principal
    ---- --------------------------------------------------------------------------
       2 nfs/j-nfs-server.vms@VMS
       2 nfs/j-nfs-server.vms@VMS

Now install the NFS server:

    $ sudo apt install nfs-kernel-server

This will already automatically start the kerberos-related nfs services, because of the presence of `/etc/krb5.keytab`.

Now populate `/etc/exports`, restricting the exports to krb5 authentication. For example, exporting `/storage` using `krb5p`:

    /storage *(rw,sync,no_subtree_check,sec=krb5p)

Refresh the exports:

    $ sudo exportfs -rav
    exporting *:/storage

The security options are explained in the [`exports(5)`](http://manpages.ubuntu.com/manpages/jammy/man5/exports.5.html) manpage, but generally they are:
  - `krb5`: use kerberos for authentication only (non-auth traffic is in clear text)
  - `krb5i`: use kerberos for authentication and integrity checks (non-auth traffic is in clear text)
  - `krb5p`: use kerberos for authentication, integrity and privacy protection (non-auth traffic is encrypted)

### NFS client (using kerberos)

The NFS client has a similar set of steps. First we will prepare the client's keytab, so that when we install the NFS client package it will start the extra kerberos services automatically just by detecting the presence of the keytab:

    sudo apt install krb5-user

To allow the `root` user to mount NFS shares via kerberos without a password, we have to create a host key for the NFS client:

    sudo kadmin -p ubuntu/admin -q "addprinc -randkey host/j-nfs-client.vms"

And extract it:

    $ sudo kadmin -p ubuntu/admin -q "ktadd host/j-nfs-client.vms"

Now install the NFS client package:

    $ sudo apt install nfs-common

And you should be able to do your first NFS kerberos mount:

    $ sudo mount j-nfs-server:/storage /mnt

If you are using a machine credential, then the above mount will work without having a kerberos ticket, i.e., `klist` will show no tickets:

    # mount j-nfs-server:/storage /mnt
    # ls -l /mnt/*
    -rw-r--r-- 1 root root 0 Apr  5 14:50 /mnt/hello-from-nfs-server.txt
    # klist
    klist: No credentials cache found (filename: /tmp/krb5cc_0)

Notice the above was done with `root`. Let's try accessing that existing mount with the `ubuntu` user, without acquiring a kerberos ticket:

    # sudo -u ubuntu -i
    $ ls -l /mnt/*
    ls: cannot access '/mnt/*': Permission denied

The `ubuntu` user will only be able to access that mount if they have a kerberos ticket:

    $ kinit
    Password for ubuntu@VMS: 
    $ ls -l /mnt/*
    -rw-r--r-- 1 root root 0 Apr  5 14:50 /mnt/hello-from-nfs-server.txt

And now we have not only the TGT, but also a ticket for the NFS service:

    $ klist
    Ticket cache: FILE:/tmp/krb5cc_1000
    Default principal: ubuntu@VMS

    Valid starting     Expires            Service principal
    04/05/22 17:48:50  04/06/22 03:48:50  krbtgt/VMS@VMS
            renew until 04/06/22 17:48:48
    04/05/22 17:48:52  04/06/22 03:48:50  nfs/j-nfs-server.vms@
            renew until 04/06/22 17:48:48
            Ticket server: nfs/j-nfs-server.vms@VMS

One drawback of using a machine credential for mounts done by the `root` user is that you need a persistent secret (the `/etc/krb5.keytab` file) in the filesystem. Some sites may not allow such a persistent secret to be stored in the filesystem. An alternative is to use `rpc.gssd`s `-n` option. From `rpc.gssd(8)`:

  - `-n`: when specified, UID 0 is forced to obtain user credentials which are used instead of the local system's machine credentials.

When this option is enabled and `rpc.gssd` restarted, then even the `root` user will need to obtain a kerberos ticket to perform an NFS kerberos mount.

> Warning
>
> Note that this prevents automatic NFS mounts via `/etc/fstab`, unless a kerberos ticket is obtained before.

In Ubuntu 22.04 LTS ("jammy"), this option is controlled in `/etc/nfs.conf` in the `[gssd]` section:

    [gssd]
    use-machine-creds=0

In older Ubuntu releases, the command line options for the `rpc.gssd` daemon are not exposed in `/etc/default/nfs-common`, therefore a systemd override file needs to be created. You can either run:

    $ sudo systemctl edit rpc-gssd.service

And paste the following into the editor that will open:

    [Service]
    ExecStart=
    ExecStart=/usr/sbin/rpc.gssd $GSSDARGS -n

Or manually create the file `/etc/systemd/system/rpc-gssd.service.d/override.conf` and any needed directories up to it, with the contents above.

After you restart the service with `systemctl restart rpc-gssd.service`, the `root` user won't be able to mount the NFS kerberos share without obtaining a ticket first.


## References

* [Linux NFS wiki](http://linux-nfs.org/wiki/)
* [Linux NFS faq](http://nfs.sourceforge.net/)

* [Ubuntu Wiki NFS Howto](https://help.ubuntu.com/community/SettingUpNFSHowTo)
* [Ubuntu Wiki NFSv4 Howto](https://help.ubuntu.com/community/NFSv4Howto)
