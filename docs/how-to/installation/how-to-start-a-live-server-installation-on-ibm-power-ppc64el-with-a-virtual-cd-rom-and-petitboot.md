---
myst:
  html_meta:
    description: Install Ubuntu Server on IBM Power (ppc64el) using a virtual CD-ROM with Petitboot and ipmitool for remote installation.
---

(how-to-start-a-live-server-installation-on-ibm-power-ppc64el-with-a-virtual-cd-rom-and-petitboot)=
# How to start a live server installation on IBM Power (ppc64el) with a virtual CD-ROM and Petitboot

```{note}
Not all IBM Power machines come with the capability of installing via a virtual CD-ROM! However, it is also possible to [boot the installer over the network](netboot-the-live-server-installer-on-ibm-power-ppc64el-with-petitboot.md).
```

A separate system (ideally in the same network, because of `ipmitool`) is needed to host the ppc64el ISO image file, which is later used as the virtual CD-ROM.

## Install ipmitool and Samba

Log in to this separate host and make sure that the `ipmitool` package is installed:

```
$ sudo apt install ipmitool
```

as well as Samba:

```
$ sudo apt install samba
```

## Configure Samba

Next, set up and configure Samba:

```
$ sudo touch /etc/samba/smb.conf && sudo tee -a /etc/samba/smb.conf <<EOF
[winshare]
  path=/var/winshare
  browseable = yes
  read only = no
  guest ok = yes
EOF
```

And do a quick verification that the required lines are present:

```
$ tail -n 5 /etc/samba/smb.conf
[winshare]
  path=/var/winshare
  browseable = yes
  read only = no
  guest ok = yes
```

> **Optional step**
> For downloading the image you may have to use a proxy server:
> ```
> $ sudo touch ~/.wgetrc && sudo tee -a ~/.wgetrc <<EOF
> use_proxy=yes
> http_proxy=squid.proxy:3128
> https_proxy=squid.proxy:3128
> EOF
> ```

## Download the ISO image

The ISO image needs to be downloaded now:

```
$ wget http://cdimage.ubuntu.com/ubuntu/releases/focal/release/ubuntu-20.04-live-server-ppc64el.iso --directory-prefix=/var/winshare
```

The proxy can also be passed over as a `wget` argument, like this:

```
$ wget -e use_proxy=yes -e http_proxy=squid.proxy:3128 http://cdimage.ubuntu.com/ubuntu/releases/focal/release/ubuntu-20.04-live-server-ppc64el.iso --directory-prefix=/var/winshare
```

Change the file mode of the ISO image file:

```
$ sudo chmod -R 755 /var/winshare/
$ ls -l /var/winshare/
-rwxr-xr-x 1 ubuntu ubuntu  972500992 Mar 23 08:02 focal-live-server-ppc64el.iso
```

## Restart and check Samba

Next we need to restart and check the Samba service:

```
$ sudo service smbd restart
$ sudo service smbd status
● smbd.service - Samba SMB Daemon
   Loaded: loaded (/lib/systemd/system/smbd.service; enabled; vendor 
preset: ena
   Active: active (running) since Tue 2020-02-04 15:17:12 UTC; 4s ago
     Docs: man:smbd(8)
           man:samba(7)
           man:smb.conf(5)
 Main PID: 6198 (smbd)
   Status: "smbd: ready to serve connections..."
    Tasks: 4 (limit: 19660)
   CGroup: /system.slice/smbd.service
           ├─6198 /usr/sbin/smbd --foreground --no-process-group
           ├─6214 /usr/sbin/smbd --foreground --no-process-group
           ├─6215 /usr/sbin/smbd --foreground --no-process-group
           └─6220 /usr/sbin/smbd --foreground --no-process-group
Feb 04 15:17:12 host systemd[1]: Starting Samba SMB Daemon…
Feb 04 15:17:12 host systemd[1]: Started Samba SMB Daemon.
```

