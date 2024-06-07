(netboot-the-live-server-installer-on-ibm-power-ppc64el-with-petitboot)=
# ppc64el netboot install

Open a terminal window on your workstation and make sure the ‘ipmitool’ package is installed.

Verify if you can reach the BMC of the IBM Power system via `ipmitool` with a simple `ipmitool` call like:

```
$ ipmitool -I lanplus -H Power9Box -U <user> -P <password> power status 
Chassis Power is off
```

or:

```
$ ipmitool -I lanplus -H Power9Box -U <user> -P <password> fru print 47
  Product Name          : OpenPOWER Firmware
  Product Version       : open-power-SUPERMICRO-P9DSU-V2.12-20190404-prod
  Product Extra         : 	op-build-1b9269e
  Product Extra         : 	buildroot-2018.11.3-12-g222837a
  Product Extra         : 	skiboot-v6.0.19
  Product Extra         : 	hostboot-c00d44a-pb1307d7
  Product Extra         : 	occ-8fa3854
  Product Extra         : 	linux-4.19.30-openpower1-p22d1df8
  Product Extra         : 	petitboot-v1.7.5-p8f5fc86
```

or:
  
```
$ ipmitool -I lanplus -H Power9Box -U <user> -P <password> sol info
  Set in progress                 : set-complete
  Enabled                         : true
  Force Encryption                : false
  Force Authentication            : false
  Privilege Level                 : OPERATOR
  Character Accumulate Level (ms) : 0
  Character Send Threshold        : 0
  Retry Count                     : 0
  Retry Interval (ms)             : 0
  Volatile Bit Rate (kbps)        : 115.2
  Non-Volatile Bit Rate (kbps)    : 115.2
  Payload Channel                 : 1 (0x01)
  Payload Port                    : 623
```

## Activate serial-over-LAN

Open a second terminal and activate serial-over-LAN (SOL), so that you have two terminal windows open:

1) to control the BMC via IPMI
2) for the serial-over-LAN console

Activate serial-over-LAN:

```
$ ipmitool -I lanplus -H Power9Box -U <user> -P <password> sol activate
...
```

Power the system on in the ‘control terminal’ and watch the SOL console:

```
$ ipmitool -I lanplus -H Power9Box -U <user> -P <password> power on
...
```

It takes some time to see the first lines in the SOL console:

```
[SOL Session operational.  Use ~? for help]
--== Welcome to Hostboot  ==--

  2.77131|secure|SecureROM valid - enabling functionality
  3.15860|secure|Booting in secure mode.
  5.59684|Booting from SBE side 0 on master proc=00050000
  5.60502|ISTEP  6. 5 - host_init_fsi
  5.87228|ISTEP  6. 6 - host_set_ipl_parms
  6.11032|ISTEP  6. 7 - host_discover_targets
  6.67868|HWAS|PRESENT> DIMM[03]=A0A0000000000000
  6.67870|HWAS|PRESENT> Proc[05]=8800000000000000
  6.67871|HWAS|PRESENT> Core[07]=3FFF0C33FFC30000
  6.98988|ISTEP  6. 8 - host_update_master_tpm
  7.22711|SECURE|Security Access Bit> 0xC000000000000000
  7.22711|SECURE|Secure Mode Disable (via Jumper)> 0x0000000000000000
  7.22731|ISTEP  6. 9 - host_gard
  7.43353|HWAS|FUNCTIONAL> DIMM[03]=A0A0000000000000
  7.43354|HWAS|FUNCTIONAL> Proc[05]=8800000000000000
  7.43356|HWAS|FUNCTIONAL> Core[07]=3FFF0C33FFC30000
  7.44509|ISTEP  6.10 - host_revert_sbe_mcs_setup
…
```

After a moment the system reaches the Petitboot screen:

