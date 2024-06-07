(interactive-live-server-installation-on-ibm-z-lpar-s390x)=
# s390x install via LPAR

Doing an interactive (manual) live installation as described here - meaning without specifying a parmfile - has been supported in Ubuntu Server since LTS 20.04.5 ('Focal').

The following guide assumes that an FTP server to host the installation files is in place, which can be used by the 'Load from Removable Media and Server' task of the Hardware Management Console (HMC).

## Download and mount the ISO

Download the ['focal daily live image' (later 20.04.5 image)](http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-s390x.iso).
   
Now loop-back mount the ISO to extract the four files that are needed for the installation:

```bash
user@workstation:~$ mkdir iso
user@workstation:~$ sudo mount -o loop ubuntu-20.04.5-live-server-s390x.iso iso
user@workstation:~$ 

user@workstation:~$ ls -1 ./iso/boot/{ubuntu.exec,parmfile.*,kernel.u*,initrd.u*}
./iso/boot/initrd.ubuntu
./iso/boot/kernel.ubuntu
./iso/boot/parmfile.ubuntu
./iso/boot/ubuntu.exec
```

## Make the files available via your FTP server.

* Open the IBM Z HMC and navigate to 'Systems Management' on your machine.

* Select the LPAR that you are going to install Ubuntu Server on. In this example we use LPAR `s1lp11`.

* Now select menu: 'Recovery' --> 'Load from Removable Media or Server' task.

* Fill out the 'Load from Removable Media or Server' form as follows (adapt the settings to your particular installation environment):

  ```text
  Load from Removable Media, or Server - <machine>:s1lp11
  Use this task to load operating system software or utility programs 
  from a CD / DVD-ROM or a server that can be accessed using FTP.
  Select the source of the software:
  o Hardware Management Console CD / DVD-ROM 
  o Hardware Management Console CD / DVD-ROM and assign for operating system use 
  o Hardware Management Console USB flash memory drive 
  o Hardware Management Console USB flash memory drive and assign for operating system use 
  * FTP Source 
     Host computer:	install-server
     User ID:	ftpuser
     Password: ********
     Account (optional):	
     File location (optional): ubuntu-live-server-20.04.5/boot
  ```
   You may need to adjust the file's location according to your install server environment.

* Confirm the entered data:

  ```text
  Load from Removable Media or Server - Select Software to Install - 
  <machine>:s1lp11
  Select the software to install.
  Select   Name                                         Description
  *  ubuntu-live-server-20.04.5/boot/ubuntu.ins     Ubuntu for IBM Z (default kernel)
  ```

* Confirm again that jobs might be cancelled if proceeding:

  ```text
  Load from Removable Media or Server Task Confirmation - 
  <machine>:s1lp11
  Load will cause jobs to be cancelled.
  Do you want to continue with this task?
  ACT33501
  ```

* And confirm a last time that it's understood that the task is disruptive:

  ```text
  Disruptive Task Confirmation : Load from Removable Media or Server - 
  <machine>:s1lp11
  
  Attention: The Load from Removable Media or Server task is disruptive.		 
  
  Executing the Load from Removable Media or Server task may
  adversely affect the objects listed below. Review the confirmation text
  for each object before continuing with the Load from Removable Media 
  or Server task.
  
  Objects that will be affected by the Load from Removable Media or
  Server task
  
  System Name       Type     OS Name     Status      Confirmation Text
  <machine>:s1lp11   Image                Operating   Load from Removable Media 
  or Server causes operations to be disrupted, since the target is
  currently in use and operating normally.

  Do you want to execute the Load from Removable Media or Server task?
  ```

* The 'Load from Removable media or Server' task is now executed:

  ```text
  Load from Removable media or Server Progress - P00B8F67:S1LPB	 
  Turn on context sensitive help. 	 
  Function duration time:	00:55:00
  Elapsed time: 00:00:04
  Select      Object Name       Status
  *           <machine> s1lp11   Please wait while the image is being loaded.
  ```

* This may take a moment, but you will soon see:

  ```
  Load from Removable media or Server Progress - <machine>:s1lp11
  Function duration time:	00:55:00
  Elapsed time:	00:00:21
  Select      Object Name       Status
  *           <machine> s1lp11   Success
  ```

* Close the 'Load from Removable media or Server' task and open the console a.k.a. 'Operating System Messages' instead. If no parmfile was configured or provided, you will find the following lines in the 'Operating System Messages' task:

  ```text
  Operating System Messages - <machine>:s1lp11
  	
  Message
  
  Unable to find a medium container a live file system
  Attempt interactive netboot from a URL?
  yes no (default yes):
  ```

* By default, you will now see the interactive network configuration menu (again, only if no parmfile was prepared with sufficient network configuration information).

* Proceed with the interactive network configuration -- in this case in a VLAN environment:

  ```text
  Unable to find a medium container a live file system
  Attempt interactive netboot from a URL?
  yes no (default yes):
  yes
  Available qeth devices:
  0.0.c000 0.0.c003 0.0.c006 0.0.c009 0.0.c00c 0.0.c00f
  zdev to activate (comma separated, optional):
  0.0.c000
  QETH device 0.0.c000:0.0.c001:0.0.c002 configured
  Two methods available for IP configuration:
  * static: for static IP configuration
  * dhcp: for automatic IP configuration
  static dhcp (default 'dhcp'):
  static
  ip:
  10.222.111.11
  gateway (default 10.222.111.1):
  10.222.111.1
  dns (default 10.222.111.1):
  10.222.111.1
  vlan id (optional):
  1234
  http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-s390x.iso (default)
  url:
  ftp://10.11.12.2:21/ubuntu-live-server-20.04.5/ubuntu-20.04.5-live-server-s390x.iso
  http_proxy (optional):
  ```

