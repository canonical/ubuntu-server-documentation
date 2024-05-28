# Interactive live server installation on IBM z/VM (s390x)

Doing an interactive (manual) live installation as described here - meaning without specifying a parmfile - has been supported in Ubuntu Server since LTS 20.04.5 ('Focal').

The following guide assumes that a z/VM guest has been defined, and that it is able to either reach the public `cdimage.ubuntu.com` server or an internal FTP or HTTP server that hosts an Ubuntu Server 20.04 installer image, like this [20.04 (a.k.a. Focal) daily live image](http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-s390x.iso)

Find a place to download the installer image:

```bash
user@workstation:~$ wget 
http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-s390x.iso
--2020-08-08 16:01:52--  
http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-s390x.iso
Resolving cdimage.ubuntu.com (cdimage.ubuntu.com)... 2001:67c:1560:8001::1d, 2001:67c:1360:8001::27, 2001:67c:1360:8001::28, ...
Connecting to cdimage.ubuntu.com 
(cdimage.ubuntu.com)|2001:67c:1560:8001::1d|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 705628160 (673M) [application/x-iso9660-image]
Saving to: ‘ubuntu-20.04.5-live-server-s390x.iso’

ubuntu-20.04.5-live 100%[===================>] 672.94M  37.1MB/s    in 
17s     

2020-08-08 16:02:10 (38.8 MB/s) - ‘ubuntu-20.04.5-live-server-s390x.iso’ saved 
[705628160/705628160]
```

Now loop-back mount the ISO to extract four files that are needed for a z/VM guest installation:

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

Now transfer these four files to your z/VM guest (for example to its 'A' file mode), using either the 3270 terminal emulator or FTP.

Then log on to the z/VM guest that you want to use for the installation. In this example it will be guest '10.222.111.24'.

Execute the `ubuntu` REXX script to kick-off the installation:

```text
ubuntu
00: 0000004 FILES PURGED
00: RDR FILE 0125 SENT FROM 10.222.111.24  PUN WAS 0125 RECS 101K CPY  001 A NOHOLD NO
KEEP
00: RDR FILE 0129 SENT FROM 10.222.111.24  PUN WAS 0129 RECS 0001 CPY  001 A NOHOLD NO
KEEP
00: RDR FILE 0133 SENT FROM 10.222.111.24  PUN WAS 0133 RECS 334K CPY  001 A NOHOLD NO
KEEP
00: 0000003 FILES CHANGED
00: 0000003 FILES CHANGED
01: HCPGSP2627I The virtual machine is placed in CP mode due to a SIGP initial CPU reset from CPU 00.
02: HCPGSP2627I The virtual machine is placed in CP mode due to a SIGP initial CPU reset from CPU 00.
03: HCPGSP2627I The virtual machine is placed in CP mode due to a SIGP initial CPU reset from CPU 00.
¬    0.390935| Initramfs unpacking failed: Decoding failed 
Unable to find a medium container a live file system 
```

In the usual case that no parmfile was configured, the installation system now offers to interactively configure the basic network:

```text
Attempt interactive netboot from a URL? 
yes no (default yes): yes
Available qeth devices: 
0.0.0600 0.0.0603 
zdev to activate (comma separated, optional): 0600
QETH device 0.0.0600:0.0.0601:0.0.0602 configured 
Two methods available for IP configuration: 
  * static: for static IP configuration 
  * dhcp: for automatic IP configuration 
static dhcp (default 'dhcp'): static
ip: 10.222.111.24
gateway (default 10.222.111.1): .
dns (default .): 
vlan id (optional): 
 http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-s390x.iso (default) 
url: ftp://10.11.12.2:21/ubuntu-live-server-20.04.5/ubuntu-20.04.5-live-server-s390x.iso
http_proxy (optional):  
```

