---
myst:
  html_meta:
    description: Install and manage LXD system containers and virtual machines with command-line administration for development and production workloads.
---

(lxd-containers)=
# LXD containers and virtual machines

[LXD](https://canonical.com/lxd) (pronounced lex-dee) is a modern, secure, and powerful system container and virtual machine manager.

It provides a unified experience for running and managing full Linux systems inside containers or virtual machines. You can access it via the command line, its [built-in graphical user interface](https://documentation.ubuntu.com/lxd/latest/howto/access_ui/), or a set of powerful [REST APIs](https://documentation.ubuntu.com/lxd/latest/restapi_landing/). 

LXD scales from one instance on a single machine [to a cluster](https://documentation.ubuntu.com/lxd/latest/explanation/clusters/) in a full data center rack, making it suitable for both development and production workloads. You can even use LXD to set up a small, scalable private cloud, [such as a MicroCloud](https://canonical.com/microcloud). 

This document will focus on how to configure and administer LXD on Ubuntu systems using the command line. On Ubuntu Server Cloud images, LXD comes pre-installed.

## Online resources

You can visit [the official LXD documentation](https://documentation.ubuntu.com/lxd/), or get in touch with the LXD team in their [Ubuntu Discourse forum](https://discourse.ubuntu.com/c/lxd/126). The team also maintains a [YouTube channel](https://www.youtube.com/c/LXDvideos) with helpful videos. 

## Installation

LXD is pre-installed on Ubuntu Server cloud images. On other systems, the `lxd` package can be installed using:

``` 
sudo snap install lxd
```

This will install the self-contained LXD snap package.

## Configuration

In order to use LXD, some basic settings need to be configured first. This is done by running:

```
lxd init
```

This will allow you to choose:

  - Directory, [Btrfs](https://btrfs.readthedocs.io/), or [ZFS](https://openzfs.org/wiki/Main_Page) container backend. If you choose ZFS, you can choose which block devices to use, or the size of a file to use as backing store.

  - Availability over the network.

  - A 'trust password' used by remote clients to vouch for their client certificate.

You must run `lxd init` as root. `lxc` commands can be run as any user who is a member of group lxd. If user `joe` is not a member of group `lxd`, you may run:

``` 
gpasswd -a joe lxd
```

as root to change it. The new membership will take effect on the next login, or after running `newgrp lxd` from an existing login.

See [How to initialize LXD](https://documentation.ubuntu.com/lxd/latest/howto/initialize/) in the LXD documentation for more information on the configuration settings. Also, refer to the definitive configuration provided with the source code for the server, container, profile, and device configuration. 

## Creating your first container

This section will describe the simplest container tasks.

### Creating a container

Every new container is created based on either an image, an existing container, or a container snapshot. At install time, LXD is configured with the following image servers:

  - `ubuntu`: this serves official Ubuntu cloud image releases.

  - `ubuntu-daily`: this serves official Ubuntu cloud images of the daily development releases.

  - `ubuntu-minimal`: this serves official Ubuntu Minimal cloud image releases.

  - `images`: this server provides unofficial images for a variety of Linux distributions. This is not the recommended server for Ubuntu images.

The command to create and start a container is:

``` 
lxc launch remote:image containername
```

To create a virtual machine instead of a container, use:

``` 
lxc launch --vm remote:image vmname
```

Alternatively, you can create a container without starting it using:

``` 
lxc init remote:image containername
```

Images are identified by their hash, but are also aliased. A list of all images available from the Ubuntu Server can be seen using:

``` 
lxc image list ubuntu:
```

To see more information about a particular image, including all the aliases it is known by, you can use:

``` 
lxc image info ubuntu:noble
```

You can generally refer to an Ubuntu image using the release name (`noble`) or the release number (`24.04`). The `ubuntu` remote knows many aliases such as `24.04`, `noble`, and `lts` which is an alias for the latest supported LTS release. To choose a different architecture, you can specify the desired architecture:

``` 
lxc image info ubuntu:lts/arm64
```

Now, let's start our first container:

``` 
lxc launch ubuntu:noble n1
```

This will download the official current Noble cloud image for your current architecture, then create a container named `n1` using that image, and finally start it. Once the command returns, you can see it using:

``` 
lxc list
lxc info n1
```

and open a shell in it using:

``` 
lxc exec n1 -- sudo -i -u ubuntu
```

This command provides a proper login shell with full session initialization, including PTY ownership and systemd user session setup.

A convenient alias that opens a shell without the full login process is:

```
lxc shell n1
```

The try-it page mentioned above gives a full synopsis of the commands you can use to administer containers.

Now that the `noble` image has been downloaded, it will be kept in sync until no new containers have been created based on it for (by default) 10 days. After that, it will be deleted.

## LXD server configuration

By default, LXD is socket activated and configured to listen only on a local UNIX socket. While LXD may not be running when you first look at the process listing, any LXC command will start it up. For instance:

``` 
lxc list
```

This will create your client certificate and contact the LXD server for a list of containers. To make the server accessible over the network you can set the http port using:

``` 
lxc config set core.https_address :8443
```

This will tell LXD to listen to port 8443 on all addresses.

### Authentication

By default, LXD will allow all members of group `lxd` to talk to it over the UNIX socket. Communication over the network is authorized using server and client certificates.

Before client `c1` wishes to use remote `r1`, `r1` must be registered using:

``` 
lxc remote add r1 r1.example.com:8443
```

The fingerprint of r1's certificate will be shown, to allow the user at c1 to reject a false certificate. The server in turn will verify that c1 may be trusted in one of two ways. The first is to register it in advance from any already-registered client, using:

``` 
lxc config trust add r1 certfile.crt
```

Now when the client adds r1 as a known remote, it will not need to provide a password as it is already trusted by the server.

The other step is to configure a 'trust password' with `r1` at initial configuration using `lxd init`. The password can then be provided when the client registers `r1` as a known remote.

## Container configuration

Containers are configured according to a set of profiles, described in the next section, and a set of container-specific configuration. Profiles are applied first, so that container specific configuration can override profile configuration.

Container configuration includes properties like the architecture, limits on resources such as CPU and RAM, security details including AppArmor restriction overrides, and devices to apply to the container.

Devices can be of several types, including UNIX character, UNIX block, network interface, or disk. In order to insert a host mount into a container, a 'disk' device type would be used. For instance, to mount `/opt` in container `c1` at `/opt`, you could use:

``` 
lxc config device add c1 opt-mount disk source=/opt path=/opt
```

See:

``` 
lxc help config
```

for more information about editing container configurations. You may also use:

``` 
lxc config edit c1
```

to edit the whole of `c1`'s configuration. Comments at the top of the configuration will show examples of correct syntax to help administrators hit the ground running. If the edited configuration is not valid when the editor is exited, then the editor will be restarted.

## Profiles

Profiles are named collections of configurations which may be applied to more than one container. For instance, all containers created with `lxc launch`, by default, include the `default` profile, which provides a network interface `eth0`.

To mask a device which would be inherited from a profile but which should not be in the final container, define a device by the same name but of type 'none':

``` 
lxc config device add c1 eth1 none
```

## Nesting

Containers all share the same host kernel. This means that there is always an inherent trade-off between features exposed to the container and host security from malicious containers. Containers by default are therefore restricted from features needed to nest child containers. In order to run lxc or lxd containers under a lxd container, the `security.nesting` feature must be set to true:

``` 
lxc config set container1 security.nesting true
```

Once this is done, `container1` will be able to start sub-containers.

In order to run unprivileged (the default in LXD) containers nested under an unprivileged container, you will need to ensure a wide enough UID mapping. Please see the 'UID mapping' section below.

## Limits

LXD supports flexible constraints on the resources which containers can consume. The limits come in the following categories:

  - CPU: limit CPU available to the container in several ways

  - Disk: configure the priority of I/O requests under load

  - RAM: configure memory and swap availability

  - Network: configure the network priority under load

  - Processes: limit the number of concurrent processes in the container

For a full list of limits known to LXD, see [the configuration documentation](https://documentation.ubuntu.com/lxd/latest/reference/instance_options/).

## UID mappings and privileged containers

By default, LXD creates unprivileged containers. This means that root in the container is a non-root UID on the host. It is privileged against the resources owned by the container, but unprivileged with respect to the host, making root in a container roughly equivalent to an unprivileged user on the host. (The main exception is the increased attack surface exposed through the system call interface)

Briefly, in an unprivileged container, 65536 UIDs are 'shifted' into the container. For instance, UID 0 in the container may be 100000 on the host, UID 1 in the container is 100001, etc, up to 165535. The starting value for UIDs and {term}`GIDs <GID>`, respectively, is determined by the 'root' entry the `/etc/subuid` and `/etc/subgid` files. (See the {manpage}`subuid(5)`) manual page.)

It is possible to request a container to run without a UID mapping by setting the `security.privileged` flag to true:

``` 
lxc config set c1 security.privileged true
```

Note however that in this case the root user in the container is the root user on the host.

## AppArmor

LXD confines containers by default with an AppArmor profile which protects containers from each other and the host from containers. For instance this will prevent root in one container from signaling root in another container, even though they have the same UID mapping. It also prevents writing to dangerous, un-namespaced files such as many sysctls and ` /proc/sysrq-trigger`.

If the AppArmor policy for a container needs to be modified for a container `c1`, specific AppArmor policy lines can be added in the `raw.apparmor` configuration key.

## Seccomp

All containers are confined by a default seccomp policy. This policy prevents some dangerous actions such as forced unmounts, kernel module loading and unloading, kexec, and the `open_by_handle_at` system call. The seccomp configuration cannot be modified, however a completely different seccomp policy -- or none -- can be requested using `raw.lxc` (see below).

## Raw LXC configuration

LXD configures containers for the best balance of host safety and container usability. Whenever possible it is highly recommended to use the defaults, and use the LXD configuration keys to request LXD to modify as needed. Sometimes, however, it may be necessary to talk to the underlying lxc driver itself. This can be done by specifying LXC configuration items in the 'raw.lxc' LXD configuration key. These must be valid items as documented in the {manpage}`lxc.container.conf(5)` manual page.

### Snapshots

Containers can be renamed and live-migrated using the `lxc move` command:

``` 
lxc move c1 final-beta
```

They can also be snapshotted:

``` 
lxc snapshot c1 snapshot-name
```

Later changes to c1 can then be reverted by restoring the snapshot:

``` 
lxc restore c1 snapshot-name
```

New containers can also be created by copying a container or snapshot:

``` 
lxc copy c1/snapshot-name new-container
```

### Publishing images

When a container or container snapshot is ready for consumption by others, it can be published as a new image using;

``` 
lxc publish c1/snapshot-name --alias foo-2.0
```

The published image will be private by default, meaning that LXD will not allow clients without a trusted certificate to see them. If the image is safe for public viewing (i.e. contains no private information), then the 'public' flag can be set, either at publish time using

``` 
lxc publish c1/snapshot-name --alias foo-2.0 public=true
```

or after the fact using

``` 
lxc image edit foo-2.0
```

and changing the value of the public field.

### Image export and import

Images can be exported as, and imported from, tarballs:

``` 
lxc image export foo-2.0 foo-2.0.tar.gz
lxc image import foo-2.0.tar.gz --alias foo-2.0 --public
```

## Troubleshooting

To view debug information about LXD itself, on a systemd based host use

``` 
journalctl -u lxd
```

Container log files for container c1 may be seen using:

``` 
lxc info c1 --show-log
```

The configuration file which was used may be found under ` /var/log/lxd/c1/lxc.conf` while AppArmor profiles can be found in ` /var/lib/lxd/security/apparmor/profiles/c1` and seccomp profiles in ` /var/lib/lxd/security/seccomp/c1`.
