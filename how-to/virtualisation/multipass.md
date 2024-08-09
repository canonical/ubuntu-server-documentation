(create-vms-with-multipass)=
# How to create a VM with Multipass


[Multipass](https://multipass.run) is the recommended method for creating Ubuntu VMs on Ubuntu. It's designed for developers who want a fresh Ubuntu environment with a single command, and it works on Linux, Windows and macOS.

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
snapcraft:core18            18.04             20201111         Snapcraft builder for Core 18
snapcraft:core20            20.04             20210921         Snapcraft builder for Core 20
snapcraft:core22            22.04             20220426         Snapcraft builder for Core 22
snapcraft:devel                               20221128         Snapcraft builder for the devel series
core                        core16            20200818         Ubuntu Core 16
core18                                        20211124         Ubuntu Core 18
18.04                       bionic            20221117         Ubuntu 18.04 LTS
20.04                       focal             20221115.1       Ubuntu 20.04 LTS
22.04                       jammy,lts         20221117         Ubuntu 22.04 LTS
22.10                       kinetic           20221101         Ubuntu 22.10
daily:23.04                 devel,lunar       20221127         Ubuntu 23.04
appliance:adguard-home                        20200812         Ubuntu AdGuard Home Appliance
appliance:mosquitto                           20200812         Ubuntu Mosquitto Appliance
appliance:nextcloud                           20200812         Ubuntu Nextcloud Appliance
appliance:openhab                             20200812         Ubuntu openHAB Home Appliance
appliance:plexmediaserver                     20200812         Ubuntu Plex Media Server Appliance
anbox-cloud-appliance                         latest           Anbox Cloud Appliance
charm-dev                                     latest           A development and testing environment for charmers
docker                                        latest           A Docker environment with Portainer and related tools
jellyfin                                      latest           Jellyfin is a Free Software Media System that puts you in control of managing and streaming your media.
minikube                                      latest           minikube is local Kubernetes
```

## Launch a fresh instance of the Ubuntu Jammy (22.04) LTS

You can launch a fresh instance by specifying either the image name from the list (in this example, 22.04) or using an alias, if the image has one. 

```bash
$ multipass launch 22.04
Launched: cleansing-guanaco
```

This command is equivalent to: `multipass launch jammy` or `multipass launch lts` in the list above. It will launch an instance based on the specified image, and provide it with a random name -- in this case, `cleansing-guanaco`.

## Check out the running instances

You can check out the currently running instance(s) by using the "multipass list` command:

```bash
$ multipass list                                                  
Name                    State             IPv4             Image
cleansing-guanaco       Running           10.140.26.17     Ubuntu 22.04 LTS
```

## Learn more about the VM instance you just launched

You can use the `multipass info` command to find out more details about the VM instance parameters:

```bash
$ multipass info cleansing-guanaco 
Name:           cleansing-guanaco
State:          Running
IPv4:           10.140.26.17
Release:        Ubuntu 22.04.1 LTS
Image hash:     dc5b5a43c267 (Ubuntu 22.04 LTS)
Load:           0.45 0.19 0.07
Disk usage:     1.4G out of 4.7G
Memory usage:   168.3M out of 969.5M
Mounts:         --
```

## Connect to a running instance

To enter the VM you created, use the `shell` command:

```bash
$ multipass shell cleansing-guanaco 
Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.0-53-generic x86_64)
(...)
ubuntu@cleansing-guanaco:~$ 
```

### Disconnect from the instance

Don't forget to log out (or <kbd>Ctrl</kbd> + <kbd>D</kbd>) when you are done, or you may find yourself heading all the way down the Inception levels...

## Run commands inside an instance from outside

```bash
$ multipass exec cleansing-guanaco -- lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 22.04.1 LTS
Release:	22.04
Codename:	jammy
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

## Integrate with the rest of your virtualization

You might have other virtualization already based on libvirt, either through using the similar older {ref}`uvtool <cloud-image-vms-with-uvtool>` or through the more common [virt-manager](https://virt-manager.org/).

You might, for example, want those guests to be on the same bridge to communicate with each other, or if you need access to the graphical output for some reason.

Fortunately it is possible to integrate this by using the {ref}`libvirt <libvirt>` backend of Multipass:

```bash
$ sudo multipass set local.driver=libvirt
```

Now when you start a guest you can also access it via tools like [virt-manager](https://virt-manager.org/) or `virsh`:

```bash
$ multipass launch lts
Launched: engaged-amberjack 

$ virsh list
 Id    Name                           State
----------------------------------------------------
 15    engaged-amberjack              running
```

For more detailed and comprehensive instructions on changing your drivers, refer to the [Multipass drivers documentation](https://multipass.run/docs/set-up-the-driver).

## Get help

You can use the following commands on the CLI:

```bash
multipass help
multipass help <command>
multipass help --all
```

Or, check out the [Multipass documentation](https://multipass.run/docs) for more details on how to use it.
