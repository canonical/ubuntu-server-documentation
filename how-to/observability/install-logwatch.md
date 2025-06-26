(install-logwatch)=
# How to install and configure Logwatch


Logs are an invaluable source of information about problems that may arise in your server.  [Logwatch](https://sourceforge.net/projects/logwatch/) keeps an eye on your logs for you, flags items that may be of interest, and reports them via email.

## Install Logwatch

Install `logwatch` using the following command:

```bash
sudo apt install logwatch
```

You will also need to manually create a temporary directory in order for it to work:

```bash
sudo mkdir /var/cache/logwatch
```

## Configure `logwatch`

Logwatch's default configuration is kept in` /usr/share/logwatch/default.conf/logwatch.conf`. However, configuration changes made directly to that file can be overwritten during updates, so instead the file should be copied into `/etc` and modified there:

```
sudo cp /usr/share/logwatch/default.conf/logwatch.conf /etc/logwatch/conf/
```

With your favorite editor, open `/etc/logwatch/conf/logwatch.conf`.  The uncommented lines indicate the default configuration values.  First, lets customise some of the basics:

```text
Output = mail
MailTo = me@mydomain.org
MailFrom = logwatch@host1.mydomain.org
Detail = Low
Service = All
```

This assumes you've already set up mail services on `host1` that will allow mail to be delivered to your `me@mydomain.org` address. These emails will be addressed from `logwatch@host1.mydomain.org`.

The **Detail** level defines how much information is included in the reports. Possible values are: `Low`, `Medium`, and `High`.

Logwatch will then monitor logs for all services on the system, unless specified otherwise with the **Service** parameter.  If there are undesired services included in the reports, they can be disabled by removing them with additional **Service** fields. E.g.:

```text
Service = "-http"
Service = "-eximstats"
```

Next, run `logwatch` manually to verify your configuration changes are valid:

```bash
sudo logwatch --detail Low --range today
```

The report produced should look something like this:

```text
################### Logwatch 7.4.3 (12/07/16) ####################
       Processing Initiated: Fri Apr 24 16:58:14 2020
       Date Range Processed: today
                             ( 2020-Apr-24 )
                             Period is day.
       Detail Level of Output: 0
       Type of Output/Format: stdout / text
       Logfiles for Host: `host1.mydomain.org`
##################################################################
 
--------------------- pam_unix Begin ------------------------
 
sudo:
   Sessions Opened:
      bryce -> root: 1 Time(s)
 
 
---------------------- pam_unix End -------------------------
 
 
--------------------- rsnapshot Begin ------------------------
 
ERRORS:
    /usr/bin/rsnapshot hourly: completed, but with some errors: 5 Time(s)
    /usr/bin/rsync returned 127 while processing root@host2:/etc/: 5 Time(s)
    /usr/bin/rsync returned 127 while processing root@host2:/home/: 5 Time(s)
    /usr/bin/rsync returned 127 while processing root@host2:/proc/uptime: 5 Time(s)
    /usr/bin/rsync returned 127 while processing root@host3:/etc/: 5 Time(s)
    /usr/bin/rsync returned 127 while processing root@host3:/home/: 5 Time(s)
    /usr/bin/rsync returned 127 while processing root@host3:/proc/uptime: 5 Time(s)
 
 
---------------------- rsnapshot End -------------------------
 
 
--------------------- SSHD Begin ------------------------
 
 
Users logging in through sshd:
   bryce:
      192.168.1.123 (`host4.mydomain.org`): 1 time
 
---------------------- SSHD End -------------------------
 
 
--------------------- Sudo (secure-log) Begin ------------------------
 
 
bryce => root
\-------------
/bin/bash                      -   1 Time(s).
 
---------------------- Sudo (secure-log) End -------------------------
 
 
--------------------- Disk Space Begin ------------------------
 
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdc1       220G   19G  190G   9% /
/dev/loop1      157M  157M     0 100% /snap/gnome-3-28-1804/110
/dev/loop11     1.0M  1.0M     0 100% /snap/gnome-logs/81
/dev/md5        9.1T  7.3T  1.8T  81% /srv/Products
/dev/md6        9.1T  5.6T  3.5T  62% /srv/Archives
/dev/loop14     3.8M  3.8M     0 100% /snap/gnome-system-monitor/127
/dev/loop17      15M   15M     0 100% /snap/gnome-characters/399
/dev/loop18     161M  161M     0 100% /snap/gnome-3-28-1804/116
/dev/loop6       55M   55M     0 100% /snap/core18/1668
/dev/md1        1.8T  1.3T  548G  71% /srv/Staff
/dev/md0        3.6T  3.5T   84G  98% /srv/Backup
/dev/loop2      1.0M  1.0M     0 100% /snap/gnome-logs/93
/dev/loop5       15M   15M     0 100% /snap/gnome-characters/495
/dev/loop8      3.8M  3.8M     0 100% /snap/gnome-system-monitor/135
/dev/md7        3.6T  495G  3.0T  15% /srv/Customers
/dev/loop9       55M   55M     0 100% /snap/core18/1705
/dev/loop10      94M   94M     0 100% /snap/core/8935
/dev/loop0       55M   55M     0 100% /snap/gtk-common-themes/1502
/dev/loop4       63M   63M     0 100% /snap/gtk-common-themes/1506
/dev/loop3       94M   94M     0 100% /snap/core/9066

/srv/Backup (/dev/md0) => 98% Used. Warning. Disk Filling up.
 
---------------------- Disk Space End -------------------------
 
 
###################### Logwatch End #########################
```

## Further reading
- The Ubuntu {manpage}`logwatch(8)` manpage contains many more detailed options.
