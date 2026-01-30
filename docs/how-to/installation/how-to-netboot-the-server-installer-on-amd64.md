---
myst:
  html_meta:
    description: Network boot the Ubuntu Server installer on amd64 systems using PXE in UEFI or legacy BIOS mode with DHCP, TFTP, and PXELINUX configuration.
---

(how-to-netboot-the-server-installer-on-amd64)=
# How to netboot the server installer on amd64

{term}`amd`64 systems boot in either UEFI or legacy ("BIOS") mode, and many systems can be configured to boot in either mode. The precise details depend on the system {term}`firmware <FW>`, but both modes usually support the "Preboot eXecution Environment" (PXE) specification, which allows the provisioning of a bootloader over the network.

## Steps needed

The process for network booting the live server installer is similar for both modes and goes like this:

1. The to-be-installed machine boots, and is directed to network boot.
2. The {term}`DHCP`/BOOTP server tells the machine its network configuration and where to get the bootloader.
3. The machine's firmware downloads the bootloader over TFTP and executes it.
4. The bootloader downloads configuration, also over TFTP, telling it where to download the kernel, RAM Disk and kernel command line to use.
5. The RAM Disk looks at the kernel command line to learn how to configure the network and where to download the server ISO from.
6. The RAM Disk downloads the ISO and mounts it as a loop device.
7. From this point on the install follows the same path as if the ISO were on a local block device.

The difference between UEFI and legacy modes is that in UEFI mode the bootloader is an {term}`EFI` executable, signed so that it is accepted by Secure Boot, and in legacy mode it is [PXELINUX](https://wiki.syslinux.org/wiki/index.php?title=PXELINUX). Most DHCP/BOOTP servers can be configured to serve the right bootloader to a particular machine.

## Configure DHCP/BOOTP and TFTP

There are several implementations of the DHCP/BOOTP and TFTP protocols available. This document describes how to configure {term}`dnsmasq` to perform both of these roles.

- Install `dnsmasq` with:

   ```
   sudo apt install dnsmasq
   ```

- Put something like this in `/etc/dnsmasq.d/pxe.conf`:

   ```
   interface=<your interface>,lo
   bind-interfaces
   dhcp-range=<your interface>,192.168.0.100,192.168.0.200
   dhcp-boot=pxelinux.0
   dhcp-match=set:efi-x86_64,option:client-arch,7
   dhcp-boot=tag:efi-x86_64,bootx64.efi
   enable-tftp
   tftp-root=/srv/tftp
   ```

```{note}
This assumes several things about your network; read `man dnsmasq` or the default `/etc/dnsmasq.conf` for many more options.
```

- Restart `dnsmasq` with:

   ```
   sudo systemctl restart dnsmasq.service
   ```

<!-- XXX: This is an internal note & should not be presented in public, until fixed.
## Serve the bootloaders and configuration.

**We need to make this section possible to write sanely**

Ideally this would be something like:

```
apt install cd-boot-images-amd64
ln -s /usr/share/cd-boot-images-amd64 /srv/tftp/boot-amd64
```
-->

- Install TFTP

```
$ sudo apt install tftpd-hpa
```

If the installation is successful, check that the corresponding TFTP service is active using this command:

```
$ systemctl status tftpd-hpa.service
```

It is expected to show **active (running)** in the output messages. We will also assume your TFTP root path is `/srv/tftp` for the remainder of this guide.

### Mode-independent set up

- Download the latest live server ISO for the release you want to install:

   ```
   wget http://cdimage.ubuntu.com/ubuntu-server/noble/daily-live/current/noble-live-server-amd64.iso
   ```

- Mount it:

   ```
   sudo mount noble-live-server-amd64.iso /mnt
   ```

- Copy the kernel and `initrd` from it to the TFTP directory served by `dnsmasq`:

   ```
   sudo cp /mnt/casper/{vmlinuz,initrd} /srv/tftp/
   ```

### Set up the files for UEFI booting

- Copy the signed shim binary into place:

   ```
   apt download shim-signed
   dpkg-deb --fsys-tarfile shim-signed*deb | tar x ./usr/lib/shim/shimx64.efi.signed.latest -O | sudo tee /srv/tftp/bootx64.efi >/dev/null
   ```

- Copy the signed GRUB binary into place:

   ```
   apt download grub-efi-amd64-signed
   dpkg-deb --fsys-tarfile grub-efi-amd64-signed*deb | tar x ./usr/lib/grub/x86_64-efi-signed/grubnetx64.efi.signed -O | sudo tee /srv/tftp/grubx64.efi >/dev/null
   ```

- GRUB also needs a font to be available over TFTP:

   ```
   apt download grub-common
   dpkg-deb --fsys-tarfile grub-common*deb | tar x ./usr/share/grub/unicode.pf2 -O | sudo tee /srv/tftp/unicode.pf2 >/dev/null
   ```

- Create `/srv/tftp/grub/grub.cfg` that contains:

   ```
   sudo mkdir -p /srv/tftp/grub/

   sudo tee /srv/tftp/grub/grub.cfg >/dev/null <<EOF
   set default="0"
   set timeout=-1

   if loadfont unicode ; then
      set gfxmode=auto
      set locale_dir=$prefix/locale
      set lang=en_US
   fi
   terminal_output gfxterm

   set menu_color_normal=white/black
   set menu_color_highlight=black/light-gray
   if background_color 44,0,30; then
      clear
   fi

   function gfxmode {
      set gfxpayload="${1}"
      if [ "${1}" = "keep" ]; then
         set vt_handoff=vt.handoff=7
      else
         set vt_handoff=
      fi
   }

   set linux_gfx_mode=keep

   export linux_gfx_mode

   menuentry 'Ubuntu 24.04' {
      gfxmode $linux_gfx_mode
      linux /vmlinuz $vt_handoff quiet splash root=/dev/ram0 ramdisk_size=1500000 cloud-config-url=/dev/null ip=dhcp url=http://cdimage.ubuntu.com/ubuntu-server/noble/daily-live/current/noble-live-server-amd64.iso
      initrd /initrd
   }
   EOF
   ```

### Set up the files for legacy boot

- Download `pxelinux.0` and put it into place:

   ```
   wget http://archive.ubuntu.com/ubuntu/dists/focal/main/installer-amd64/current/legacy-images/netboot/pxelinux.0
   mkdir -p /srv/tftp
   mv pxelinux.0 /srv/tftp/
   ```

- Ensure the `syslinux-common` package is installed, then:

   ```
   cp /usr/lib/syslinux/modules/bios/ldlinux.c32 /srv/tftp/
   ```

- Create `/srv/tftp/pxelinux.cfg/default` containing:

   ```
    DEFAULT install
    LABEL install
      KERNEL vmlinuz
      INITRD initrd
      APPEND root=/dev/ram0 ramdisk_size=1500000 cloud-config-url=/dev/null ip=dhcp url=http://cdimage.ubuntu.com/ubuntu-server/noble/daily-live/current/noble-live-server-amd64.iso
   ```

```{note}
Setting `cloud-config-url=/dev/null` on the kernel command line prevents cloud-init from downloading the ISO twice.
```

As you can see, this downloads the ISO from Ubuntu's servers. You may want to host it somewhere on your infrastructure and change the URL to match.

This configuration is very simple. PXELINUX has many, many options, and you can [consult its documentation](https://wiki.syslinux.org/wiki/index.php?title=PXELINUX) for more.
