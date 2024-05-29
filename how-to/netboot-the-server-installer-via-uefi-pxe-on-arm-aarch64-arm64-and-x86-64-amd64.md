# Netboot the server installer via UEFI PXE on ARM (aarch64, arm64) and x86_64 (amd64)


This document provides the steps needed to install a system via netbooting and the live server installer (Subiquity) in UEFI mode with Ubuntu 20.04 (or later).

The process described here is applicable to both arm64 and amd64 architectures. The process is inspired by [this Ubuntu Discourse post](https://discourse.ubuntu.com/t/netbooting-the-live-server-installer/14510) for **legacy mode**, which is UEFI's predecessor. Focal (20.04, 20.04.5) and Groovy (20.10) have been tested with the following method.

## Configure TFTP

This article assumes that you have set up your TFTP (and/or DHCP/bootp if necessary, depending on your LAN configuration) by following [the method described here](https://discourse.ubuntu.com/t/netbooting-the-live-server-installer/14510). You could also build your own TFTP in this way if your DNS and DHCP are already well configured:

```
$ sudo apt install tftpd-hpa
```

If the installation is successful, check that the corresponding TFTP service is active using this command:

```
$ systemctl status tftpd-hpa.service
```

It is expected to show **active (running)** in the output messages. We will also assume your TFTP root path is `/var/lib/tftpboot` for the remainder of this article.

## How to serve files

You can **skip the whole section** of the following manual set up instruction by using [this non-official tool](https://github.com/dannf/ubuntu-server-netboot). The tool will setup your TFTP server to serve necessary files for netbooting.

### Necessary files

The following files are needed for this process:

- Ubuntu live server image:
  - For arm64 architectures, the image name has the suffix `-arm64`. For example, `ubuntu-20.04.5-live-server-arm64.iso`.
  - For amd64 architectures, the image name has the suxxif `-amd64`. For example, `ubuntu-20.04.5-live-server-amd64.iso`.
- GRUB EFI binary (and the corresponding `grub.cfg` text file):
  - For arm64 architectures, this is called `grubnetaa64.efi.signed`.
  - For amd64 architectures, this is called `grubnetx64.efi.signed`.
- `initrd` extracted from your target Ubuntu live server image (use `hwe-initrd` instead if you want to boot with the HWE kernel).
- `vmlinuz` extracted from your target Ubuntu live server image (use `hwe-vmlinuz` instead if you want to boot with the HWE kernel).

### Examples

In the following sections, we will use an arm64 image as an example. This means the following files are used:

- Ubuntu 20.04.5 live server image [ubuntu-20.04.5-live-server-arm64.iso](https://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-arm64.iso)
- GRUB EFI binary [grubnetaa64.efi.signed](http://ports.ubuntu.com/ubuntu-ports/dists/focal/main/uefi/grub2-arm64/current/grubnetaa64.efi.signed)
- `initrd` extracted from `ubuntu-20.04.5-live-server-arm64.iso`
- `vmlinuz` extracted from `ubuntu-20.04.5-live-server-arm64.iso`


Replace the corresponding files if you want to work on an amd64 image. For example, your files may be:

- Ubuntu 20.04.5 live server image [ubuntu-20.04.5-live-server-amd64.iso](https://releases.ubuntu.com/20.04.5/ubuntu-20.04.5-live-server-amd64.iso)
- GRUB EFI binary [grubnetx64.efi.signed](http://archive.ubuntu.com/ubuntu/dists/focal/main/uefi/grub2-amd64/current/grubnetx64.efi.signed)
- `initrd` extracted from `ubuntu-20.04.5-live-server-amd64.iso`
- `vmlinuz` extracted from `ubuntu-20.04.5-live-server-amd64.iso`


### Download and serve the GRUB EFI binary

The GRUB binary helps us redirect the download path to the target files via `grub.cfg`. Refer to [the instructions here](https://discourse.ubuntu.com/t/netbooting-the-live-server-installer/14510) to get more information about the PXE process and why we need this binary.

```
$ sudo wget http://ports.ubuntu.com/ubuntu-ports/dists/focal/main/uefi/grub2-arm64/current/grubnetaa64.efi.signed -O /var/lib/tftpboot/grubnetaa64.efi.signed
```

> **Note**:
> You may need to change **the archive distribution's name** from `Focal` to your target distribution name.

### Download and serve more files

Fetch the installer by downloading an Ubuntu ARM server ISO, e.g. the [20.04.5 live server arm64 ISO](http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-arm64.iso). Note that the prefix "live" is significant. We will need the files available only in the live version.

Mount the ISO and copy the target files we need over to the TFTP folder:

```
$ sudo mount ./ubuntu-20.04.5-live-server-arm64.iso /mnt
$ sudo mkdir /var/lib/tftpboot/grub /var/lib/tftpboot/casper
$ sudo cp /mnt/boot/grub/grub.cfg /var/lib/tftpboot/grub/
$ sudo cp /mnt/casper/initrd /var/lib/tftpboot/casper/
$ sudo cp /mnt/casper/vmlinuz /var/lib/tftpboot/casper/
```

So, the TFTP root folder should look like this now:

```
$ find /var/lib/tftpboot/
/var/lib/tftpboot/
/var/lib/tftpboot/grub
/var/lib/tftpboot/grub/grub.cfg
/var/lib/tftpboot/grubnetaa64.efi.signed
/var/lib/tftpboot/casper
/var/lib/tftpboot/casper/initrd
/var/lib/tftpboot/casper/vmlinuz
```

Finally, let’s customise the GRUB menu so we can install our target image by fetching it directly over the internet.

```
$ sudo chmod +w /var/lib/tftpboot/grub/grub.cfg
$ sudo vi /var/lib/tftpboot/grub/grub.cfg
```

Add a new entry:

```
menuentry "Install Ubuntu Server (Focal 20.04.5) (Pull the iso from web)" {
        set gfxpayload=keep
        linux   /casper/vmlinuz url=http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-arm64.iso only-ubiquity ip=dhcp ---
        initrd  /casper/initrd
}
```

Note that here:

* `ip=dhcp` is for the DHCP management setup in the lab. 
* `url` is used to point to your target image download URL. Remember to change them according to your scenario.

If everything goes well, you should get into the expected GRUB menu of the ephemeral live prompt. Select the entry you just put in `grub.cfg`, which is `Install Ubuntu Server (Focal 20.04.5) (Pull the ISO from web)` in our example. Wait for the ISO to download, and then you will see the Subiquity welcome message. Enjoy the installation!

## Appendix

### Always check the serving file names

For example, always make sure the target file name for `linux` and `initrd` is correct. For example, the default `initrd` binary file name of 20.04.5 is `initrd`, and it is `initrd.lz` for 20.10. Always make sure you serve the correct file names, since this is a frequent troubleshooting issue. Paying attention to this detail could save you a lot of time.

### Booting screenshots

If your setup is correct, your `grub.cfg` should redirect the process to an ephemeral environment where your target image is downloaded and assigned in the GRUB entry of `grub.cfg`. You will see a screen like this if you are able to access the console or monitor device of your target machine:

![Downloading target image|690x246](https://assets.ubuntu.com/v1/fbdff13b-downloading_image.png) 

Wait for the download to complete. If you see this Subiquity welcome page, the installer successfully launched via your UEFI PXE setup. Congratulations!

![Subiquity welcome page|690x380](https://assets.ubuntu.com/v1/ef037190-subiquity_welcome_page.png)
