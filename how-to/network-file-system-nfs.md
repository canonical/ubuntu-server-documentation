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