```
Petitboot (v1.7.5-p8f5fc86)                                   9006-12P 1302NXA 
  ─────────────────────────────────────────────────
 [Network: enP2p1s0f0 / 0c:c4:7a:87:04:d8]
   Execute
   netboot enP2p1s0f0 (pxelinux.0)
 [CD/DVD: sr0 / 2019-10-17-13-35-12-00]
   Install Ubuntu Server
 [Disk: sda2 / 295f571b-b731-4ebb-b752-60aadc80fc1b]
   Ubuntu, with Linux 5.4.0-14-generic (recovery mode)
   Ubuntu, with Linux 5.4.0-14-generic
   Ubuntu
  
 System information
 System configuration
 System status log
 Language
 Rescan devices
 Retrieve config from URL
 Plugins (0)
  
   *Exit to shell                                        
   ─────────────────────────────────────────────────
Enter=accept, e=edit, n=new, x=exit, l=language, g=log, h=help
```

Select "*Exit to shell".

> **Note**:
> Make sure you really watch the SOL, since the Petitboot screen (above) has a time out (usually 10 or 30 seconds) and afterwards it automatically proceeds and tries to boot from the configured devices (usually disk). This can be prevented by just navigating in Petitboot.
> The petitboot shell is small Linux based OS:
>  ```
>  ...
>  Exiting petitboot. Type 'exit' to return.
>  You may run 'pb-sos' to gather diagnostic data
>  ```

> **Note**:
> In case one needs to gather system details and diagnostic data for IBM support, this can be done here by running ‘pb-sos’ (see `msg`).

## Download the ISO

Now download the ‘live-server’ ISO image (notice that ‘focal-live-server-ppc64el.iso’ uses the liver server installer, Subiquity, while ‘focal-server-s390x.iso’ uses `d-i`).

Again, for certain web locations a proxy needs to be used:

```
/ # export http_proxy=http://squid.proxy:3128   # in case a proxy is required
/ # 
/ # wget http://cdimage.ubuntu.com/ubuntu-server/daily-live/current/focal-live-server-ppc64el.iso
Connecting to <proxy-ip>:3128 (<proxy-ip>:3128)
focal-live-server-pp 100% |....................|  922M  0:00:00 ETA
```

Next we need to loop-back mount the ISO:

```
/ # mkdir iso
/ # mount -o loop focal-live-server-ppc64el.iso iso
```

Or, in case autodetect of type iso9660 is not supported or not working, you should explicitly specify the 'iso9660' type:

```
/ # mount -t iso9660 -o loop focal-live-server-ppc64el.iso iso
```

Now load kernel and initrd from the loop-back mount, specify any needed kernel parameters and get it going:

```
/ # kexec -l ./iso/casper/vmlinux --initrd=./iso/casper/initrd.gz --append="ip=dhcp url=http://cdimage.ubuntu.com/ubuntu-server/daily-live/current/focal-live-server-ppc64el.iso http_proxy=http://squid.proxy:3128 --- quiet"
/ # kexec -e
The system is going down NOW!
Sent SIGTERM to all processes
Sent SIGKILL to all processes
...
```

> **Note**: 
> In order to boot with and install the HWE kernel (if available), substitute `vmlinux` with `vmlinux-hwe` in the first `kexec` line.

The system now performs the initial boot of the installer:

```
[ 1200.687004] kexec_core: Starting new kernel
[ 1277.493883374,5] OPAL: Switch to big-endian OS
[ 1280.465061219,5] OPAL: Switch to little-endian OS
ln: /tmp/mountroot-fail-hooks.d//scripts/init-premount/lvm2: No such file or directory
Internet Systems Consortium DHCP Client 4.4.1
Copyright 2004-2018 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/
Listening on LPF/enP2p1s0f3/0c:c4:7a:87:04:db
Sending on   LPF/enP2p1s0f3/0c:c4:7a:87:04:db
Listening on LPF/enP2p1s0f2/0c:c4:7a:87:04:da
Sending on   LPF/enP2p1s0f2/0c:c4:7a:87:04:da
Listening on LPF/enP2p1s0f1/0c:c4:7a:87:04:d9
Sending on   LPF/enP2p1s0f1/0c:c4:7a:87:04:d9
Listening on LPF/enP2p1s0f0/0c:c4:7a:87:04:d8
Sending on   LPF/enP2p1s0f0/0c:c4:7a:87:04:d8
Sending on   Socket/fallback
DHCPDISCOVER on enP2p1s0f3 to 255.255.255.255 port 67 interval 3
(xid=0x8d5704c)
DHCPDISCOVER on enP2p1s0f2 to 255.255.255.255 port 67 interval 3
(xid=0x94b25b28)
DHCPDISCOVER on enP2p1s0f1 to 255.255.255.255 port 67 interval 3
(xid=0x4edd0558)
DHCPDISCOVER on enP2p1s0f0 to 255.255.255.255 port 67 interval 3
(xid=0x61c90d28)
DHCPOFFER of 10.245.71.102 from 10.245.71.3
DHCPREQUEST for 10.245.71.102 on enP2p1s0f0 to 255.255.255.255 port 67
(xid=0x280dc961)
DHCPACK of 10.245.71.102 from 10.245.71.3 (xid=0x61c90d28)
bound to 10.245.71.102 -- renewal in 236 seconds.
Connecting to 91.189.89.11:3128 (91.189.89.11:3128)
focal-live-server-pp   1% |                                | 14.0M  0:01:04 ETA
focal-live-server-pp   4% |*                               | 45.1M  0:00:38 ETA
focal-live-server-pp   8% |**                              | 76.7M  0:00:33 ETA
focal-live-server-pp  11% |***                             |  105M  0:00:31 ETA
focal-live-server-pp  14% |****                            |  133M  0:00:29 ETA
focal-live-server-pp  17% |*****                           |  163M  0:00:27 ETA
focal-live-server-pp  20% |******                          |  190M  0:00:26 ETA
focal-live-server-pp  24% |*******                         |  222M  0:00:25 ETA
focal-live-server-pp  27% |********                        |  253M  0:00:23 ETA
focal-live-server-pp  30% |*********                       |  283M  0:00:22 ETA
focal-live-server-pp  34% |**********                      |  315M  0:00:21 ETA
focal-live-server-pp  37% |***********                     |  343M  0:00:20 ETA
focal-live-server-pp  39% |************                    |  367M  0:00:19 ETA
focal-live-server-pp  42% |*************                   |  392M  0:00:18 ETA
focal-live-server-pp  45% |**************                  |  420M  0:00:17 ETA
focal-live-server-pp  48% |***************                 |  451M  0:00:16 ETA
focal-live-server-pp  52% |****************                |  482M  0:00:15 ETA
focal-live-server-pp  55% |*****************               |  514M  0:00:14 ETA
focal-live-server-pp  59% |******************              |  546M  0:00:13 ETA
focal-live-server-pp  62% |********************            |  578M  0:00:11 ETA
focal-live-server-pp  65% |*********************           |  607M  0:00:10 ETA
focal-live-server-pp  69% |**********************          |  637M  0:00:09 ETA
focal-live-server-pp  72% |***********************         |  669M  0:00:08 ETA
focal-live-server-pp  75% |************************        |  700M  0:00:07 ETA
focal-live-server-pp  79% |*************************       |  729M  0:00:06 ETA
focal-live-server-pp  82% |**************************      |  758M  0:00:05 ETA
focal-live-server-pp  85% |***************************     |  789M  0:00:04 ETA
focal-live-server-pp  88% |****************************    |  817M  0:00:03 ETA
focal-live-server-pp  91% |*****************************   |  842M  0:00:02 ETA
focal-live-server-pp  93% |******************************  |  867M  0:00:01 ETA
focal-live-server-pp  97% |******************************* |  897M  0:00:00 ETA
focal-live-server-pp 100% |********************************|  922M  0:00:00 ETA
mount: mounting /cow on /root/cow failed: No such file or directory
Connecting to plymouth: Connection refused
passwd: password expiry information changed.
[   47.202736] /dev/loop3: Can't open blockdev
[   52.672550] cloud-init[3759]: Cloud-init v. 20.1-10-g71af48df-0ubuntu1 running
 'init-local' at Wed, 18 Mar 2020 15:18:07 +0000. Up 51.87 seconds.
...
```

Once it has completed, you will reach the initial Subiquity installer screen:
 
```
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    Willkommen! Bienvenue! Welcome! Добро пожаловать! Welkom          
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
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

From this point, you can follow the normal Subiquity installation. For more details, refer to the [Subquity installer documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/index.html).