Ensure that the same version of the ISO image that was used to extract the installer files -- kernel and initrd -- is referenced at the '`url:`' setting. It can be at a different location, for example directly referencing the public `cdimage.ubuntu.com` server: `http://cdimage.ubuntu.com/ubuntu/releases/20.04.5/release/ubuntu-20.04.5-live-server-s390x.iso`

The boot-up of the live-server installation now completes:

```text
Configuring networking... 
QETH device 0.0.0600:0.0.0601:0.0.0602 already configured 
IP-Config: enc600 hardware address 02:28:0a:00:00:39 mtu 1500 
IP-Config: enc600 guessed broadcast address 10.222.111255 
IP-Config: enc600 complete: 
 address: 10.222.111.24    broadcast: 10.222.111255   netmask: 255.255.255.0   
 
 gateway: 10.222.111.1     dns0     : 10.222.111.1     dns1   : 0.0.0.0         
 
 rootserver: 0.0.0.0 rootpath:  
 filename  :  
Connecting to 10.11.12.2:21 (10.11.12.2:21) 
focal-live-server-s   5% !*                               ! 35.9M  0:00:17 ETA 
focal-live-server-s  19% !******                          !  129M  0:00:08 ETA 
focal-live-server-s  33% !**********                      !  225M  0:00:05 ETA 
focal-live-server-s  49% !***************                 !  330M  0:00:04 ETA 
focal-live-server-s  60% !*******************             !  403M  0:00:03 ETA 
focal-live-server-s  76% !************************        !  506M  0:00:01 ETA 
focal-live-server-s  89% !****************************    !  594M  0:00:00 ETA 
focal-live-server-s 100% !********************************!  663M  0:00:00 ETA 
passwd: password expiry information changed. 
QETH device 0.0.0600:0.0.0601:0.0.0602 already configured 
no search or nameservers found in /run/net-enc600.conf /run/net-*.conf /run/net6
-*.conf 
¬  594.766372| /dev/loop3: Can't open blockdev 
¬  595.610434| systemd¬1|: multi-user.target: Job getty.target/start deleted to 
break ordering cycle starting with multi-user.target/start 
¬ ¬0;1;31m SKIP  ¬0m| Ordering cycle found, skipping  ¬0;1;39mLogin Prompts ¬0m 
¬  595.623027| systemd¬1|: Failed unmounting /cdrom. 
¬ ¬0;1;31mFAILED ¬0m| Failed unmounting  ¬0;1;39m/cdrom ¬0m. 
 
¬  598.973538| cloud-init¬1256|: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 runnin
g 'init-local' at Thu, 04 Jun 2020 12:06:46 +0000. Up 598.72 seconds. 
¬  599.829069| cloud-init¬1288|: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 runnin
g 'init' at Thu, 04 Jun 2020 12:06:47 +0000. Up 599.64 seconds. 
¬  599.829182| cloud-init¬1288|: ci-info: ++++++++++++++++++++++++++++++++++++Ne
t device info+++++++++++++++++++++++++++++++++++++ 
¬  599.829218| cloud-init¬1288|: ci-info: +--------+------+---------------------
----+---------------+--------+-------------------+ 
¬  599.829255| cloud-init¬1288|: ci-info: ! Device !  Up  !         Address     
    !      Mask     ! Scope  !     Hw-Address    ! 
¬  599.829292| cloud-init¬1288|: ci-info: +--------+------+---------------------
----+---------------+--------+-------------------+ 
¬  599.829333| cloud-init¬1288|: ci-info: ! enc600 ! True !      10.222.111.24  
    ! 255.255.255.0 ! global ! 02:28:0a:00:00:39 ! 
¬  599.829376| cloud-init¬1288|: ci-info: ! enc600 ! True ! fe80::28:aff:fe00:3
/64 !       .       !  link  ! 02:28:0a:00:00:39 ! 
¬  599.829416| cloud-init¬1288|: ci-info: !   lo   ! True !        127.0.0.1    
    !   255.0.0.0   !  host  !         .         ! 
¬  599.829606| cloud-init¬1288|: ci-info: !   lo   ! True !         ::1/128     
    !       .       !  host  !         .         ! 
¬  599.829684| cloud-init¬1288|: ci-info: +--------+------+---------------------
----+---------------+--------+-------------------+ 
¬  599.829721| cloud-init¬1288|: ci-info: ++++++++++++++++++++++++++++++Route IP
v4 info++++++++++++++++++++++++++++++ 
¬  599.829754| cloud-init¬1288|: ci-info: +-------+--------------+--------------
+---------------+-----------+-------+ 
¬  599.829789| cloud-init¬1288|: ci-info: ! Route ! Destination  !   Gateway    
!    Genmask    ! Interface ! Flags ! 
¬  599.829822| cloud-init¬1288|: ci-info: +-------+--------------+--------------
+---------------+-----------+-------+ 
¬  599.829858| cloud-init¬1288|: ci-info: !   0   !   0.0.0.0    ! 10.222.111.1 
!    0.0.0.0    !   enc600  !   UG  ! 
¬  599.829896| cloud-init¬1288|: ci-info: !   1   ! 10.222.1110 !   0.0.0.0    
! 255.255.255.0 !   enc600  !   U   ! 
¬  599.829930| cloud-init¬1288|: ci-info: +-------+--------------+--------------
+---------------+-----------+-------+ 
¬  599.829962| cloud-init¬1288|: ci-info: +++++++++++++++++++Route IPv6 info++++
+++++++++++++++ 
¬  599.829998| cloud-init¬1288|: ci-info: +-------+-------------+---------+-----
------+-------+ 
¬  599.830031| cloud-init¬1288|: ci-info: ! Route ! Destination ! Gateway ! Inte
rface ! Flags ! 
¬  599.830064| cloud-init¬1288|: ci-info: +-------+-------------+---------+-----
------+-------+ 
¬  599.830096| cloud-init¬1288|: ci-info: !   1   !  fe80::/64  !    ::   !   en
c600  !   U   ! 
¬  599.830131| cloud-init¬1288|: ci-info: !   3   !    local    !    ::   !   en
c600  !   U   ! 
¬  599.830164| cloud-init¬1288|: ci-info: !   4   !   ff00::/8  !    ::   !   en
c600  !   U   ! 
¬  599.830212| cloud-init¬1288|: ci-info: +-------+-------------+---------+-----
------+-------+ 
¬  601.077953| cloud-init¬1288|: Generating public/private rsa key pair. 
¬  601.078101| cloud-init¬1288|: Your identification has been saved in /etc/ssh/
ssh_host_rsa_key 
¬  601.078136| cloud-init¬1288|: Your public key has been saved in /etc/ssh/ssh
host_rsa_key.pub 
¬  601.078170| cloud-init¬1288|: The key fingerprint is: 
¬  601.078203| cloud-init¬1288|: SHA256:kHtkABZwk8AE80fy0KPzTRcYpht4iXdZmJ37Cgi3
fJ0 root§ubuntu-server 
¬  601.078236| cloud-init¬1288|: The key's randomart image is: 
¬  601.078274| cloud-init¬1288|: +---¬RSA 3072|----+ 
¬  601.078307| cloud-init¬1288|: !o+*+B++*..       ! 
¬  601.078340| cloud-init¬1288|: ! o.X+=+=+        ! 
¬  601.078373| cloud-init¬1288|: !  +.O.= oo       ! 
¬  601.078406| cloud-init¬1288|: !  ++.+.=o        ! 
¬  601.078439| cloud-init¬1288|: !   *.=.oSo       ! 
¬  601.078471| cloud-init¬1288|: !    = +.E .      ! 
¬  601.078503| cloud-init¬1288|: !     . . .       ! 
¬  601.078537| cloud-init¬1288|: !        .        ! 
¬  601.078570| cloud-init¬1288|: !                 ! 
¬  601.078602| cloud-init¬1288|: +----¬SHA256|-----+ 
¬  601.078635| cloud-init¬1288|: Generating public/private dsa key pair. 
¬  601.078671| cloud-init¬1288|: Your identification has been saved in /etc/ssh/
ssh_host_dsa_key 
¬  601.078704| cloud-init¬1288|: Your public key has been saved in /etc/ssh/ssh_
host_dsa_key.pub 
¬  601.078736| cloud-init¬1288|: The key fingerprint is: 
¬  601.078767| cloud-init¬1288|: SHA256:ZBNyksVVYZVhKJeL+PWKpsdUcn21yiceX/DboXQd
Pq0 root§ubuntu-server 
¬  601.078800| cloud-init¬1288|: The key's randomart image is: 
¬  601.078835| cloud-init¬1288|: +---¬DSA 1024|----+ 
¬  601.078867| cloud-init¬1288|: !      o++...+=+o ! 
¬  601.078899| cloud-init¬1288|: !      .+....+.. .! 
¬  601.078932| cloud-init¬1288|: !        +. + o  o! 
¬  601.078964| cloud-init¬1288|: !       o..o = oo.! 
¬  601.078996| cloud-init¬1288|: !        S. =..o++! 
¬  601.079029| cloud-init¬1288|: !          o  *.*=! 
¬  601.079061| cloud-init¬1288|: !         o .o.B.*! 
¬  601.079094| cloud-init¬1288|: !          = .oEo.! 
¬  601.079135| cloud-init¬1288|: !        .+       ! 
¬  601.079167| cloud-init¬1288|: +----¬SHA256|-----+ 
¬  601.079199| cloud-init¬1288|: Generating public/private ecdsa key pair. 
¬  601.079231| cloud-init¬1288|: Your identification has been saved in /etc/ssh/
ssh_host_ecdsa_key 
¬  601.079263| cloud-init¬1288|: Your public key has been saved in /etc/ssh/ssh_
host_ecdsa_key.pub 
¬  601.079295| cloud-init¬1288|: The key fingerprint is: 
¬  601.079327| cloud-init¬1288|: SHA256:Bitar9fVHUH2FnYVSJJnldprdAcM5Est0dmRWFTU
i8k root§ubuntu-server 
¬  601.079362| cloud-init¬1288|: The key's randomart image is: 
¬  601.079394| cloud-init¬1288|: +---¬ECDSA 256|---+ 
¬  601.079426| cloud-init¬1288|: !           o**O%&! 
¬  601.079458| cloud-init¬1288|: !           o.OB+=! 
¬  601.079491| cloud-init¬1288|: !      .     B *o+! 
¬  601.079525| cloud-init¬1288|: !       o   . E.=o! 
¬  601.079557| cloud-init¬1288|: !    o . S  .....+! 
¬  601.079589| cloud-init¬1288|: !   o o .  . . .o ! 
¬  601.079621| cloud-init¬1288|: !  .   .. .    .  ! 
¬  601.079653| cloud-init¬1288|: !     .. .        ! 
¬  601.079685| cloud-init¬1288|: !    ..           ! 
¬  601.079717| cloud-init¬1288|: +----¬SHA256|-----+ 
¬  601.079748| cloud-init¬1288|: Generating public/private ed25519 key pair. 
¬  601.079782| cloud-init¬1288|: Your identification has been saved in /etc/ssh/
ssh_host_ed25519_key 
¬  601.079814| cloud-init¬1288|: Your public key has been saved in /etc/ssh/ssh_
host_ed25519_key.pub 
¬  601.079847| cloud-init¬1288|: The key fingerprint is: 
¬  601.079879| cloud-init¬1288|: SHA256:yWsZ/5+7u7D3SIcd7HYnyajXyeWnt5nQ+ZI3So3b
eN8 root§ubuntu-server 
¬  601.079911| cloud-init¬1288|: The key's randomart image is: 
¬  601.079942| cloud-init¬1288|: +--¬ED25519 256|--+ 
¬  601.079974| cloud-init¬1288|: !                 ! 
¬  601.080010| cloud-init¬1288|: !                 ! 
¬  601.080042| cloud-init¬1288|: !                 ! 
¬  601.080076| cloud-init¬1288|: !       . .    .  ! 
¬  601.080107| cloud-init¬1288|: !        S      o ! 
¬  601.080139| cloud-init¬1288|: !         =   o=++! 
¬  601.080179| cloud-init¬1288|: !        + . o**§=! 
¬  601.080210| cloud-init¬1288|: !       .   oo+&B%! 
¬  601.080244| cloud-init¬1288|: !          ..o*%/E! 
¬  601.080289| cloud-init¬1288|: +----¬SHA256|-----+ 
¬  612.293731| cloud-init¬2027|: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 runnin
g 'modules:config' at Thu, 04 Jun 2020 12:06:59 +0000. Up 612.11 seconds. 
¬  612.293866| cloud-init¬2027|: Set the following 'random' passwords 
¬  612.293940| cloud-init¬2027|: installer:wgYsAPzYQbFYqU2X2hYm 
ci-info: no authorized SSH keys fingerprints found for user installer. 
<14>Jun  4 12:07:00 ec2:  
<14>Jun  4 12:07:00 ec2: #######################################################
###### 
<14>Jun  4 12:07:00 ec2: -----BEGIN SSH HOST KEY FINGERPRINTS----- 
<14>Jun  4 12:07:00 ec2: 1024 SHA256:ZBNyksVVYZVhKJeL+PWKpsdUcn21yiceX/DboXQdPq0
 root§ubuntu-server (DSA) 
<14>Jun  4 12:07:00 ec2: 256 SHA256:Bitar9fVHUH2FnYVSJJnldprdAcM5Est0dmRWFTUi8k 
root§ubuntu-server (ECDSA) 
<14>Jun  4 12:07:00 ec2: 256 SHA256:yWsZ/5+7u7D3SIcd7HYnyajXyeWnt5nQ+ZI3So3beN8 
root§ubuntu-server (ED25519) 
<14>Jun  4 12:07:00 ec2: 3072 SHA256:kHtkABZwk8AE80fy0KPzTRcYpht4iXdZmJ37Cgi3fJ0
 root§ubuntu-server (RSA) 
<14>Jun  4 12:07:00 ec2: -----END SSH HOST KEY FINGERPRINTS----- 
<14>Jun  4 12:07:00 ec2: #######################################################
###### 
-----BEGIN SSH HOST KEY KEYS----- 
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBIXM6t1/
35ot/aPI59ThIJBzg+qGJJ17+1ZVHfzMEDbsTwpM7e9pstPZUM7W1IHWqDvLQDBm/hGg4u8ZGEqmIMI=
 root§ubuntu-server 
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN7QtU+en+RGruj2zuxWgkMqLmh+35/GR/OEOD16k4nA
 root§ubuntu-server 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDJdKT7iUAvSjkUqI1l3fHysE+Gj7ulwGgGjYh639px
kcHEbbS3V48eROY9BmDISEHfjYXGY2wEH0tGJjNRROGJhZJVNR+qAqJBioj9d/TwXEgwLP8eAy9aVtJB
K1rIylnMQltx/SIhgiymjHLCtKlVoIS4l0frT9FiF54Qi/JeJlwGJIW3W2XgcY9ODT0Q5g3PSmlZ8KTR
imTf9Fy7WJEPA08b3fimYWsz9enuS/gECEUGV3M1MvrzpAQju27NUEOpSMZHR62IMxGvIjYIu3dUkAzm
MBdwxHdLMQ8rI8PehyHDiFr6g2Ifxoy5QLmb3hISKlq/R6pLLeXbb748gN2i8WCvK0AEGfa/kJDW3RNU
VYd+ACBBzyhVbiw7W1CQW/ohik3wyosUyi9nJq2IqOA7kkGH+1XoYq/e4/MoqxhIK/oaiudYAkaCWmP1
r/fBa3hlf0f7mVHvxA3tWZc2wYUxFPTmePvpydP2PSctHMhgboaHrGIY2CdSqg8SUdPKrOE= root§ub
untu-server 
-----END SSH HOST KEY KEYS----- 
¬  612.877357| cloud-init¬2045|: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 runnin
g 'modules:final' at Thu, 04 Jun 2020 12:07:00 +0000. Up 612.79 seconds. 
¬  612.877426| cloud-init¬2045|: ci-info: no authorized SSH keys fingerprints fo
und for user installer. 
¬  612.877468| cloud-init¬2045|: Cloud-init v. 20.2-45-g5f7825e2-0ubuntu1 finish
ed at Thu, 04 Jun 2020 12:07:00 +0000. Datasource DataSourceNoCloud ¬seed=/var/l
ib/cloud/seed/nocloud|¬dsmode=net|.  Up 612.87 seconds 
¬  612.877509| cloud-init¬2045|: Welcome to Ubuntu Server InstallerÜ 
¬  612.877551| cloud-init¬2045|: Above you will find SSH host keys and a random 
password set for the `installer` user. You can use these credentials to ssh-in a
nd complete the installation. If you provided SSH keys in the cloud-init datasou
rce, they were also provisioned to the installer user. 
¬  612.877634| cloud-init¬2045|: If you have access to the graphical console, li
ke TTY1 or HMC ASCII terminal you can complete the installation there too. 
 
It is possible to connect to the installer over the network, which 
might allow the use of a more capable terminal.  
 
To connect, SSH to installer§10.222.111.24. 
 
The password you should use is "KRuXtz5dURAyPkcjcUvA". 
 
The host key fingerprints are: 
 
    RSA     SHA256:3IvYMkU05lQSKBxOVZUJMzdtXpz3RJl3dEQsg3UWc54 
    ECDSA   SHA256:xd1xnkBpn49DUbuP8uWro2mu1GM4MtnqR2WEWg1fS3o 
    ED25519 SHA256:Hk3+/4+X7NJBHl6/e/6xFhNXsbHBsOvt6i8YEFUepko 
  
Ubuntu Focal Fossa (development branch) ubuntu-server ttyS0
```  
  