Test Samba share:

```
ubuntu@host:~$ smbclient -L localhost
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\ubuntu's password: 
	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	winshare        Disk      
	IPC$            IPC       IPC Service (host server (Samba, Ubuntu))
	Reconnecting with SMB1 for workgroup listing.
	Server               Comment
	---------            -------
	Workgroup            Master
	---------            -------
	WORKGROUP            host
```

Get the IP address of the Samba host:

```
$ ip -4 -brief address show
lo               UNKNOWN        127.0.0.1/8 
ibmveth2         UNKNOWN        10.245.246.42/24 
```

> **Optional step**:
> Additional testing to make certain the Samba share is accessible from remote:
>  ```
>  user@workstation:~$ mkdir -p /tmp/test
>  user@workstation:~$ sudo mount -t cifs -o 
>  username=guest,password=guest //10.245.246.42/winshare /tmp/test/
>  user@workstation:~$ ls -la /tmp/test/
>  total 1014784
>  drwxr-xr-x  2 root root          0 May  4 15:46 .
>  drwxrwxrwt 18 root root        420 May  4 19:25 ..
>  -rwxr-xr-x  1 root root 1038249984 May  3 19:37 ubuntu-20.04-live-server-ppc64el.iso
>  ```


Now use a browser and navigate to the BMC of the Power system, which should be installed (let's assume the BMC's IP address is `10.245.246.247`):

```
firefox http://10.245.246.247/ 
```

Log into the BMC, then find and select:

>  Virtual Media --> CD-ROM

Enter the IP address of the Samba share:

> 10.245.246.42

and the path to the Samba share:

```
\winshare\focal-live-server-ppc64el.iso
```

Click "Save and Mount". Make sure that the virtual CD-ROM is really properly mounted!

```
CD-ROM Image:
  
This option allows you to share a CD-ROM image over a Windows Share with a
maximum size of 4.7GB. This image will be emulated to the host as USB device.
  
Device 1	There is an iso file mounted.
Device 2	No disk emulation set.
Device 3	No disk emulation set.
<Refresh Status>
```

```
Share host: 10.245.246.42
Path to image: \winshare\focal-live-server-ppc64el.iso
User (optional):
Password (optional):
<Save> <Mount> <Unmount>
```

````{note}
It’s important that you see a status like this:
```
Device 1 There is an iso file mounted
 ```
Then the virtual CD-ROM is properly mounted and you will see the boot/install from CD-ROM entry in Petitboot:
```
[CD/DVD: sr0 / 2020-03-23-08-02-42-00]
  Install Ubuntu Server
```
````

## Boot into the Petitboot loader

Now use `ipmitool` to boot the system into the Petitboot loader:

```
$ ipmitool -I lanplus -H 10.245.246.247 -U ADMIN -P <password> power status
$ ipmitool -I lanplus -H 10.245.246.247 -U ADMIN -P <password> sol activate
$ ipmitool -I lanplus -H 10.245.246.247 -U ADMIN -P <password> power on
Chassis Power Control: Up/On
```

And reach the Petitboot screen:

```
Petitboot (v1.7.5-p8f5fc86)                                   9006-12C BOS0026
 ─────────────────────────────────────────────
  [Network: enP2p1s0f0 / ac:1f:6b:09:c0:52]
    execute
    netboot enP2p1s0f0 (pxelinux.0)
  
  System information
  System configuration
  System status log
  Language
  Rescan devices
  Retrieve config from URL
 *Plugins (0)                              
  Exit to shell
─────────────────────────────────────────────
 Enter=accept, e=edit, n=new, x=exit, l=language, g=log, h=help
 Default boot cancelled
```

Make sure that booting from CD-ROM is enabled:

