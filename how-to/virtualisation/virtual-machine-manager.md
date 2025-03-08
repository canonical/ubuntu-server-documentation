(virtual-machine-manager)=
# Virtual Machine Manager

The [Virtual Machine Manager](https://virt-manager.org/), through the `virt-manager` package, provides a graphical user interface (GUI) for managing local and remote virtual machines. In addition to the `virt-manager` utility itself, the package also contains a collection of other helpful tools like `virt-install`, `virt-clone` and `virt-viewer`.

## Install virt-manager

To install `virt-manager`, enter:

```bash
sudo apt install virt-manager
```

Since `virt-manager` requires a {term}`Graphical User Interface (GUI) <GUI>` environment we recommend installing it on a workstation or test machine instead of a production server. To connect to the local libvirt service, enter:

```bash
virt-manager
```

You can connect to the libvirt service running on another host by entering the following in a terminal prompt:

```bash
virt-manager -c qemu+ssh://virtnode1.mydomain.com/system
```

> **Note**:
> The above example assumes that SSH connectivity between the management system and the target system has already been configured, and uses **SSH keys** for authentication. SSH keys are needed because libvirt sends the password prompt to another process. See our guide on OpenSSH for details on {ref}`how to set up SSH keys <smart-card-authentication-with-ssh>`.

## Use virt-manager to manage guests

### Guest lifecycle 

When using `virt-manager` it is always important to know the context you're looking at. The main window initially lists only the currently-defined guests. You'll see their **name**, **state** (e.g., 'Shutoff' or 'Running') and a small chart showing the **CPU usage**.

![virt-manager-gui-start|499x597](https://assets.ubuntu.com/v1/07edc140-virt-manager-gui-start.png) 

In this context, there isn't much to do except start/stop a guest. However, by double-clicking on a guest or by clicking the **Open** button at the top of the window, you can see the guest itself. For a running guest that includes the guest's main-console/virtual-screen output.

![virt-manager-gui-showoutput|690x386](https://assets.ubuntu.com/v1/dda60637-virt-manager-gui-show-output.png) 

If you are deeper in the guest configuration, clicking on "Show the graphical console" in the top left of the guest's window will get you back to this output.

### Guest modification

`virt-manager` provides a handy, GUI-assisted way to edit guest definitions. To do so, the per-guest context view will have "Show virtual hardware details" at the top of the guest window. Here, you can edit the virtual hardware of the guest, which will alter the [guest representation](https://libvirt.org/formatdomain.html) behind the scenes.

![virt-manager-gui-edit|690x346](https://assets.ubuntu.com/v1/7422b267-virt-manager-gui-edit.png) 

The UI edit ability is limited to the features known to (and supported by) that GUI feature. Not only does libvirt grow features faster than `virt-manager` can keep up -- adding every feature would also overload the UI and render it unusable.

To strike a balance between the two, there also is the XML view which can be reached via the "Edit libvirt XML" button.

![virt-manager-gui-XML|690x346](https://assets.ubuntu.com/v1/34e3503f-virt-manager-gui-xml.png) 

By default, this will be read-only and you can see what the UI-driven actions have changed. You can allow read-write access in this view via the "Preferences". This is the same content that the `virsh edit` of the {ref}`libvirt-client <libvirt>` exposes.

## Virtual Machine Viewer (virt-viewer)

The Virtual Machine Viewer application, through `virt-viewer`, allows you to connect to a virtual machine's console like `virt-manager` does, but reduced to the GUI functionality. `virt-viewer` requires a GUI to interface with the virtual machine.

### Install virt-viewer

If `virt-viewer` is not already installed, you can install it from the terminal with the following command:

```bash
sudo apt install virt-viewer
```

Once a virtual machine is installed and running you can connect to the virtual machine's console by using:

```bash
virt-viewer <guestname>
```

The UI will show a window representing the virtual screen of the guest, just like with `virt-manager` above, but without the extra buttons and features around it.

![virt-viewer-gui-showoutput|690x598](https://assets.ubuntu.com/v1/a38dc56a-virt-viewer-gui-show-output.png) 

Similarly to `virt-manager`, `virt-viewer` can also connect to a remote host using SSH with key authentication:

```bash
virt-viewer -c qemu+ssh://virtnode1.mydomain.com/system <guestname>
```

Be sure to replace `web_devel` with the appropriate virtual machine name.

If configured to use a **bridged** network interface you can also set up SSH access to the virtual machine.

## virt-install

`virt-install` is part of the `virtinst` package. It can help with installing classic ISO-based systems and provides a CLI for the most common options needed to do so. 

### Install virt-install

To install `virt-install`, if it is not installed already, run the following from a terminal prompt:

```bash
sudo apt install virtinst
```

There are several options available when using `virt-install`. For example:

```bash
virt-install \
 --name web_devel \
 --ram 8192 \
 --disk path=/home/doug/vm/web_devel.img,bus=virtio,size=50 \
 --cdrom focal-desktop-amd64.iso \
 --network network=default,model=virtio \
 --graphics vnc,listen=0.0.0.0 --noautoconsole --hvm --vcpus=4
```

There are many more arguments that can be found in the [`virt-install` manpage](https://manpages.ubuntu.com/manpages/jammy/man1/virt-install.1.html). However, explaining those of the example above one by one:

* `--name web_devel`
   The name of the new virtual machine will be `web_devel`.
* `--ram 8192`
   Specifies the amount of memory the virtual machine will use (in megabytes).
* `--disk path=/home/doug/vm/web_devel.img,bus=virtio,size=50`
   Indicates the path to the virtual disk which can be a file, partition, or logical volume. In this example a file named `web_devel.img` in the current user's directory, with a size of 50 gigabytes, and using `virtio` for the disk bus. Depending on the disk path, `virt-install` may need to run with elevated privileges. 
* `--cdrom focal-desktop-amd64.iso`
   File to be used as a virtual CD-ROM. The file can be either an ISO file or the path to the host's CD-ROM device.
* `--network`
   Provides details related to the VM's network interface. Here the default network is used, and the interface model is configured for `virtio`.
* `--graphics vnc,listen=0.0.0.0`
   Exports the guest's virtual console using VNC and on all host interfaces. Typically servers have no GUI, so another GUI-based computer on the Local Area Network (LAN) can connect via VNC to complete the installation.
* `--noautoconsole`
   Will not automatically connect to the virtual machine's console.
* `--hvm` : creates a fully virtualised guest.
* `--vcpus=4` : allocate 4 virtual CPUs.

After launching `virt-install` you can connect to the virtual machine's console either locally using a GUI (if your server has a GUI), or via a remote VNC client from a GUI-based computer.

## `virt-clone`

The `virt-clone` application can be used to copy one virtual machine to another. For example:

```bash
virt-clone --auto-clone --original focal
```

Options used:
* `--auto-clone`
   To have `virt-clone` create guest names and disk paths on its own.
* `--original`
   Name of the virtual machine to copy.

You can also use the `-d` or `--debug` option to help troubleshoot problems with `virt-clone`.

Replace *`focal`* with the appropriate virtual machine names for your case.

> **Warning**: 
> Please be aware that this is a full clone, therefore any sorts of secrets, keys and for example `/etc/machine-id` will be shared. This will cause issues with security and anything that needs to identify the machine like {term}`DHCP`. You most likely want to edit those afterwards and de-duplicate them as needed.

## Resources

  - See the [KVM](http://www.linux-kvm.org/) home page for more details.

  - For more information on libvirt see the [libvirt home page](http://libvirt.org/)

  - The [Virtual Machine Manager](http://virt-manager.org/) site has more information on `virt-manager` development.