The next step is to remotely connect to the install system and to proceed with the Subiquity installer.

Notice that at the end of the installer boot-up process, all necessary data is provided to proceed with running the installer in a remote SSH shell. The command to execute locally is:

``` bash
user@workstation:~$ ssh installer@10.222.111.24
```

A temporary random password for the installation was created and shared as well, which should be used without the leading and trailing double quotes:

```text
  "KRuXtz5dURAyPkcjcUvA"
```
  
```text
user@workstation:~$ ssh installer@10.222.111.24
The authenticity of host '10.222.111.24 (10.222.111.24)' can't be established.
ECDSA key fingerprint is 
SHA256:xd1xnkBpn49DUbuP8uWro2mu1GM4MtnqR2WEWg1fS3o.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.222.111.24' (ECDSA) to the list of known hosts.
installer@10.222.111.24's password: KRuXtz5dURAyPkcjcUvA
```

You may now temporarily see some login messages like these:

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
  
Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.
```

Eventually, the initial Subiquity installer screen appears:

```text
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

From this point, you can follow the normal Subiquity installation. For more details, refer to the [Subquity installer documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/index.html).

```text
 ====================================================================
  Keyboard configuration                                           ====================================================================
  Please select your keyboard layout below, or select "Identify keyboard" to  
  detect your layout automatically.                                           
                                                                              
                 Layout:  [ English (US)                     v ]              
                                                                              
                                                                              
                Variant:  [ English (US)                     v ]              
                                                                              
                                                                              
                             [ Identify keyboard ]                            
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```text
 ====================================================================
  Zdev setup                                                      