```
Petitboot (v1.7.5-p8f5fc86)                                   9006-12C BOS0026 
─────────────────────────────────────────────
  [Network: enP2p1s0f0 / ac:1f:6b:09:c0:52]
    Execute
    netboot enP2p1s0f0 (pxelinux.0)
  [Disk: sda2 / ebdb022b-96b2-4f4f-ae63-69300ded13f4]
    Ubuntu, with Linux 5.4.0-12-generic (recovery mode)
    Ubuntu, with Linux 5.4.0-12-generic
    Ubuntu
    
  System information
  System configuration
  System status log
  Language
  Rescan devices
  Retrieve config from URL
 *Plugins (0)                                          
  Exit to shell
  
─────────────────────────────────────────────
 Enter=accept, e=edit, n=new, x=exit, l=language, g=log, h=help
 [sda3] Processing new Disk device
```

```
Petitboot System Configuration
   
──────────────────────────────────────────────
  
  Autoboot:      ( ) Disabled
                 (*) Enabled
  
  Boot Order:    (0) Any CD/DVD device
                 (1) disk: sda2 [uuid: ebdb022b-96b2-4f4f-ae63-69300ded13f4]
                 (2) net:  enP2p1s0f0 [mac: ac:1f:6b:09:c0:52]
  
                 [     Add Device     ]
                 [  Clear & Boot Any  ]
                 [       Clear        ]
    
  Timeout:       30    seconds
    
    
  Network:       (*) DHCP on all active interfaces
                 ( ) DHCP on a specific interface
                 ( ) Static IP configuration
    
─────────────────────────────────────────────
 tab=next, shift+tab=previous, x=exit, h=help
```

```
Petitboot System Configuration
─────────────────────────────────────────────
  Network:       (*) DHCP on all active interfaces
                 ( ) DHCP on a specific interface
                 ( ) Static IP configuration
  
  DNS Server(s):                                   (eg. 192.168.0.2)
                 (if not provided by DHCP server)
  HTTP Proxy:                                    
  HTTPS Proxy:                                   
  
  Disk R/W:      ( ) Prevent all writes to disk
                 (*) Allow bootloader scripts to modify disks
  
  Boot console:  (*) /dev/hvc0 [IPMI / Serial]
                 ( ) /dev/tty1 [VGA]
                 Current interface: /dev/hvc0
  
                 [    OK    ]  [   Help   ]  [  Cancel  ]
  
───────────────────────────────────────────
 tab=next, shift+tab=previous, x=exit, h=help
```

Now select the 'Install Ubuntu Server' entry below the CD/DVD entry:

```
  [CD/DVD: sr0 / 2020-03-23-08-02-42-00]
  *  Install Ubuntu Server                              
```

And let Petitboot boot from the (virtual) CD-ROM image:

```
Sent SIGKILL to all processes
[  119.355371] kexec_core: Starting new kernel
[  194.483947394,5] OPAL: Switch to big-endian OS
[  197.454615202,5] OPAL: Switch to little-endian OS
```

The initial Subiquity installer screen will show up in the console:

```
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  Willkommen! Bienvenue! Welcome! Добро пожаловать! Welkom
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
  Use UP, DOWN and ENTER keys to select your language.                        
  
                [ English                                    ▸ ]              
                [ Asturianu                                  ▸ ]              
                [ Català                                     ▸ ]              
                [ Hrvatski                                   ▸ ]              
                [ Nederlands                                 ▸ ]              
                [ Suomi                                      ▸ ]              
                [ Français                                   ▸ ]              
                [ Deutsch                                    ▸ ]              
                [ Ελληνικά                                   ▸ ]              
                [ Magyar                                     ▸ ]              
                [ Latviešu                                   ▸ ]              
                [ Norsk bokmål                               ▸ ]              
                [ Polski                                     ▸ ]              
                [ Русский                                    ▸ ]              
                [ Español                                    ▸ ]              
                [ Українська                                 ▸ ]              

```

From this point, you can follow the normal Subiquity installation. For more details, refer to the [Subiquity installer documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/index.html).