* After the last interactive step here (that this is about an optional proxy configuration), the installer will complete its boot-up process:

```text
Configuring networking...
IP-Config: encc000.1234 hardware address 3e:00:10:55:00:ff mtu 1500
IP-Config: encc000.1234 guessed broadcast address 10.222.111.255
IP-Config: encc000.1234 complete:
address: 10.222.111.11    broadcast: 10.222.111.255   netmask: 255.255.255.0
 
gateway: 10.222.111.1     dns0     : 10.222.111.1     dns1   : 0.0.0.0
 
rootserver: 0.0.0.0 rootpath:
filename  :
Connecting to 10.11.12.2:21 (10.11.12.2:21)
focal-live-server-s  10% |***                             | 72.9M  0:00:08 ETA
focal-live-server-s  25% |********                        |  168M  0:00:05 ETA
focal-live-server-s  42% |*************                   |  279M  0:00:04 ETA
focal-live-server-s  58% |******************              |  390M  0:00:02 ETA
focal-live-server-s  75% |************************        |  501M  0:00:01 ETA
focal-live-server-s  89% |****************************    |  595M  0:00:00 ETA
focal-live-server-s  99% |******************************* |  662M  0:00:00 ETA
focal-live-server-s 100% |********************************|  663M  0:00:00 ETA
ip: RTNETLINK answers: File exists
no search or nameservers found in /run/net-encc000.1234.conf / run/net-*.conf /run/net6-*.conf
[  399.808930] /dev/loop3: Can't open blockdev
[[0;1;31m SKIP [0m] Ordering cycle found, skipping [0;1;39mLogin Prompts[0m
[  401.547705] systemd[1]: multi-user.target: Job getty.target/start deleted to
break ordering cycle starting with multi-user.target/start
[  406.241972] cloud-init[1321]: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 running
'init-local' at Wed, 03 Jun 2020 17:07:39 +0000. Up 406.00 seconds.
[  407.025557] cloud-init[1348]: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 running
'init' at Wed, 03 Jun 2020 17:07:40 +0000. Up 406.87 seconds.
[  407.025618] cloud-init[1348]: ci-info:   ++++Net device info++++
[  407.025658] cloud-init[1348]: ci-info: +--------------+------+---------------
---------------+---------------+--------+-------------------+
[  407.025696] cloud-init[1348]: ci-info: |    Device    |  Up  |           Addr
ess            |      Mask     | Scope  |     Hw-Address    |
[  407.025731] cloud-init[1348]: ci-info: +--------------+------+---------------
---------------+---------------+--------+-------------------+
[  407.025766] cloud-init[1348]: ci-info: |   encc000    | True | fe80::3ca7:10f
f:fea5:c69e/64 |       .       |  link  | 72:5d:0d:09:ea:76 |
[  407.025802] cloud-init[1348]: ci-info: | encc000.1234 | True |        10.245.
236.11         | 255.255.255.0 | global | 72:5d:0d:09:ea:76 |
[  407.025837] cloud-init[1348]: ci-info: | encc000.1234 | True | fe80::3ca7:10f
f:fea5:c69e/64 |       .       |  link  | 72:5d:0d:09:ea:76 |
[  407.025874] cloud-init[1348]: ci-info: |      lo      | True |          127.0
.0.1           |   255.0.0.0   |  host  |         .         |
[  407.025909] cloud-init[1348]: ci-info: |      lo      | True |           ::1/
128            |       .       |  host  |         .         |
[  407.025944] cloud-init[1348]: ci-info: +--------------+------+---------------
---------------+---------------+--------+-------------------+
[  407.025982] cloud-init[1348]: ci-info: +++++++++++++Route I
Pv4 info++++++++++++++
[  407.026017] cloud-init[1348]: ci-info: +-------+--------------+--------------
+---------------+--------------+-------+
[  407.026072] cloud-init[1348]: ci-info: | Route | Destination  |   Gateway
|    Genmask    |  Interface   | Flags |
[  407.026107] cloud-init[1348]: ci-info: +-------+--------------+--------------
+---------------+--------------+-------+
[  407.026141] cloud-init[1348]: ci-info: |   0   |   0.0.0.0    | 10.222.111.1
|    0.0.0.0    | encc000.1234 |   UG  |
[  407.026176] cloud-init[1348]: ci-info: |   1   | 10.222.111.0 |   0.0.0.0
| 255.255.255.0 | encc000.1234 |   U   |
[  407.026212] cloud-init[1348]: ci-info: +-------+--------------+--------------
+---------------+--------------+-------+
[  407.026246] cloud-init[1348]: ci-info: ++++++++++++++++++++Route IPv6 info+++
++++++++++++++++++
[  407.026280] cloud-init[1348]: ci-info: +-------+-------------+---------+-----
---------+-------+
[  407.026315] cloud-init[1348]: ci-info: | Route | Destination | Gateway |  Int
erface   | Flags |
[  407.026355] cloud-init[1348]: ci-info: +-------+-------------+---------+-----
---------+-------+
[  407.026390] cloud-init[1348]: ci-info: |   1   |  fe80::/64  |    ::   |   en
cc000    |   U   |
[  407.026424] cloud-init[1348]: ci-info: |   2   |  fe80::/64  |    ::   | encc
000.1234 |   U   |
[  407.026458] cloud-init[1348]: ci-info: |   4   |    local    |    ::   |   en
cc000    |   U   |
[  407.026495] cloud-init[1348]: ci-info: |   5   |    local    |    ::   | encc
000.1234 |   U   |
[  407.026531] cloud-init[1348]: ci-info: |   6   |   ff00::/8  |    ::   |   en
cc000    |   U   |
[  407.026566] cloud-init[1348]: ci-info: |   7   |   ff00::/8  |    ::   | encc
000.1234 |   U   |
[  407.026600] cloud-init[1348]: ci-info: +-------+-------------+---------+-----
---------+-------+
[  407.883058] cloud-init[1348]: Generating public/private rsa key pair.
[  407.883117] cloud-init[1348]: Your identification has been saved in /etc/ssh/
ssh_host_rsa_key
[  407.883154] cloud-init[1348]: Your public key has been saved in /etc/ssh/ssh_
host_rsa_key.pub
[  407.883190] cloud-init[1348]: The key fingerprint is:
[  407.883232] cloud-init[1348]: SHA256:KX5cHC4YL9dXpvhnP6eSfS+J/zmKgg9zdlEzaEb+
RTA root@ubuntu-server
[  407.883267] cloud-init[1348]: The key's randomart image is:
[  407.883302] cloud-init[1348]: +---[RSA 3072]----+
[  407.883338] cloud-init[1348]: |           . E.. |
[  407.883374] cloud-init[1348]: |          o . o  |
[  407.883408] cloud-init[1348]: |      .   .= +o. |
[  407.883443] cloud-init[1348]: |       + =ooo++  |
[  407.883478] cloud-init[1348]: |      + S *.o.   |
[  407.883512] cloud-init[1348]: |     . = o o.    |
[  407.883546] cloud-init[1348]: |      .o+o ..+o. |
[  407.883579] cloud-init[1348]: |       o=.. =o+++|
[  407.883613] cloud-init[1348]: |        .... ++*O|
[  407.883648] cloud-init[1348]: +----[SHA256]-----+
[  407.883682] cloud-init[1348]: Generating public/private dsa key pair.
[  407.883716] cloud-init[1348]: Your identification has been saved in /etc/ssh/
ssh_host_dsa_key
[  407.883750] cloud-init[1348]: Your public key has been saved in /etc/ssh/ssh_
host_dsa_key.pub
[  407.883784] cloud-init[1348]: The key fingerprint is:
[  407.883817] cloud-init[1348]: SHA256:xu3vlG1BReKDy3DsuMZc/lg5y/+nhzlEmLDk/qFZ
Am0 root@ubuntu-server
[  407.883851] cloud-init[1348]: The key's randomart image is:
[  407.883905] cloud-init[1348]: +---[DSA 1024]----+
[  407.883941] cloud-init[1348]: |              ..o|
[  407.883975] cloud-init[1348]: |          o. o o |
[  407.884008] cloud-init[1348]: |         +.o+o+  |
[  407.884042] cloud-init[1348]: |       ...E*oo.. |
[  407.884076] cloud-init[1348]: |        S+o =..  |
[  407.884112] cloud-init[1348]: |       . +o+oo.o |
[  407.884145] cloud-init[1348]: |          **+o*o |
[  407.884179] cloud-init[1348]: |         .oo.*+oo|
[  407.884212] cloud-init[1348]: |           .+ ===|
[  407.884246] cloud-init[1348]: +----[SHA256]-----+
[  407.884280] cloud-init[1348]: Generating public/private ecdsa key pair.
[  407.884315] cloud-init[1348]: Your identification has been saved in /etc/ssh/
ssh_host_ecdsa_key
[  407.884352] cloud-init[1348]: Your public key has been saved in /etc/ssh/ssh_
host_ecdsa_key.pub
[  407.884388] cloud-init[1348]: The key fingerprint is:
[  407.884422] cloud-init[1348]: SHA256:P+hBF3fj/pu6+0KaywUYii3Lyuc09Za9/a2elCDO
gdE root@ubuntu-server
[  407.884456] cloud-init[1348]: The key's randomart image is:
[  407.884490] cloud-init[1348]: +---[ECDSA 256]---+
[  407.884524] cloud-init[1348]: |                 |
[  407.884558] cloud-init[1348]: |         .       |
[  407.884591] cloud-init[1348]: |        ..E . o  |
[  407.884625] cloud-init[1348]: |      o .ooo o . |
[  407.884660] cloud-init[1348]: |     o +S.+.. .  |
[  407.884694] cloud-init[1348]: |    . +..*oo.+ . |
[  407.884728] cloud-init[1348]: |     =  o+=.+.+  |
[  407.884762] cloud-init[1348]: |  . o......++o oo|
[  407.884795] cloud-init[1348]: |   oo.  .  +.*@*+|
[  407.884829] cloud-init[1348]: +----[SHA256]-----+
[  407.884862] cloud-init[1348]: Generating public/private ed25519 key pair.
[  407.884896] cloud-init[1348]: Your identification has been saved in /etc/ssh/
ssh_host_ed25519_key
[  407.884930] cloud-init[1348]: Your public key has been saved in /etc/ssh/ssh_
host_ed25519_key.pub
[  407.884966] cloud-init[1348]: The key fingerprint is:
[  407.884999] cloud-init[1348]: SHA256:CbZpkR9eFHuB1sCDZwSdSdwJzy9FpsIWRIyc9ers
hZ0 root@ubuntu-server
[  407.885033] cloud-init[1348]: The key's randomart image is:
[  407.885066] cloud-init[1348]: +--[ED25519 256]--+
[  407.885100] cloud-init[1348]: |       ../%X..o  |
[  407.885133] cloud-init[1348]: |       .=o&*+=   |
[  407.885167] cloud-init[1348]: |      = .+*.* .  |
[  407.885200] cloud-init[1348]: |     . B = + o   |
[  407.885238] cloud-init[1348]: |      + S . . .  |
[  407.885274] cloud-init[1348]: |     .   o o o   |
[  407.885308] cloud-init[1348]: |          + E    |
[  407.885345] cloud-init[1348]: |         . .     |
[  407.885378] cloud-init[1348]: |          .      |
[  407.885420] cloud-init[1348]: +----[SHA256]-----+
[  418.521933] cloud-init[2185]: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 runnin
g 'modules:config' at Wed, 03 Jun 2020 17:07:52 +0000. Up 418.40 seconds.
[  418.522012] cloud-init[2185]: Set the following 'random' passwords
[  418.522053] cloud-init[2185]: installer:C7BZrW76s4mJzmpf4eUy
ci-info: no authorized SSH keys fingerprints found for user installer.
<14>Jun  3 17:07:52 ec2:
<14>Jun  3 17:07:52 ec2: #######################################################
######
<14>Jun  3 17:07:52 ec2: -----BEGIN SSH HOST KEY FINGERPRINTS-----
<14>Jun  3 17:07:52 ec2: 1024 SHA256:xu3vlG1BReKDy3DsuMZc/lg5y/+nhzlEmLDk/qFZAm0
root@ubuntu-server (DSA)
<14>Jun  3 17:07:52 ec2: 256 SHA256:P+hBF3fj/pu6+0KaywUYii3Lyuc09Za9/a2elCDOgdE
root@ubuntu-server (ECDSA)
<14>Jun  3 17:07:52 ec2: 256 SHA256:CbZpkR9eFHuB1sCDZwSdSdwJzy9FpsIWRIyc9ershZ0
root@ubuntu-server (ED25519)
<14>Jun  3 17:07:52 ec2: 3072 SHA256:KX5cHC4YL9dXpvhnP6eSfS+J/zmKgg9zdlEzaEb+RTA
root@ubuntu-server (RSA)
<14>Jun  3 17:07:52 ec2: -----END SSH HOST KEY FINGERPRINTS-----
<14>Jun  3 17:07:52 ec2: #######################################################
######
-----BEGIN SSH HOST KEY KEYS-----
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBC2zp4Fq
r1+NJOIEQIISbX+EzeJ6ucXSLi2xEvurgwq8iMYT6yYOXBOPc/XzeFa6vBCDZk3SSSW6Lq83y7VmdRQ=
root@ubuntu-server
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJFzgips94nJNoR4QumiyqlJoSlZ48P+NVrd7zgD5k4T
root@ubuntu-server
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQChKo06O715FAjd6ImK7qZbWnL/cpgQ2A2gQEqFNO+1
joF/41ygxuw5aG0IQObWFpV9jDsMF5z4qHKzX8tFCpKC0s4uR8QBxh1dDm4wcwcgtAfVLqh7S4/R9Sqa
IFnkCzxThhNeMarcRrutY0mIzspmCg/QvfE1wrXJzl+RtOJ7GiuHHqpm76fX+6ZF1BYhkA87dXQiID2R
yUubSXKGg0NtzlgSzPqD3GB+HxRHHHLT5/Xq+njPq8jIUpqSoHtkBupsyVmcD9gDbz6vng2PuBHwZP9X
17QtyOwxddxk4xIXaTup4g8bH1oF/czsWqVxNdfB7XqzROFUOD9rMIB+DwBihsmH1kRik4wwLi6IH4hu
xrykKvfb1xcZe65kR42oDI7JbBwxvxGrOKx8DrEXnBpOWozS0IDm2ZPh3ci/0uCJ4LTItByyCfAe/gyR
5si4SkmXrIXf5BnErZRgyJnfxKXmsFaSh7wf15w6GmsgzyD9sI2jES9+4By32ZzYOlDpi0s= root@ub
untu-server
-----END SSH HOST KEY KEYS-----
[  418.872320] cloud-init[2203]: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 runnin
g 'modules:final' at Wed, 03 Jun 2020 17:07:52 +0000. Up 418.79 seconds.
[  418.872385] cloud-init[2203]: ci-info: no authorized SSH keys fingerprints fo
und for user installer.
[  418.872433] cloud-init[2203]: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 finish
ed at Wed, 03 Jun 2020 17:07:52 +0000. Datasource DataSourceNoCloud [seed=/var/l
ib/cloud/seed/nocloud][dsmode=net].  Up 418.86 seconds
[  418.872484] cloud-init[2203]: Welcome to Ubuntu Server Installer!
[  418.872529] cloud-init[2203]: Above you will find SSH host keys and a random
password set for the `installer` user. You can use these credentials to ssh-in a
nd complete the installation. If you provided SSH keys in the cloud-init datasou
rce, they were also provisioned to the installer user.
[  418.872578] cloud-init[2203]: If you have access to the graphical console, li
ke TTY1 or HMC ASCII terminal you can complete the installation there too.
 
It is possible to connect to the installer over the network, which
might allow the use of a more capable terminal.
 
To connect, SSH to installer@10.222.111.11.
 
The password you should use is "C7BZrW76s4mJzmpf4eUy".
 
The host key fingerprints are:
 
RSA     SHA256:KX5cHC4YL9dXpvhnP6eSfS+J/zmKgg9zdlEzaEb+RTA
ECDSA   SHA256:P+hBF3fj/pu6+0KaywUYii3Lyuc09Za9/a2elCDOgdE
ED25519 SHA256:CbZpkR9eFHuB1sCDZwSdSdwJzy9FpsIWRIyc9ershZ0
 
Ubuntu Focal Fossa (development branch) ubuntu-server sclp_line0
ubuntu-server login:
```