====================================================================
  ID                          ONLINE  NAMES                                  ^
                                                                             │
  generic-ccw                                                                │
  0.0.0009                                    >                              │
  0.0.000c                                    >                              │
  0.0.000d                                    >                              │
  0.0.000e                                    >                              │
                                                                             │
  dasd-eckd                                                                  │
  0.0.0190                                    >                              │
  0.0.0191                                    >                              │
  0.0.019d                                    >                              │
  0.0.019e                                    >                               
  0.0.0200                                    >                               
  0.0.0300                                    >                               
  0.0.0400                                    >                               
  0.0.0592                                    >                              v
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```

* If the list is long, hit the <kbd>End</kbd> key that will automatically scroll you down to the bottom of the Z devices list and screen.
```text
====================================================================
  Zdev setup                                                      
====================================================================
  ID                          ONLINE  NAMES                                  ^
                                                                             │
  generic-ccw                                                                │
  0.0.0009                                    >                              │
  0.0.000c                                    >                              │
  0.0.000d                                    >                              │
  0.0.000e                                    >                              │
                                                                             │
  dasd-eckd                                                                  │
  0.0.0190                                    >                              │
  0.0.0191                                    >                              │
  0.0.019d                                    >                              │
  0.0.019e                                    >┌────────────┐                 
  0.0.0200                                    >│< (close)   │                 
  0.0.0300                                    >│  Enable    │                 
  0.0.0400                                    >│  Disable   │                 
  0.0.0592                                    >└────────────┘                v
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```                                                                         

```text
====================================================================
  Zdev setup                                                      
