---
myst:
  html_meta:
    description: Install and use Multipass to quickly create Ubuntu VMs with a single command on Linux, Windows, and macOS using snap packages.
---

(create-vms-with-multipass)=
# How to create a VM with Multipass

[Multipass](https://canonical.com/multipass) is the recommended method for creating Ubuntu VMs on Ubuntu. It's designed for developers who want a fresh Ubuntu environment with a single command, and it works on Linux, Windows and macOS.

On Linux it's available as a snap:

```bash
sudo snap install multipass
```

If you're running an older version of Ubuntu where `snapd` isn't pre-installed, you will need to install it first:

```bash
sudo apt update
sudo apt install snapd
```

## Find available images

To find available images you can use the `multipass find` command, which will produce a list like this:

```text
Image                       Aliases           Version          Description
core                        core16            20200818         Ubuntu Core 16
core18                                        20211124         Ubuntu Core 18
core20                                        20230119         Ubuntu Core 20
core22                                        20230717         Ubuntu Core 22
22.04                       jammy             20260515         Ubuntu 22.04 LTS
24.04                       noble             20260518         Ubuntu 24.04 LTS
25.10                       questing          20260520         Ubuntu 25.10
26.04                       resolute,lts      20260520         Ubuntu 26.04 LTS
charm-dev                                     latest           A development and testing environment for charmers
docker                                        latest           A Docker environment with Portainer and related tools
minikube                                      latest           minikube is local Kubernetes
```

## Launch a fresh instance of Ubuntu 26.04 LTS

You can launch a fresh instance by specifying either the image name from the list (in this example, 26.04) or using an alias, if the image has one.

```bash
$ multipass launch 26.04
Launched: cleansing-guanaco
```

This command is equivalent to: `multipass launch resolute` or `multipass launch lts` in the list above. It will launch an instance based on the specified image, and provide it with a random name -- in this case, `cleansing-guanaco`.

## Check out the running instances

You can check out the currently running instance(s) by using the `multipass list` command:

```bash
$ multipass list
Name                    State             IPv4             Image
cleansing-guanaco       Running           10.140.26.17     Ubuntu 26.04 LTS
```

## Learn more about the VM instance you just launched

You can use the `multipass info` command to find out more details about the VM instance parameters:

```bash
$ multipass info cleansing-guanaco
Name:           cleansing-guanaco
State:          Running
Snapshots:      0
IPv4:           10.140.26.17
Release:        Ubuntu 26.04 LTS
Image hash:     dc5b5a43c267 (Ubuntu 26.04 LTS)
CPU(s):         1
Load:           0.74 0.35 0.13
Disk usage:     2.2GiB out of 4.8GiB
Memory usage:   347.4MiB out of 950.8MiB
Mounts:         --
```

## Connect to a running instance

To enter the VM you created, use the `shell` command:

```bash
$ multipass shell cleansing-guanaco
Welcome to Ubuntu 26.04 LTS (GNU/Linux 7.0.0-15-generic x86_64)
(...)
ubuntu@cleansing-guanaco:~$
```

### Disconnect from the instance

Don't forget to log out (or {kbd}`Ctrl` + {kbd}`D`) when you are done, or you may find yourself heading all the way down the Inception levels...

## Run commands inside an instance from outside

```bash
$ multipass exec cleansing-guanaco -- lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 26.04 LTS
Release:	26.04
Codename:	resolute
```

## Stop or start an instance

You can stop an instance to save resources using the `stop` command:

```bash
$ multipass stop cleansing-guanaco
```

You can start it back up again using the `start` command:

```bash
$ multipass start cleansing-guanaco
```

## Delete the instance

Once you are finished with the instance, you can delete it as follows:

```bash
$ multipass delete cleansing-guanaco
```

It will now show up as deleted when you use the `list` command:

```bash
$ multipass list
Name                    State             IPv4             Image
cleansing-guanaco       Deleted           --               Not Available
```


And when you want to completely get rid of it (and any other deleted instances), you can use the `purge` command:

```bash
$ multipass purge
```

Which we can check again using `list`:

```bash
$ multipass list
No instances found.
```

## Integrate with the rest of your virtualisation

If you already have a hypervisor interacting with {ref}`libvirt`, such as {term}`QEMU`, {term}`KVM`, or {term}`ESXi`, you might
be managing virtual machines through tools like [virt-manager](https://virt-manager.org/) or the older {ref}`uvtool <cloud-image-vms-with-uvtool>`.

In that case, integrating Multipass with your existing setup would allow VMs to share the same network bridge for communication
and be managed using `virsh`. However, Multipass runs as a headless system, so you don't have direct GUI access through virt-viewer. Follow this [guide](https://documentation.ubuntu.com/multipass/latest/how-to-guides/customise-multipass/set-up-a-graphical-interface/) to set up a GUI. 

To begin, integrate Multipass into your existing setup by selecting `libvirt` as your local driver:

```bash
$ sudo multipass set local.driver=libvirt
```

:::{note}
If you are having issues interacting with Multipass after switching to the libvirt driver, check if there is a restriction by {term}`AppArmor`, for example. AppArmor may have a default policy which restricts the multipass service from interacting with the [libvert service](https://libvirt.org/daemons.html). So you need to add an explicit permission that allows it.
:::

Start a guest, and access it via tools like [virt-manager](https://virt-manager.org/) or `virsh`:

```bash
$ multipass launch lts
Launched: engaged-amberjack

$ virsh list
 Id    Name                           State
----------------------------------------------------
 15    engaged-amberjack              running
```

For more detailed and comprehensive instructions on changing your drivers, refer to the [Multipass drivers documentation](https://documentation.ubuntu.com/multipass/latest/how-to-guides/customise-multipass/set-up-the-driver/).

## Get help

You can use the following commands on the CLI:

```bash
multipass help
multipass help <command>
multipass help --all
```

Or, check out the [Multipass documentation](https://documentation.ubuntu.com/multipass/latest/) for more details on how to use it.