* At this point you can proceed with the regular installation either by using 'Recovery' --> 'Integrated ASCII Console' or with a remote SSH session.

* If the 'Integrated ASCII Console' was opened (you can hit <kbd>F3</kbd>to refresh the task), the initial Subiquity installation screen is presented, which looks like this:
```
================================================================================
  Willkommen! Bienvenue! Welcome! ????? ??????????! Welkom!           [ Help ]  
================================================================================
  Use UP, DOWN and ENTER keys to select your language.
                [ English                                    > ]
                [ Asturianu                                  > ]
                [ Cataln                                     > ]
                [ Hrvatski                                   > ]
                [ Nederlands                                 > ]
                [ Suomi                                      > ]
                [ Francais                                   > ]
                [ Deutsch                                    > ]
                [ Magyar                                     > ]
                [ Latvie?u                                   > ]
                [ Norsk bokm?l                               > ]
                [ Polski                                     > ]
                [ Espanol                                    > ]
```

* Since the user experience is nicer in a remote SSH session, we recommend using that.
However, with certain network environments it's just not possible to use a remote shell, and the 'Integrated ASCII Console' will be the only option.

> **Note**:
> At the end of the installer boot-up process, **all** necessary information is provided to proceed with a remote shell.

* The command to execute locally is:

   ```bash
   user@workstation:~$ ssh installer@10.222.111.11
   ```