====================================================================
  ID                          ONLINE  NAMES                                  ^
                                                                             │
  generic-ccw                                                                │
  0.0.0009                                    >                              │
  0.0.000c                                    >                              │
  0.0.000d                                    >                              │
  0.0.000e                                    >                              │
                                                                             │
  dasd-eckd                                                                  │
  0.0.0190                                    >                              │
  0.0.0191                                    >                              │
  0.0.019d                                    >                              │
  0.0.019e                                    >                               
  0.0.0200                    online  dasda   >                               
  0.0.0300                                    >                               
  0.0.0400                                    >                               
  0.0.0592                                    >                              v
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```

```text
====================================================================
  Zdev setup                                                      
====================================================================
                                                                             ^
  dasd-eckd                                                                   
  0.0.0190                                    >                               
  0.0.0191                                    >                               
  0.0.019d                                    >                               
  0.0.019e                                    >                              │
  0.0.0200                    online  dasda   >                              │
  0.0.0300                                    >                              │
  0.0.0400                                    >                              │
  0.0.0592                                    >                              │
                                                                             │
  qeth                                                                       │
  0.0.0600:0.0.0601:0.0.0602          enc600  >                              │
  0.0.0603:0.0.0604:0.0.0605                  >                              │
                                                                             │
  dasd-eckd                                                                  │
  0.0.1607                                    >                              v
                                                                              
                                 [ Continue   ]                               
                                 [ Back       ]                               
