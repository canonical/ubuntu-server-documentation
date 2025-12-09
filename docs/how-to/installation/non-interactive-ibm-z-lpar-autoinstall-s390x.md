---
myst:
  html_meta:
    description: Automated Ubuntu Server installation on IBM Z LPAR (s390x) using autoinstall with zFCP storage and VLAN network configuration.
---

(non-interactive-ibm-z-lpar-autoinstall-s390x)=
# Non-interactive IBM Z LPAR autoinstall (s390x)

This non-interactive installation uses `autoinstall`, which can be considered the successor to the Debian installer (d-i) and `preseed` on Ubuntu. This is a detailed step-by-step guide, including output and logs (which are partially a bit shortened, as indicated by `…`, to limit the size of this document).

The example logical partition (LPAR) here uses zFCP storage and is connected to a VLAN network.
For a {term}`DASD` and a non-VLAN network example, please see the [non-interactive IBM z/VM (s390x) auto-installation](https://discourse.ubuntu.com/t/non-interactive-ibm-z-vm-s390x-installation-using-autoinstall/16995) guide.

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

* The ISO image needs to be extracted now. Since files in its boot folder need to be modified, loopback mount is not an option here:

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
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ rsync -rtvz ./iso/ . && sync
  sending incremental file list
  skipping non-regular file "ubuntu"
  skipping non-regular file "ubuntu-ports"
  ./
  README.diskdefines
  boot.catalog
  md5sum.txt
  ubuntu.ins
  skipping non-regular file "dists/stable"
  skipping non-regular file "dists/unstable"
  .disk/
  .disk/base_installable
  .disk/casper-uuid-generic
  .disk/cd_type
  .disk/info
  boot/
  boot/README.boot
  boot/initrd.off
  boot/initrd.siz
  boot/initrd.ubuntu
  boot/kernel.ubuntu
  boot/parmfile.ubuntu
  boot/ubuntu.exec
  boot/ubuntu.ikr
  boot/ubuntu.ins
  casper/
    ...
  sent 681,509,758 bytes  received 1,857 bytes  22,344,643.11 bytes/sec
  total size is 700,317,941  speedup is 1.03
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ ls -l
  total 684578
  dr-xr-xr-x  2 user user      4096 Jun 26 10:12 boot
  -r--r--r--  1 user user      2048 Jun 26 10:12 boot.catalog
  dr-xr-xr-x  3 user user      4096 Jun 26 10:12 casper
  dr-xr-xr-x  3 user user      4096 Jun 26 10:11 dists
  -rw-rw-r--  1 user user 700952576 Jun 26 10:12 focal-live-server-s390x.iso
  dr-xr-xr-x  2 user user      4096 Jun 26 10:11 install
  dr-xr-xr-x 10 root    root         2048 Jun 26 10:12 iso
  -r--r--r--  1 user user      4944 Jun 26 10:12 md5sum.txt
  dr-xr-xr-x  2 user user      4096 Jun 26 10:11 pics
  dr-xr-xr-x  3 user user      4096 Jun 26 10:11 pool
  dr-xr-xr-x  2 user user      4096 Jun 26 10:11 preseed
  -r--r--r--  1 user user       236 Jun 26 10:11 README.diskdefines
  -r--r--r--  1 user user       185 Jun 26 10:12 ubuntu.ins
  ```

* Now create `.ins` and parmfiles dedicated to the LPAR that will be installed (here `zlinlpar`), based on the default `.ins` and parmfiles that are shipped with the ISO image:

  ```bash
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ chmod -R +rw ./boot
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ cp ./boot/ubuntu.ins ./boot/ubuntu_zlinlpar.ins
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ cp ./boot/parmfile.ubuntu ./boot/parmfile.zlinlpar
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ 
  ```
  ```bash  
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ vi ./boot/ubuntu_zlinlpar.ins
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ cat ./boot/ubuntu_zlinlpar.ins
  * Ubuntu for z Series (default kernel)
  kernel.ubuntu 0x00000000
  initrd.off 0x0001040c
  initrd.siz 0x00010414
  parmfile.zlinlpar 0x00010480
  initrd.ubuntu 0x01000000
  admin@installserver:~$ 
    ```
    ```bash
    admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ vi ./boot/parmfile.zlinlpar
    admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ cat ./boot/parmfile.zlinlpar
    ```
    ```bash
   ip=10.11.12.42::10.11.12.1:255.255.255.0:zlinlpar:encc000.4711:none:10.11.12.1 vlan=encc000.4711:encc000 url=http://installserver.local:80/ubuntu-daily-live-server-20.04/focal-live-server-s390x.iso autoinstall ds=nocloud-net;s=http://installserver.local:80/autoinstall/zlinlpar/ --- quiet
   ```

* Now make sure an FTP server is running in the `installserver` with `/srv/ftp` as ftp-server root (as used in this example).

* Now prepare an *autoinstall* (HTTP) server, which hosts the configuration data for the non-interactive installation.

  ```bash
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ mkdir -p /srv/www/autoinstall/zlinlpar
  admin@installserver:/srv/ftp/ubuntu-daily-live-server-20.04$ cd /srv/www/autoinstall/zlinlpar
  admin@installserver:/srv/www/autoinstall/zlinlpar$ 
  admin@installserver:/srv/www/autoinstall/zlinlpar$ echo "instance-id: $(uuidgen || openssl rand -base64 8)" > meta-data
  admin@installserver:/srv/www/autoinstall/zlinlpar$ cat meta-data
  instance-id: 2c2215fb-6a38-417f-b72f-376b1cc44f01
  admin@installserver:/srv/www/autoinstall/zlinlpar$
  ```
  ```bash
  admin@installserver:/srv/www/autoinstall/zlinlpar$ vi user-data
  admin@installserver:/srv/www/autoinstall/zlinlpar$ cat user-data
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
      hostname: zlinlpar
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
        - chzdev zfcp -e e000
        - chzdev zfcp -e e100
        - chzdev zfcp-lun -e --online
        - touch /tmp/s390x_devices_activation_done
      network:
        ethernets:
          encc000: {}
        version: 2
        vlans:
          encc000.4711:
            addresses: [10.11.12.42/24]
            gateway4: 10.11.12.1
            id: 4711
            link: encc000
            nameservers:
              addresses: [10.11.12.1]
      ssh:
        install-server: true
        allow-pw: true
        authorized-keys: ['ssh-rsa  meQwtZ user@workstation # ssh-import-id lp:user']
    admin@installserver:~$
  ```

* For s390x installations the `early-commands` section is the interesting part:

  ```bash
  early-commands:
    - touch /tmp/lets_activate_the_s390x_devices
    - chzdev zfcp -e e000
    - chzdev zfcp -e e100
    - chzdev zfcp-lun -e --online
    - touch /tmp/s390x_devices_activation_done
  ```
  The first and last `early-commands` are optional; they only frame and indicate the real s390x command activation.

  In this particular example, two zFCP hosts (host-bus-adapters) are enabled via their addresses *e000* (`chzdev zfcp -e e000`) and *e100* (`chzdev zfcp -e e000`). These have certain logical unit numbers (LUNs) assigned that are all automatically discovered and activated by `chzdev zfcp-lun -e --online`.

  Activation of a direct-access storage device (DASD) would look like this: `chzdev dasd -e 1f00`, and a QETH device activation looks like: `chzdev qeth -e c000`.

```{seealso}
For more details about the autoinstall config options, please have a look at the [autoinstall reference](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html) and [autoinstall schema](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-schema.html) pages.
```

* Now make sure a HTTP server is running with `/srv/www` as web-server root (in this particular example).

* Next steps need to be done at the {term}`hardware management console (HMC) <HMC>`. First, connect to the HMC and proceed with the 'Load From Removable Media and Server' task.

* Then, start the 'Load from Removable Media or Server' task under 'Recovery' --> 'Load from Removable Media or Server' on your specific LPAR that you are going to install, and fill out the following fields (the contents will be of course different on your system):

  ```bash
  FTP Source 	
  Host computer:	installserver.local
  User ID:	ftpuser
  Password: ********
  Account (optional):	
  File location (optional): ubuntu-daily-live-server-20.04/boot
  ```

* Now confirm the entered data and click 'OK'.

* At the 'Load from Removable Media or Server - Select Software to Install' screen, choose the LPAR that is going to be installed, here:

  ```bash
  ubuntu-daily-live-server-20.04/boot/ubuntu_zlinlpar.ins   Ubuntu for z Series (default kernel)
  ```

* Confirm again with 'OK'.

* And another confirmation about the 'Load will cause jobs to be cancelled'.

* Then, another 'Yes' -- understanding that it's a disruptive task:

  ```bash
  Disruptive Task Confirmation : Load from Removable Media or Server
  ```

* Now monitor the 'Load from Removable media or Server Progress' screen and confirm it once again when the status changes from 'Please wait while the image is being loaded.' to 'Success'.

* Then navigate to 'Daily' --> 'Operating System Messages' to monitor the initial program load (IPL) of the install system ...

  ```bash
  Message
  chzdev: Unknown device type or device ID format: c000.4711
  Use 'chzdev --help' for more information
  QETH device 0.0.c000:0.0.c001:0.0.c002 configured
  IP-Config: encc000.4711 hardware address 1a:3c:99:55:2a:ef mtu 1500
  IP-Config: encc000.4711 guessed broadcast address 10.11.12.255
  IP-Config: encc000.4711 complete:
  address: 10.11.12.42    broadcast: 10.11.12.255   netmask: 255.255.255.0
  
  gateway: 10.11.12.1     dns0     : 10.11.12.1     dns1   : 0.0.0.0
  
  host   : zlinlpar
  rootserver: 0.0.0.0 rootpath:
  filename  :
  Connecting to installserver.local:80 (installserver.local:80)
  focal-live-server-s3   5% |*                               | 39.9M  0:00:15 ETA
  focal-live-server-s3  22% |*******                         |  147M  0:00:07 ETA
  focal-live-server-s3  38% |************                    |  254M  0:00:04 ETA
  focal-live-server-s3  53% |*****************               |  355M  0:00:03 ETA
  focal-live-server-s3  67% |*********************           |  453M  0:00:02 ETA
  focal-live-server-s3  81% |**************************      |  545M  0:00:01 ETA
  focal-live-server-s3  94% |*****************************  |  633M  0:00:00 ETA
  focal-live-server-s3 100% |******************************|  668M  0:00:00 ETA
  mount: mounting /cow on /root/cow failed: No such file or directory
  Connecting to plymouth: Connection refused
  passwd: password expiry information changed.
  Using CD-ROM mount point /cdrom/
  Identifying... [5d25356068b713167814807dd678c261-2]
  Scanning disc for index files...
  Found 2 package indexes, 0 source indexes, 0 translation indexes and 1 signature
  Found label 'Ubuntu-Server 20.04 LTS _Focal Fossa_ - Release s390x (20200616)'
  This disc is called:
  'Ubuntu-Server 20.04 LTS _Focal Fossa_ - Release s390x (20200616)'
  ...
  [   61.190916] cloud-init[2076]: Cloud-init v. 20.1-10-g71af48df-0ubuntu5 running
  'modules:final' at Fri, 26 Jun 2020 11:02:01 +0000. Up 61.09 seconds.
  [   61.191002] cloud-init[2076]: ci-info: no authorized SSH keys fingerprints fo
  und for user installer.
  [   61.191071] cloud-init[2076]: Cloud-init v. 20.1-10-g71af48df-0ubuntu5 finished at Fri, 26 Jun 2020 11:02:01 +0000.
  Datasource DataSourceNoCloudNet [seed=cmdline,
  /var/lib/cloud/seed/nocloud,
  http://installserver.local:80/autoinstall/zlinlpar/]
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
  
  To connect, SSH to installer@10.11.12.42.
  
  The password you should use is ''i7UFdP8fhiVVMme3qqH8''.
  
  The host key fingerprints are:
  
  RSA     SHA256:rBXLeUke3D4gKdsruKEajHjocxc9hr3PI
  ECDSA   SHA256:KZZYFswtKxFXWQPuQS9QpOBUoS6RHswis
  ED25519 SHA256:s+5tZfagx0zffC6gYRGW3t1KcBH6f+Vt0
  
  Ubuntu 20.04 LTS ubuntu-server sclp_line0
  ```
  
* At short notice, you can even log in to the system with the user 'installer' and the temporary password that was given at the end of the boot-up process (see above) of the installation system:

  ```bash
  user@workstation:~$ ssh installer@zlinlpar
  The authenticity of host 'zlinlpar (10.11.12.42)' can't be established.
  ECDSA key fingerprint is SHA256:O/dU/D8jJAEGQcbqKGE9La24IRxUPLpzzs5li9F6Vvk.
  Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
  Warning: Permanently added 'zlinlpar,10.11.12.42' (ECDSA) to the list of known hosts.
  installer@zlinlpar's password: 
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

* Notice that it informs you about a currently-running autoinstall process:
 
  ```bash
  the installer running on /dev/tty1 will perform the autoinstall
  ```

* Nevertheless, we can quickly check some things -- though only until the autoinstall process has finished and the post-install reboot has been triggered:

  ```
  root@ubuntu-server:/# ls -l /tmp/lets_activate_the_s390x_devices 
  -rw-r--r-- 1 root root 0 Jun 26 11:08 /tmp/lets_activate_the_s390x_devices
  -rw-r--r-- 1 root root 0 Jun 26 11:09 /tmp/s390x_devices_activation_done
  
  root@ubuntu-server:/# lszdev | grep yes
  zfcp-host    0.0.e000                                        yes  yes   
  zfcp-host    0.0.e100                                        yes  yes   
  zfcp-lun     0.0.e000:0x50050763060b16b6:0x4026400200000000  yes  yes   sdb sg1
  zfcp-lun     0.0.e000:0x50050763061b16b6:0x4026400200000000  yes  yes   sda sg0
  zfcp-lun     0.0.e100:0x50050763060b16b6:0x4026400200000000  yes  yes   sdd sg3
  zfcp-lun     0.0.e100:0x50050763061b16b6:0x4026400200000000  yes  yes   sdc sg2
  qeth         0.0.c000:0.0.c001:0.0.c002                      yes  no    encc000
  root@ubuntu-server:/# 
  ```

* If you wait long enough you'll see the remote session get closed:

  ```bash
  root@ubuntu-server:/# Connection to zlinlpar closed by remote host.
  Connection to zlinlpar closed.
  user@workstation:~$ 
  ```

* As well as at the console:

  ```bash
  ubuntu-server login:
  
  [[0;1;31mFAILED[0m] Failed unmounting [0;1;39m/cdrom[0m.
  [  169.161139] sd-umoun[15600]: Failed to unmount /oldroot: Device or resource busy
  [  169.161550] sd-umoun[15601]: Failed to unmount /oldroot/cdrom: Device or resource busy
  [  169.168118] shutdown[1]: Failed to finalize  file systems, loop devices, ignoring
  Total: 282 Selected: 0
  
  Command:
  ```

* ...and that the post-install reboot gets triggered:

  ```bash
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
  
  zlinlpar login:
  ```
  
* With the completion of the reboot, the autoinstall is finished and the LPAR is ready to use:

  ```
  user@workstation:~$ ssh-keygen -f "/home/user/.ssh/known_hosts" -R "zlinlpar"
  # Host zlinlpar found: line 163
  /home/user/.ssh/known_hosts updated.
  Original contents retained as /home/user/.ssh/known_hosts.old
  user@workstation:~$ ssh ubuntu@zlinlpar
  The authenticity of host 'zlinlpar (10.11.12.42)' can't be established.
  ECDSA key fingerprint is SHA256:iGtCArEg+ZnoZlgtOkvmyy0gPY8UEI+f7zoISOF+m/0.
  Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
  Warning: Permanently added 'zlinlpar,10.11.12.42' (ECDSA) to the list of known hosts.
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
  
  ubuntu@zlinlpar:~$ uptime
   11:12:35 up 2 min,  1 user,  load average: 0.18, 0.17, 0.08
  ubuntu@zlinlpar:~$ lsb_release -a
  No LSB modules are available.
  Distributor ID:	Ubuntu
  Description:	Ubuntu 20.04 LTS
  Release:	20.04
  Codename:	focal
  ubuntu@zlinlpar:~$ uname -a
  Linux zlinlpar 5.4.0-39-generic #43-Ubuntu SMP Fri Jun 19 10:27:17
  UTC 2020 s390x s390x s390x 
  GNU/Linux
  ubuntu@zlinlpar:~$ lszdev | grep yes
  zfcp-host    0.0.e000                                        yes  yes   
  zfcp-host    0.0.e100                                        yes  yes   
  zfcp-lun     0.0.e000:0x50050763060b16b6:0x4026400200000000  yes  yes   
  sdb sg1
  zfcp-lun     0.0.e000:0x50050763061b16b6:0x4026400200000000  yes  yes   
  sda sg0
  zfcp-lun     0.0.e100:0x50050763060b16b6:0x4026400200000000  yes  yes   
  sdc sg2
  zfcp-lun     0.0.e100:0x50050763061b16b6:0x4026400200000000  yes  yes   
  sdd sg3
  qeth         0.0.c000:0.0.c001:0.0.c002                      yes  yes   encc000
  ubuntu@zlinlpar:~$ exit
  logout
  Connection to zlinlpar closed.
  user@workstation:~$
  ```

## Some closing notes
  * It's always best to use the latest installer and autoinstall components. Be sure to update the installer to the most recent version, or just use a current daily live-server image.

  * The ISO image specified with the kernel parameters needs to fit in the boot folder. Its kernel and initrd are specified in the 'Load from Removable Media and Server' task at the hardware management console (HMC).

  * In addition to activating disk storage resources in `early-commands`, other devices like OSA/QETH can be added and activated there, too. This is not needed for the basic network device, as specified in the kernel parameters used for the installation (that one is automatically handled).

  * If everything is properly set up -- FTP server for the image, HTTP server for the autoinstall config files -- the installation can be as quick as 2 to 3 minutes. Of course this depends on the complexity of the autoinstall YAML file.

  * There is a simple way of generating a sample autoinstall YAML file; one can perform an interactive Subiquity installation, grab the file `/var/log/installer/autoinstall-user-data`, and use it as an example -- but beware that the `early-commands` entries to activate the s390x-specific devices need to be added manually!
