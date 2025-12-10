---
myst:
  html_meta:
    description: Automated Ubuntu Server installation on IBM z/VM (s390x) using autoinstall with DASD storage and non-VLAN network configuration.
---

(non-interactive-ibm-z-vm-autoinstall-s390x)=
# Non-interactive IBM z/VM autoinstall (s390x)


This non-interactive installation uses 'autoinstall', which can be considered the successor to the Debian installer (d-i) and preseed on Ubuntu. This is a detailed step-by-step guide, including output and logs (which are partially a bit shortened, as indicated by '...', to limit the size of this document).

The example z/VM guest here uses a direct-access storage device ({term}`DASD`) and is connected to a regular (non-VLAN) network.

For a zFCP and a VLAN network example, please see the [non-interactive IBM LPAR (s390x) installation using autoinstall](https://discourse.ubuntu.com/t/non-interactive-ibm-z-lpar-s390x-installation-using-autoinstall/16988) guide.

* Start with the preparation of the (FTP) install server (if it doesn't already exist).

  ```bash
  user@local:~$ ssh admin@installserver.local
  admin@installserver:~$ mkdir -p /srv/ftp/ubuntu-daily-live-server-20.04
  admin@installserver:~$ wget http://cdimage.ubuntu.com/ubuntu-server/focal/daily-live/current/focal-live-server-s390x.iso --directory-prefix=/srv/ftp/ubuntu-daily-live-server-20.04
  --2020-06-26 12:18:48--  http://cdimage.ubuntu.com/ubuntu-server/focal/daily-live/current/focal-live-server-s390x.iso
  Resolving cdimage.ubuntu.com (cdimage.ubuntu.com)... 2001:67c:1560:8001::1d, 2001:67c:1360:8001::28, 2001:67c:1360:8001::27, 
   ...
  Connecting to cdimage.ubuntu.com (cdimage.ubuntu.com)|2001:67c:1560:8001::1d|:80... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 700952576 (668M) [application/x-iso9660-image]
  Saving to: ‘focal-live-server-s390x.iso’
  
  focal-live-server-s 100%[===================>] 668.48M  2.73MB/s    in 4m 54s
  
  2020-06-26 12:23:42 (2.27 MB/s) - ‘focal-live-server-s390x.iso’ saved [700952576/700952576]
  admin@installserver:~$
  ```

* The ISO image needs to be extracted now. Since files in the boot folder need to be modified, loopback mount is not an option here:

  ```bash
  admin@installserver:~$ cd /srv/ftp/ubuntu-daily-live-server-20.04
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ mkdir iso
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ sudo mount -o loop ./focal-live-server-s390x.iso ./iso
  [sudo] password for admin: 
  mount: /home/user/iso-test/iso: WARNING: device write-protected, mounted read-only.
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ ls -l
  total 684530
  -rw-rw-r--  1 user user 700952576 Jun 26 10:12 focal-live-server-s390x.iso
  dr-xr-xr-x 10 root    root         2048 Jun 26 10:12 iso
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$
  ```

* Now make sure an FTP server is running in the *`installserver`* with `/srv/ftp` as `ftp-server` root (as used in this example).

* Next, prepare an *autoinstall* (HTTP) server. This hosts the configuration data for the non-interactive installation.

  ```bash
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ mkdir -p /srv/www/autoinstall/zvmguest
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ cd /srv/www/autoinstall/zvmguest
  admin@installserver:/srv/www/autoinstall/zvmguest$ 
  admin@installserver:/srv/www/autoinstall/zvmguest$ echo "instance-id: $(uuidgen || openssl rand -base64 8)" > meta-data
  admin@installserver:/srv/www/autoinstall/zvmguest$ cat meta-data
  instance-id: 2c2215fb-6a38-417f-b72f-376b1cc44f01
  admin@installserver:/srv/www/autoinstall/zvmguest$
  ```
  ```bash
  admin@installserver:/srv/www/autoinstall/zvmguest$ vi user-data
  admin@installserver:/srv/www/autoinstall/zvmguest$ cat user-data
  #cloud-config
  autoinstall:
    version: 1
    refresh-installer:
      update: yes
    reporting:
      builtin:
        type: print
    apt:
      preserve_sources_list: false
      primary:
      - arches: [amd64, i386]
        uri: http://archive.ubuntu.com/ubuntu
      - arches: [default]
        uri: http://ports.ubuntu.com/ubuntu-ports
    keyboard:
      layout: en
      variant: us
    locale: en_US
    identity:
      hostname: zvmguest
      password: 
  "$6$ebJ1f8wxED22bTL4F46P0"
        username: ubuntu
      user-data:
        timezone: America/Boston
        users:
          - name: ubuntu
            password: 
  "$6$KwuxED22bTL4F46P0"
            lock_passwd: false
      early-commands:
        - touch /tmp/lets_activate_the_s390x_devices
        - chzdev dasd -e 1f00
        - touch /tmp/s390x_devices_activation_done
      network:
        version: 2
        ethernets:
          enc600:
            addresses: [10.11.12.23/24]
            gateway4: 10.11.12.1
            nameservers:
              addresses: [10.11.12.1]
      ssh:
        install-server: true
        allow-pw: true
        authorized-keys: ['ssh-rsa  meQwtZ user@workstation # ssh-import-id lp:user']
    admin@installserver:~$
  ```

* For s390x installations, the `early-commands` section is the interesting part:

  ```bash
  early-commands:
    - touch /tmp/lets_activate_the_s390x_devices
    - chzdev dasd -e 1f00
    - touch /tmp/s390x_devices_activation_done
  ```

  The first and last `early-commands` are optional; they only frame and indicate the real s390x command activation.

  In this particular example a single {term}`DASD` {term}`ECKD` disk with the address `1f00` is enabled. zFCP disk storage can be enabled via their host ({term}`host-bus-adapters <HBA>`) addresses, for example *e000* (`chzdev zfcp -e e000`) and *e100* (`chzdev zfcp -e e000`). These have certain Logical Unit Numbers (LUNs) assigned, which are all automatically discovered and activated by `chzdev zfcp-lun -e --online`. Activation of a QETH device would look like this: `chzdev qeth -e 0600`.

* For more details about the autoinstall config options, please have a look at the [autoinstall reference](https://ubuntu.com/server/docs/install/autoinstall-reference) and [autoinstall schema](https://ubuntu.com/server/docs/install/autoinstall-schema) page.

* Now make sure a HTTP server is running with `/srv/www` as web-server root (in this particular example).

* Log in to your z/VM system using your preferred 3270 client -- for example x3270 or c3270.

* Transfer the installer kernel, initrd, parmfile and exec file to the z/VM system that is used for the installation. Put these files (for example) on File Mode (Fm) *A* (a.k.a disk *A*):

  ```
  listfiles
  UBUNTU    EXEC     A1
  KERNEL    UBUNTU   A1
  INITRD    UBUNTU   A1
  PARMFILE  UBUNTU   A1
  ```
* Now specify the necessary autoinstall parameters in the parmfile:

  ```
  xedit PARMFILE  UBUNTU   A
   PARMFILE UBUNTU   O1  F 80  Trunc=80 Size=3 Line=0 Col=1 Alt=0
  00000 * * * Top of File * * *
  00001 ip=10.11.12.23::10.11.12.1:255.255.255.0:zvmguest:enc600:none:10.11.12.1  
  00002 url=ftp://installserver.local:21/ubuntu-daily-live-server-20.04/focal-li
  ve-ser
  00003 ver-s390x.iso autoinstall ds=nocloud-net;s=http://installserver.local:80
  00004 /autoinstall/zvmguest/ --- quiet                            
  00005 * * * End of File * * * 
  ```

```{note}
In case of any issues hitting the 80-character-per-line limit of the file, you can write parameters across two lines as long as there are no unwanted white spaces. To view all 80 characters in one line, disable the prefix area on the left. "prefix off | on" will be  your friend -- use it in the command area. 
```

* You can now start the z/VM installation by executing the `UBUNTU REXX` script with `UBUNTU`.

* Now monitor the initial program load (IPL) -- a.k.a. the boot-up process -- of the install system. This is quite crucial, because during this process a temporary installation password is generated and displayed. The line(s) look similar to this:

  ```
  ...
  |37.487141| cloud-init¬1873|: Set the following 'random' passwords
  |37.487176| cloud-init¬1873|: installer: **i7UFdP8fhiVVMme3qqH8**
  ...
  ```

  This password is needed for remotely connecting to the installer via SSH in the next step.

* So, start the `REXX` script:

  ```
  UBUNTU
  00: 0000004 FILES PURGED
  00: RDR FILE 1254 SENT FROM zvmguest  PUN WAS 1254 RECS 102K CPY  
  001 A NOHOLD NO
  KEEP
  00: RDR FILE 1258 SENT FROM zvmguest  PUN WAS 1258 RECS 0003 CPY  
  001 A NOHOLD NO
  KEEP
  00: RDR FILE 1262 SENT FROM zvmguest  PUN WAS 1262 RECS 303K CPY  
  001 A NOHOLD NO
  KEEP
  00: 0000003 FILES CHANGED
  00: 0000003 FILES CHANGED
  01: HCPGSP2627I The virtual machine is placed in CP mode due to a SIGP 
  initial C
  PU reset from CPU 00.
  02: HCPGSP2627I The virtual machine is placed in CP mode due to a SIGP 
  initial C
  PU reset from CPU 00.
  03: HCPGSP2627I The virtual machine is placed in CP mode due to a SIGP 
  initial C
  PU reset from CPU 00.
  ¬    0.403380| Initramfs unpacking failed: Decoding failed
  ln: /tmp/mountroot-fail-hooks.d//scripts/init-premount/lvm2: No such file or dir
  ectory
  QETH device 0.0.0600:0.0.0601:0.0.0602 configured
  IP-Config: enc600 hardware address 02:28:0b:00:00:51 mtu 1500
  IP-Config: enc600 guessed broadcast address 10.11.12.255
  IP-Config: enc600 complete:
   address: 10.11.12.23    broadcast: 10.210.210.255   netmask: 255.255.255.0  
  
   gateway: 10.11.12.1     dns0     : 10.11.12.1     dns1   : 0.0.0.0        
  
   host   : zvmguest                                                         
   rootserver: 0.0.0.0 rootpath: 
   filename  : 
  Connecting to installserver.local:21 (10.11.12.2:21)
  focal-live-server-s3   2% !                                ! 15.2M  0:00:48 ETA
  focal-live-server-s3  16% !*****                           !  126M  0:00:09 ETA
  focal-live-server-s3  31% !**********                      !  236M  0:00:06 ETA
  focal-live-server-s3  46% !**************                  !  347M  0:00:04 ETA
  focal-live-server-s3  60% !*******************             !  456M  0:00:03 ETA
  focal-live-server-s3  74% !***********************         !  563M  0:00:02 ETA
  focal-live-server-s3  88% !****************************    !  667M  0:00:00 ETA
  focal-live-server-s3 100% !********************************!  752M  0:00:00 ETA
  mount: mounting /cow on /root/cow failed: No such file or directory
  Connecting to plymouth: Connection refused
  passwd: password expiry information changed.
  ¬   16.748137| /dev/loop3: Can't open blockdev
  ¬   17.908156| systemd¬1|: Failed unmounting /cdrom.
  ¬ ¬0;1;31mFAILED ¬0m| Failed unmounting  ¬0;1;39m/cdrom ¬0m.
  ¬ ¬0;32m  OK   ¬0m| Listening on  ¬0;1;39mJournal Socket ¬0m.
           Mounting  ¬0;1;39mHuge Pages File System ¬0m...
           Mounting  ¬0;1;39mPOSIX Message Queue File System ¬0m...
           Mounting  ¬0;1;39mKernel Debug File System ¬0m...
           Starting  ¬0;1;39mJournal Service ¬0m...
  ...
  [   61.190916] cloud-init[2076]: Cloud-init v. 20.1-10-g71af48df-0ubuntu5 running
  'modules:final' at Fri, 26 Jun 2020 11:02:01 +0000. Up 61.09 seconds.
  [   61.191002] cloud-init[2076]: ci-info: no authorized SSH keys fingerprints fo
  und for user installer.
  [   61.191071] cloud-init[2076]: Cloud-init v. 20.1-10-g71af48df-0ubuntu5 finished at Fri, 26 Jun 2020 11:02:01 +0000.
  Datasource DataSourceNoCloudNet [seed=cmdline,
  /var/lib/cloud/seed/nocloud,
  http://installserver.local:80/autoinstall/zvmguest/]
  [dsmode=net].  Up 61.18 seconds
  [   61.191136] cloud-init[2076]: Welcome to Ubuntu Server Installer!
  [   61.191202] cloud-init[2076]: Above you will find SSH host keys and a random
  password set for the `installer` user. You can use these credentials to ssh-in
  and complete the installation. If you provided SSH keys in the cloud-init datasource,
  they were also provisioned to the installer user.
  [   61.191273] cloud-init[2076]: If you have access to the graphical console,
  like TTY1 or HMC ASCII terminal you can complete the installation there too.
  
  It is possible to connect to the installer over the network, which
  might allow the use of a more capable terminal.
  
  To connect, SSH to installer@10.11.12.23.
  
  The password you should use is ''i7UFdP8fhiVVMme3qqH8''.
  
  The host key fingerprints are:
  
  RSA     SHA256:rBXLeUke3D4gKdsruKEajHjocxc9hr3PI
  ECDSA   SHA256:KZZYFswtKxFXWQPuQS9QpOBUoS6RHswis
  ED25519 SHA256:s+5tZfagx0zffC6gYRGW3t1KcBH6f+Vt0
  
  Ubuntu 20.04 LTS ubuntu-server sclp_line0
  ```

* At short notice, you can even log in to the system with the user 'installer' and the temporary password that was given at the end of the boot-up process (see above) of the installation system:

  ```
  user@workstation:~$ ssh installer@zvmguest
  The authenticity of host 'zvmguest (10.11.12.23)' can't be established.
  ECDSA key fingerprint is SHA256:O/dU/D8jJAEGQcbqKGE9La24IRxUPLpzzs5li9F6Vvk.
  Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
  Warning: Permanently added 'zvmguest,10.11.12.23' (ECDSA) to the list of known hosts.
  installer@zvmguest's password: 
  Welcome to Ubuntu 20.04 LTS (GNU/Linux 5.4.0-37-generic s390x)
  
   * Documentation:  https://help.ubuntu.com
   * Management:     https://landscape.canonical.com
   * Support:        https://ubuntu.com/pro
  
    System information as of Fri Jun 26 11:08:18 UTC 2020
  
    System load:    1.25      Memory usage: 4%   Processes:       192
    Usage of /home: unknown   Swap usage:   0%   Users logged in: 0
  
  0 updates can be installed immediately.
  0 of these updates are security updates.
  
  
  The list of available updates is more than a week old.
  To check for new updates run: sudo apt update
  
  
  The programs included with the Ubuntu system are free software;
  the exact distribution terms for each program are described in the
  individual files in /usr/share/doc/*/copyright.
  
  Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
  applicable law.
  
  the installer running on /dev/tty1 will perform the autoinstall
  
  press enter to start a shell
  ```

* Please note that it informs you about a currently-running autoinstall process: 

  ```
  the installer running on /dev/tty1 will perform the autoinstall
  ```

* Nevertheless, we can quickly check some things -- although, only until the autoinstall process is finished and the post-install reboot has been triggered:

  ```
  root@ubuntu-server:/# ls -l /tmp/lets_activate_the_s390x_devices 
  -rw-r--r-- 1 root root 0 Jun 26 11:08 /tmp/lets_activate_the_s390x_devices
  -rw-r--r-- 1 root root 0 Jun 26 11:09 /tmp/s390x_devices_activation_done
  
  root@ubuntu-server:/# lszdev | grep yes
  dasd-eckd    0.0.1f00                                        yes  yes   
  qeth         0.0.0600:0.0.0601:0.0.0602                      yes  no    enc600
  root@ubuntu-server:/# 
  ```

* If you wait long enough, you'll see that the remote session gets closed:

  ```
  root@ubuntu-server:/# Connection to zvmguest closed by remote host.
  Connection to zvmguest closed.
  user@workstation:~$ 
  ```

* As well as at the console:

  ```
  ubuntu-server login:
  
  [[0;1;31mFAILED[0m] Failed unmounting [0;1;39m/cdrom[0m.
  [  169.161139] sd-umoun[15600]: Failed to unmount /oldroot: Device or resource busy
  [  169.161550] sd-umoun[15601]: Failed to unmount /oldroot/cdrom: Device or resource busy
  [  169.168118] shutdown[1]: Failed to finalize  file systems, loop devices, ignoring
  Total: 282 Selected: 0
  
  Command:
  ```

* ...and that the post-install reboot got triggered:

  ```
  Message
  Mounting [0;1;39mKernel Configuration File System[0m...
  Starting [0;1;39mApply Kernel Variables[0m...
  [[0;32m  OK  [0m] Finished [0;1;39mRemount Root and Kernel File Systems[0m.
  [[0;32m  OK  [0m] Finished [0;1;39mUncomplicated firewall[0m.
  [[0;32m  OK  [0m] Mounted [0;1;39mFUSE Control File System[0m.
  [[0;32m  OK  [0m] Mounted [0;1;39mKernel Configuration File System[0m.
  ...
  [   35.378928] cloud-init[2565]: Cloud-init v. 20.1-10-g71af48df-0ubuntu5 runnin
  g 'modules:final' at Fri, 26 Jun 2020 11:10:44 +0000. Up 35.29 seconds.
  [   35.378978] cloud-init[2565]: Cloud-init v. 20.1-10-g71af48df-0ubuntu5 finish
  ed at Fri, 26 Jun 2020 11:10:44 +0000. Datasource DataSourceNone.  Up 35.37 seconds
  [   35.379008] cloud-init[2565]: 2020-06-26 11:10:44,359 - cc_final_message.py[W
  ARNING]: Used fallback datasource
  [[0;32m  OK  [0m] Finished [0;1;39mExecute cloud user/final scripts[0m.
  [[0;32m  OK  [0m] Reached target [0;1;39mCloud-init target[0m.
  
  zvmguest login:
  ```
  
* With the completion of the reboot the autoinstall is finished and the z/VM guest is ready to use:

  ```
  user@workstation:~$ ssh-keygen -f "/home/user/.ssh/known_hosts" -R "zvmguest"
  # Host zvmguest found: line 163
  /home/user/.ssh/known_hosts updated.
  Original contents retained as /home/user/.ssh/known_hosts.old
  user@workstation:~$ ssh ubuntu@zvmguest
  The authenticity of host 'zvmguest (10.11.12.23)' can't be established.
  ECDSA key fingerprint is SHA256:iGtCArEg+ZnoZlgtOkvmyy0gPY8UEI+f7zoISOF+m/0.
  Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
  Warning: Permanently added 'zvmguest,10.11.12.23' (ECDSA) to the list of known hosts.
  Welcome to Ubuntu 20.04 LTS (GNU/Linux 5.4.0-39-generic s390x)
  
   * Documentation:  https://help.ubuntu.com
   * Management:     https://landscape.canonical.com
   * Support:        https://ubuntu.com/pro
  
    System information as of Fri 26 Jun 2020 11:12:23 AM UTC
  
    System load: 0.21               Memory usage: 3%   Processes:       189
    Usage of /:  28.2% of 30.88GB   Swap usage:   0%   Users logged in: 0
  
  10 updates can be installed immediately.
  0 of these updates are security updates.
  To see these additional updates run: apt list --upgradable
  
  The programs included with the Ubuntu system are free software;
  the exact distribution terms for each program are described in the
  individual files in /usr/share/doc/*/copyright.
  
  Ubuntu comes with ABSOLUTELY NO WARRANTY,
  to the extent permitted by applicable law.
  
  To run a command as administrator (user "root"), use "sudo <command>".
  See "man sudo_root" for details.
  
  ubuntu@zvmguest:~$ uptime
   11:12:35 up 2 min,  1 user,  load average: 0.18, 0.17, 0.08
  ubuntu@zvmguest:~$ lsb_release -a
  No LSB modules are available.
  Distributor ID:	Ubuntu
  Description:	Ubuntu 20.04 LTS
  Release:	20.04
  Codename:	focal
  ubuntu@zvmguest:~$ uname -a
  Linux zvmguest 5.4.0-39-generic #43-Ubuntu SMP Fri Jun 19 10:27:17
  UTC 2020 s390x s390x s390x 
  GNU/Linux
  ubuntu@zvmguest:~$ lszdev | grep yes
  dasd-eckd    0.0.1f00                                        yes  yes   
  qeth         0.0.0600:0.0.0601:0.0.0602                      yes  yes   enc600
  ubuntu@zvmguest:~$ exit
  logout
  Connection to zvmguest closed.
  user@workstation:~$
  ```

## Some closing notes

  * It's always best to use the latest installer and autoinstall components: either make sure the installer gets updated to the latest level, or just use a current daily live-server image.

  * The ISO image specified with the kernel parameters needs to fit in the boot folder. Its kernel and initrd are specified in the 'Load from Removable Media and Server' task at the {term}`hardware management console (HMC) <HMC>`.

  * In addition to activating disk storage resources in `early-commands`, other devices like OSA/QETH can be added and activated there, too. This is not needed for the basic network device, as specified in the kernel parameters that are used for the installation (that one is automatically handled).

  * If everything is properly set up -- FTP server for the image, HTTP server for the autoinstall config files -- the installation can be as quick as 2 to 3 minutes (depending on the complexity of the autoinstall YAML file).

  * There is a simple way of generating a sample autoinstall YAML file: one can perform an interactive Subiquity installation, grab the file `/var/log/installer/autoinstall-user-data`, and use it as an example -- but beware that the `early-commands` entries to activate the s390x-specific devices need to be added manually!