```

```text
====================================================================
  Network connections                                             
====================================================================
  Configure at least one interface this server can use to talk to other       
  machines, and which preferably provides sufficient access for updates.      
                                                                              
    NAME    TYPE  NOTES                                                       
  [ enc600  eth   -                > ]                                        
    static  10.222.111.24/24                                                  
    02:28:0a:00:00:39 / Unknown Vendor / Unknown Model                        
                                                                              
  [ Create bond > ]                                                           
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```text
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

```text
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

```text
====================================================================
  Guided storage configuration                                    
====================================================================
  Configure a guided storage layout, or create a custom one:                  
                                                                              
  (X)  Use an entire disk                                                     
                                                                              
       [ 0X0200       local disk 6.876G                                    v ]
                                                                              
       [ ]  Set up this disk as an LVM group                                  
                                                                              
            [ ]  Encrypt the LVM group with LUKS                              
                                                                              
                         Passphrase:                                          
                                                                              
                                                                              
                 Confirm passphrase:                                          
                                                                              
                                                                              
  ( )  Custom storage layout                                                  
                                                                              
                                 [ Done       ]                               
                                 [ Back       ]                               
```

```text
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

```text
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

```text
====================================================================
  Profile setup                                                   
====================================================================
  Enter the username and password you will use to log in to the system. You   
  can configure SSH access on the next screen but a password is still needed  
  for sudo.                                                                   
                                                                              
              Your name:  Ed Example                                          
                                                                              
                                                                              
     Your server's name:  10.222.111.24                                             
                          The name it uses when it talks to other computers.  
                                                                              
        Pick a username:  ubuntu                                              
                                                                              
                                                                              
      Choose a password:  ********                                            
                                                                              
                                                                              
  Confirm your password:  ********                                            
                                                                              
                                                                              
                                 [ Done       ]                               
```