* A temporary random password for the installation was created and shared as well, which you should use without the leading and trailing double quotes:
```text
"C7BZrW76s4mJzmpf4eUy"
```

* Hence the remote session for the installer can be opened by:
```bash
user@workstation:~$ ssh installer@10.222.111.11
The authenticity of host '10.222.111.11 (10.222.111.11)' can't be established.
ECDSA key fingerprint is SHA256:P+hBF3fj/pu6+0KaywUYii3Lyuc09Za9/a2elCDOgdE.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.222.111.11' (ECDSA) to the list of known hosts.
installer@10.222.111.11's password: C7BZrW76s4mJzmpf4eUy
```

* One may swiftly see some login messages like the following ones:
```
Welcome to Ubuntu Focal Fossa (development branch) (GNU/Linux 5.4.0-42-generic s390x)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

  System information as of Wed Jun  3 17:32:10 UTC 2020

  System load:    0.0       Memory usage: 2%   Processes:       146
  Usage of /home: unknown   Swap usage:   0%   Users logged in: 0

0 updates can be installed immediately.
0 of these updates are security updates.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.
```

Eventually you'll reach the initial Subiquity installer screen:

```
====================================================================
  Willkommen! Bienvenue! Welcome! ????? ??????????! Welkom!       
====================================================================
  Use UP, DOWN and ENTER keys to select your language.                        
                                                                              
                [ English                                    > ]              
                [ Asturianu                                  > ]              
                [ Cataln                                     > ]              
                [ Hrvatski                                   > ]              
                [ Nederlands                                 > ]              
                [ Suomi                                      > ]              
                [ Francais                                   > ]              
                [ Deutsch                                    > ]              
                [ Magyar                                     > ]              
                [ Latvie?u                                   > ]              
                [ Norsk bokm?l                               > ]              
                [ Polski                                     > ]              
                [ Espanol                                    > ]                                             
```
* From this point, you can follow the normal Subiquity installation. For more details, refer to the [Subquity installer documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/index.html).

