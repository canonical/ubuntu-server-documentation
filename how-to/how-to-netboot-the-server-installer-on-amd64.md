# How to netboot the server installer on amd64

amd64 systems boot in either UEFI or legacy ("BIOS") mode, and many systems can be configured to boot in either mode. The precise details depend on the system firmware, but both modes usually support the "Preboot eXecution Environment" (PXE) specification, which allows the provisioning of a bootloader over the network.

## Steps needed

The process for network booting the live server installer is similar for both modes and goes like this:

1. The to-be-installed machine boots, and is directed to network boot.
2. The DHCP/BOOTP server tells the machine its network configuration and where to get the bootloader.
3. The machine's firmware downloads the bootloader over TFTP and executes it.
4. The bootloader downloads configuration, also over TFTP, telling it where to download the kernel, RAM Disk and kernel command line to use.
5. The RAM Disk looks at the kernel command line to learn how to configure the network and where to download the server ISO from.
6. The RAM Disk downloads the ISO and mounts it as a loop device.
7. From this point on the install follows the same path as if the ISO was on a local block device.

The difference between UEFI and legacy modes is that in UEFI mode the bootloader is an EFI executable, signed so that is accepted by Secure Boot, and in legacy mode it is [PXELINUX](https://wiki.syslinux.org/wiki/index.php?title=PXELINUX). Most DHCP/BOOTP servers can be configured to serve the right bootloader to a particular machine.

## Configure DHCP/BOOTP and TFTP

There are several implementations of the DHCP/BOOTP and TFTP protocols available. This document will briefly describe how to configure `dnsmasq` to perform both of these roles.

1. Install `dnsmasq` with:

   ```
   sudo apt install dnsmasq
   ```

2. Put something like this in `/etc/dnsmasq.conf.d/pxe.conf`:

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

> **Note**:
> This assumes several things about your network; read `man dnsmasq` or the default `/etc/dnsmasq.conf` for many more options.

3. Restart `dnsmasq` with:

   ```
   sudo systemctl restart dnsmasq.service
   ```

## Serve the bootloaders and configuration.

**We need to make this section possible to write sanely**

Ideally this would be something like:

```
apt install cd-boot-images-amd64
ln -s /usr/share/cd-boot-images-amd64 /srv/tftp/boot-amd64
```

### Mode-independent set up

1. Download the latest live server ISO for the release you want to install:

   ```
   wget http://cdimage.ubuntu.com/ubuntu-server/daily-live/current/focal-live-server-amd64.iso
   ```

2. Mount it:

   ```
   mount ubuntu-19.10-live-server-amd64.iso /mnt
   ```

3. Copy the kernel and `initrd` from it to where the `dnsmasq` serves TFTP from:

   ```
   cp /mnt/casper/{vmlinuz,initrd} /srv/tftp/
   ```

### Set up the files for UEFI booting

1. Copy the signed shim binary into place:

   ```
   apt download shim-signed
   dpkg-deb --fsys-tarfile shim-signed*deb | tar x ./usr/lib/shim/shimx64.efi.signed -O > /srv/tftp/bootx64.efi
   ```

2. Copy the signed GRUB binary into place:

   ```
   apt download grub-efi-amd64-signed
   dpkg-deb --fsys-tarfile grub-efi-amd64-signed*deb | tar x ./usr/lib/grub/x86_64-efi-signed/grubnetx64.efi.signed -O > /srv/tftp/grubx64.efi
   ```

3. GRUB also needs a font to be available over TFTP:

   ```
   apt download grub-common
   dpkg-deb --fsys-tarfile grub-common*deb | tar x ./usr/share/grub/unicode.pf2 -O > /srv/tftp/unicode.pf2
   ```

4. Create `/srv/tftp/grub/grub.cfg` that contains:

   ```
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
        
    menuentry 'Ubuntu 20.04' {
            gfxmode $linux_gfx_mode
            linux /vmlinux $vt_handoff quiet splash
            initrd /initrd
    }
   ```

### Set up the files for legacy boot

1. Download `pxelinux.0` and put it into place:

   ```
   wget http://archive.ubuntu.com/ubuntu/dists/eoan/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/pxelinux.0
   mkdir -p /srv/tftp
   mv pxelinux.0 /srv/tftp/
   ```

5. Make sure to have installed package `syslinux-common` and then:

   ```
   cp /usr/lib/syslinux/modules/bios/ldlinux.c32 /srv/tftp/
   ```

6. Create `/srv/tftp/pxelinux.cfg/default` containing:

   ```
    DEFAULT install
    LABEL install
      KERNEL vmlinuz
      INITRD initrd
      APPEND root=/dev/ram0 ramdisk_size=1500000 ip=dhcp url=http://cdimage.ubuntu.com/ubuntu-server/daily-live/current/focal-live-server-amd64.iso
   ```
As you can see, this downloads the ISO from Ubuntu's servers. You may want to host it somewhere on your infrastructure and change the URL to match.

This configuration is very simple. PXELINUX has many, many options, and you can [consult its documentation](https://wiki.syslinux.org/wiki/index.php?title=PXELINUX) for more.