```text
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

* It’s a nice and convenient new feature to add the user's SSH keys during the installation to the system, since that makes the system login password-less on the initial login!

```text
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

```text
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
   │  2048 SHA256:joGsdfW7NbJRkg17sRyXaegoR0iZEdDWdR9Hpbc2KIw user@W520  │
   │   (RSA)                                                                │
   │  521 SHA256:T3JzxvB6K1GzXJpP5NFgX4yXvk0jhhgvbw01F7/fZ2c                │
   │  frank.heimes@canonical.com  (ECDSA)                                   │
   │                                                                        │
   │                             [ Yes        ]                             │
   │                             [ No         ]                             │
   │                                                                        │
   └────────────────────────────────────────────────────────────────────────┘

                                 [ Done       ]                               
                                 [ Back       ]                               
```

```text
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

```text
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
  │  installing openssh-server |                                            v│
  └──────────────────────────────────────────────────────────────────────────┘

                               [ View full log ]
```

```text
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

```text
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

                               [ Connection to 10.222.111.24 closed by remote host.                            [ Rebooting...  ]
Connection to 10.222.111.24 closed.
user@workstation:~$ 
```

Type `reset` to clear the screen and to revert it back to the defaults.

Now remove the old host key, since the system got a new one during the installation:

```bash
user@workstation:~$ ssh-keygen -f "/home/user/.ssh/known_hosts" -R "10.222.111.24"
# Host 10.222.111.24 found: line 159
/home/user/.ssh/known_hosts updated.
Original contents retained as /home/user/.ssh/known_hosts.old
user@workstation:~$
```

And finally login to the newly installed z/VM guest:
```bash
user@workstation:~$ ssh ubuntu@10.222.111.24
Warning: Permanently added the ECDSA host key for IP address
'10.222.111.24' to the list of known hosts.
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
the exact distribution terms for each program are described in the individual files in /usr/share/doc/*/copyright.
  
Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.
  
To run a command as administrator (user "root"), use `sudo <command>`.
See `man sudo_root` for details.
  
ubuntu@10.222.111.24:~$ uptime
 17:50:09 up 1 min,  1 user,  load average: 0.08, 0.11, 0.05
ubuntu@10.222.111.24:~$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description: Ubuntu 20.04.5 LTS
Release:	20.04
Codename:	focal
ubuntu@10.222.111.24:~$ uname -a
Linux 10.222.111.24 5.4.0-42-generic #30-Ubuntu SMP Wed Aug 05 16:57:22 UTC 2020 s390x s390x s390x GNU/Linux
ubuntu@10.222.111.24:~$ exit
logout
Connection to 10.222.111.24 closed.
user@workstation:~$
```

Done!