(I'm leaving some pretty standard screenshots here just to give an example for a basic installation ...)
```
====================================================================
  Keyboard configuration                                          
====================================================================
  Please select your keyboard layout below, or select "Identify keyboard" to  
  detect your layout automatically.                                           
                                                                              
                 Layout:  [ English (US)                     v ]              
                                                                              
                                                                              
                Variant:  [ English (US)                     v ]              
                                                                              
                                                                              
                             [ Identify keyboard ]                            
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```
====================================================================
  Zdev setup                                                      
====================================================================
  ID                          ONLINE  NAMES                                  ^
                                                                             │
  dasd-eckd                                                                   
  0.0.1600                                     >                              
  0.0.1601                                     >                              
  0.0.1602                                     >                              
  0.0.1603                                     >                              
  0.0.1604                                     >                              
  0.0.1605                                     >                              
  0.0.1606                                     >                              
  0.0.1607                                     >                              
  0.0.1608                                     >                              
  0.0.1609                                     >                              
  0.0.160a                                     >                              
  0.0.160b                                     >                              
  0.0.160c                                     >                              
  0.0.160d                                     >                             v
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```

```                      
====================================================================
  Zdev setup                                                      
====================================================================
  ID                          ONLINE  NAMES                                  ^
                                                                             │
  dasd-eckd                                                                   
  0.0.1600                                     >┌────────────┐                
  0.0.1601                                     >│< (close)   │                
  0.0.1602                                     >│  Enable    │                
  0.0.1603                                     >│  Disable   │                
  0.0.1604                                     >└────────────┘                
  0.0.1605                                     >                              
  0.0.1606                                     >                              
  0.0.1607                                     >                              
  0.0.1608                                     >                              
  0.0.1609                                     >                              
  0.0.160a                                     >                              
  0.0.160b                                     >                              
  0.0.160c                                     >                              
  0.0.160d                                     >                             v
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```

```                             
====================================================================
  Zdev setup                                                      
====================================================================
  ID                          ONLINE  NAMES                                  ^
                                                                             │
  dasd-eckd                                                                   
  0.0.1600                                     >                              
  0.0.1601                    online  dasda    >                              
  0.0.1602                                     >                              
  0.0.1603                                     >                              
  0.0.1604                                     >                              
  0.0.1605                                     >                              
  0.0.1606                                     >                              
  0.0.1607                                     >                              
  0.0.1608                                     >                              
  0.0.1609                                     >                              
  0.0.160a                                     >                              
  0.0.160b                                     >                              
  0.0.160c                                     >                              
  0.0.160d                                     >                             v
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```

* One may hit the <kbd>End</kbd> key here -- that will automatically scroll down to the bottom of the Z devices list and screen:

```
====================================================================
  Zdev setup                                                      
====================================================================
  0.0.f1de:0.0.f1df                            >                             ^
  0.0.f1e0:0.0.f1e1                            >                              
  0.0.f1e2:0.0.f1e3                            >                              
  0.0.f1e4:0.0.f1e5                            >                              
  0.0.f1e6:0.0.f1e7                            >                              
  0.0.f1e8:0.0.f1e9                            >                              
  0.0.f1ea:0.0.f1eb                            >                              
  0.0.f1ec:0.0.f1ed                            >                              
  0.0.f1ee:0.0.f1ef                            >                              
  0.0.f1f0:0.0.f1f1                            >                              
  0.0.f1f2:0.0.f1f3                            >                              
  0.0.f1f4:0.0.f1f5                            >                              
  0.0.f1f6:0.0.f1f7                            >                              
  0.0.f1f8:0.0.f1f9                            >                              
  0.0.f1fa:0.0.f1fb                            >                              
  0.0.f1fc:0.0.f1fd                            >                             │
  0.0.f1fe:0.0.f1ff                            >                             v
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```

```                        
====================================================================
  Network connections                                             
====================================================================
  Configure at least one interface this server can use to talk to other       
  machines, and which preferably provides sufficient access for updates.      
                                                                              
    NAME          TYPE  NOTES                                                 
  [ encc000       eth   -                > ]                                  
    72:00:bb:00:aa:11 / Unknown Vendor / Unknown Model                        
                                                                              
  [ encc000.1234  vlan  -                > ]                                  
    static        10.222.111.11/24                                            
    VLAN 1234 on interface encc000                                            
                                                                              
  [ Create bond > ]                                                           
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```

* Depending on the installer version you are using you may face a little bug here.
In that case the button will be named 'Continue without network', but the network is there. If you see that, just ignore it and continue ...
(If you wait long enough the label will be refreshed and corrected.)

```
====================================================================
  Configure proxy                                                 
====================================================================
  If this system requires a proxy to connect to the internet, enter its       
  details here.                                                               
                                                                              
  Proxy address:                                                              
                  If you need to use a HTTP proxy to access the outside world,
                  enter the proxy information here. Otherwise, leave this     
                  blank.                                                      
                                                                              
                  The proxy information should be given in the standard form  
                  of "http://[[user][:pass]@]host[:port]/".                   
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```                            
====================================================================
  Configure Ubuntu archive mirror                                 
====================================================================
  If you use an alternative mirror for Ubuntu, enter its details here.        
                                                                              
  Mirror address:  http://ports.ubuntu.com/ubuntu-ports                       
                   You may provide an archive mirror that will be used instead
                   of the default.                                            
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```                             
====================================================================
  Guided storage configuration                                    
====================================================================
  Configure a guided storage layout, or create a custom one:                  
                                                                              
  (X)  Use an entire disk                                                     
                                                                              
       [ 0X1601       local disk 6.877G                                    v ]
                                                                              
       [ ]  Set up this disk as an LVM group                                  
                                                                              
            [ ]  Encrypt the LVM group with LUKS                              
                                                                              
                         Passphrase:                                          
                                                                              
                                                                              
                 Confirm passphrase:                                          
                                                                              
                                                                              
  ( )  Custom storage layout                                                  
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```                             
====================================================================
  Storage configuration                                           
====================================================================
  FILE SYSTEM SUMMARY                                                        ^
                                                                             │
    MOUNT POINT     SIZE    TYPE      DEVICE TYPE                            │
  [ /               6.875G  new ext4  new partition of local disk > ]        │
                                                                             │
                                                                             │
  AVAILABLE DEVICES                                                          │
                                                                             │
    No available devices                                                     │
                                                                             │
  [ Create software RAID (md) > ]                                            │
  [ Create volume group (LVM) > ]                                            │
                                                                              
                                                                              
  USED DEVICES                                                                
                                                                             v
                                                                              
                                 [ Done       ]                               
                                 [ Reset      ]                               
                                 [ Back       ]                               
```

```                        
====================================================================
  Storage configuration                                           
====================================================================
  FILE SYSTEM SUMMARY                                                        ^
                                                                             │

   ┌────────────────────── Confirm destructive action ──────────────────────┐
   │                                                                        │
   │  Selecting Continue below will begin the installation process and      │
   │  result in the loss of data on the disks selected to be formatted.     │
   │                                                                        │
   │  You will not be able to return to this or a previous screen once the  │
   │  installation has started.                                             │
   │                                                                        │
   │  Are you sure you want to continue?                                    │
   │                                                                        │
   │                             [ No         ]                             │
   │                             [ Continue   ]                             │
   │                                                                        │
   └────────────────────────────────────────────────────────────────────────┘

                                 [ Reset      ]                               
                                 [ Back       ]                               
```

```                        
====================================================================
  Profile setup                                                   
====================================================================
  Enter the username and password you will use to log in to the system. You   
  can configure SSH access on the next screen but a password is still needed  
  for sudo.                                                                   
                                                                              
              Your name:  Ed Example                                              
                                                                              
                                                                              
     Your server's name:  s1lp11                                              
                          The name it uses when it talks to other computers.  
                                                                              
        Pick a username:  ubuntu                                              
                                                                              
                                                                              
      Choose a password:  ********                                            
                                                                              
                                                                              
  Confirm your password:  ********                                            
                                                                              
                                                                              
                                 [ Done       ]                               
```

```
====================================================================
  SSH Setup                                                       
====================================================================
  You can choose to install the OpenSSH server package to enable secure remote
  access to your server.                                                      
                                                                              
                   [ ]  Install OpenSSH server                                
                                                                              
                                                                              
  Import SSH identity:  [ No             v ]                                  
                        You can import your SSH keys from Github or Launchpad.
                                                                              
      Import Username:                                                        
                                                                              
                                                                              
                   [X]  Allow password authentication over SSH                
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

* It's a nice and convenient new feature to add the user's SSH keys during the installation to the system, since that makes the system login password-less for the initial login!

```
====================================================================
  SSH Setup                                                       
====================================================================
  You can choose to install the OpenSSH server package to enable secure remote
  access to your server.                                                      
                                                                              
                   [X]  Install OpenSSH server                                
                                                                              
                                                                              
  Import SSH identity:  [ from Launchpad v ]                                  
                        You can import your SSH keys from Github or Launchpad.
                                                                              
   Launchpad Username:  user                                               
                        Enter your Launchpad username.                        
                                                                              
                   [X]  Allow password authentication over SSH                
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```
====================================================================
  SSH Setup                                                       
====================================================================
  You can choose to install the OpenSSH server package to enable secure remote
  access to your server.                                                      

   ┌─────────────────────────── Confirm SSH keys ───────────────────────────┐
   │                                                                        │
   │  Keys with the following fingerprints were fetched. Do you want to     │
   │  use them?                                                             │
   │                                                                        │
   │  2048 SHA256:joGscmiamcaoincinaäonnväineorviZEdDWdR9Hpbc2KIw user@W520  │
   │   (RSA)                                                                │
   │  521 SHA256:T3JzxvB6K1Gzidvoidhoidsaoicak0jhhgvbw01F7/fZ2c                │
   │  ed.example@acme.com  (ECDSA)                                   │
   │                                                                        │
   │                             [ Yes        ]                             │
   │                             [ No         ]                             │
   │                                                                        │
   └────────────────────────────────────────────────────────────────────────┘

                                 [ Done       ]                               
                                 [ Back       ]                               
```

```
====================================================================
  Featured Server Snaps                                           
====================================================================
  These are popular snaps in server environments. Select or deselect with     
  SPACE, press ENTER to see more details of the package, publisher and        
  versions available.                                                         
                                                                              
  [ ] kata-containers Lightweight virtual machines that seamlessly plug into >
  [ ] docker          Docker container runtime                               >
  [ ] mosquitto       Eclipse Mosquitto MQTT broker                          >
  [ ] etcd            Resilient key-value store by CoreOS                    >
  [ ] stress-ng       A tool to load, stress test and benchmark a computer s >
  [ ] sabnzbd         SABnzbd                                                >
  [ ] wormhole        get things from one computer to another, safely        >
  [ ] slcli           Python based SoftLayer API Tool.                       >
  [ ] doctl           DigitalOcean command line tool                         >
  [ ] keepalived      High availability VRRP/BFD and load-balancing for Linu >
  [ ] juju            Simple, secure and stable devops. Juju keeps complexit >
                                                                              
                                                                              
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```                                      
====================================================================
  Install complete!                                               
====================================================================
  ┌──────────────────────────────────────────────────────────────────────────┐
  │          configuring raid (mdadm) service                               ^│
  │          installing kernel                                               │
  │          setting up swap                                                 │
  │          apply networking config                                         │
  │          writing etc/fstab                                               │
  │          configuring multipath                                           │
  │          updating packages on target system                              │
  │          configuring pollinate user-agent on target                      │
  │          updating initramfs configuration                                │
  │    finalizing installation                                               │
  │      running 'curtin hook'                                               │
  │        curtin command hook                                               │
  │    executing late commands                                               │
  │final system configuration                                                │
  │  configuring cloud-init                                                 ││
  │  installing openssh-server \                                            v│
  └──────────────────────────────────────────────────────────────────────────┘

                               [ View full log ]
```

```
====================================================================
  Installation complete!                                          
====================================================================
  ┌──────────────────────────── Finished install! ───────────────────────────┐
  │          apply networking config                                        ^│
  │          writing etc/fstab                                               │
  │          configuring multipath                                           │
  │          updating packages on target system                              │
  │          configuring pollinate user-agent on target                      │
  │          updating initramfs configuration                                │
  │    finalizing installation                                               │
  │      running 'curtin hook'                                               │
  │        curtin command hook                                               │
  │    executing late commands                                               │
  │final system configuration                                                │
  │  configuring cloud-init                                                  │
  │  installing openssh-server                                               │
  │  restoring apt configuration                                            ││
  │downloading and installing security updates                              v│
  └──────────────────────────────────────────────────────────────────────────┘

                               [ View full log ]
                               [ Reboot        ]
```

```
  Installation complete!                                          
====================================================================
  ┌──────────────────────────── Finished install! ───────────────────────────┐
  │          apply networking config                                        ^│
  │          writing etc/fstab                                               │
  │          configuring multipath                                           │
  │          updating packages on target system                              │
  │          configuring pollinate user-agent on target                      │
  │          updating initramfs configuration                                │
  │    finalizing installation                                               │
  │      running 'curtin hook'                                               │
  │        curtin command hook                                               │
  │    executing late commands                                               │
  │final system configuration                                                │
  │  configuring cloud-init                                                  │
  │  installing openssh-server                                               │
  │  restoring apt configuration                                            ││
  │downloading and installing security updates                              v│
  └──────────────────────────────────────────────────────────────────────────┘

                               [ Connection to 10.222.111.11 closed by remote host.                            [ Rebooting...  ]
Connection to 10.222.111.11 closed.
user@workstation:~$ 
```

* Now type `reset` to clear the screen and reset it to its defaults.

* Before proceeding one needs to remove the old, temporary host key of the target system, since it was only for use during the installation:

  ```
  user@workstation:~$ ssh-keygen -f "/home/user/.ssh/known_hosts" -R "s1lp11"
  # Host s1lp11 found: line 159
  /home/user/.ssh/known_hosts updated.
  Original contents retained as /home/user/.ssh/known_hosts.old
  user@workstation:~$
  ```
* And assuming the post-installation reboot is done, one can now login:

  ```
  user@workstation:~$ ssh ubuntu@s1lp11
  Warning: Permanently added the ECDSA host key for IP address
  '10.222.111.11' to the list of known hosts.
  Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-42-generic s390x)
   
   * Documentation:  https://help.ubuntu.com
   * Management:     https://landscape.canonical.com
   * Support:        https://ubuntu.com/pro
  
    System information as of Wed 03 Jun 2020 05:50:05 PM UTC
  
    System load: 0.08              Memory usage: 2%   Processes:       157
    Usage of /:  18.7% of 6.70GB   Swap usage:   0%   Users logged in: 0
  
  0 updates can be installed immediately.
  0 of these updates are security updates.
  
  The programs included with the Ubuntu system are free software;
  the exact distribution terms for each program are described in the
  individual files in /usr/share/doc/*/copyright.
  
  Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.
  
  To run a command as administrator (user "root"), use "sudo <command>".
  See "man sudo_root" for details.
  
  ubuntu@s1lp11:~$ uptime
   17:50:09 up 1 min,  1 user,  load average: 0.08, 0.11, 0.05
  ubuntu@s1lp11:~$ lsb_release -a
  No LSB modules are available.
  Distributor ID:	Ubuntu
  Description:	Ubuntu 20.04.5 LTS
  Release:	20.04
  Codename:	focal
  ubuntu@s1lp11:~$ uname -a
  Linux s1lp11 5.4.0-42-generic #30-Ubuntu SMP Wed Aug 05 16:57:22 UTC 2020 s390x s390x s390x GNU/Linux
  ubuntu@s1lp11:~$ exit
  logout
  Connection to s1lp11 closed.
  user@workstation:~$
  ```

Done !
