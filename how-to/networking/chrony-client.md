(chrony-client)=
# Synchronize time using Chrony

Ubuntu uses `chrony` for synchronizing time, which is installed by default as of Ubuntu 25.10. You can optionally use `timedatectl`/`timesyncd` to {ref}`synchronize time using systemd <timedatectl-and-timesyncd>`.

In this guide, we will show you how to configure these services.

## Check status of `chrony` client

The current status of time and time configuration via `timedatectl` and `timesyncd` can be checked with the `timedatectl status` command, which will produce output like this:

```text
               Local time: Wed 2023-06-14 12:05:11 BST
           Universal time: Wed 2023-06-14 11:05:11 UTC
                 RTC time: Wed 2023-06-14 11:05:11
                Time zone: Europe/Isle_of_Man (BST, +0100)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

### Configure `chrony` client

By using `chronyc`, an admin can control the timezone, how the system clock should relate to the `hwclock` and whether permanent synchronization should be enabled. See `man chronyc` for more details.

### Network Time Security (NTS)

TODO:
chronyc -N sources
chronyc -N authdata -a
chronyc ntpdata [ip] | grep Authenticated

## Check status of `chrony` daemon

`chronyd` itself is a normal service, so you can check its status in more detail using:

```
systemctl status chrony.service
```

The output produced will look something like this:

FIXME:
```
      systemd-timesyncd.service - Network Time Synchronization
       Loaded: loaded (/lib/systemd/system/systemd-timesyncd.service; enabled; vendor preset: enabled)
       Active: active (running) since Fri 2018-02-23 08:55:46 UTC; 10s ago
         Docs: man:systemd-timesyncd.service(8)
     Main PID: 3744 (systemd-timesyn)
       Status: "Synchronized to time server 91.189.89.198:123 (ntp.ubuntu.com)."
        Tasks: 2 (limit: 4915)
       CGroup: /system.slice/systemd-timesyncd.service
               |-3744 /lib/systemd/systemd-timesyncd
    
    Feb 23 08:55:46 bionic-test systemd[1]: Starting Network Time Synchronization...
    Feb 23 08:55:46 bionic-test systemd[1]: Started Network Time Synchronization.
    Feb 23 08:55:46 bionic-test systemd-timesyncd[3744]: Synchronized to time server 91.189.89.198:123 (ntp.ubuntu.com).
```

### Configure `chrony` daemon

The server from which to fetch time for `timedatectl` and `timesyncd` can be specified in `/etc/systemd/timesyncd.conf`. Additional config files can be stored in `/etc/systemd/timesyncd.conf.d/`. The entries for `NTP=` and `FallbackNTP=` are space-separated lists. See `man timesyncd.conf` for more details.

## Next steps

If you would now like to serve the Network Time Protocol via `chrony`, this guide will walk you through {ref}`how to install and configure your setup <serve-ntp-with-chrony>`.

## References

- [Manpage about chronyc](https://manpages.ubuntu.com/manpages/man1/chronyc.1.html)

- [Manpage about chronyd](https://manpages.ubuntu.com/manpages/man8/chronyd.8.html)

- [Manpage about chrony.conf](https://manpages.ubuntu.com/manpages/man5/chrony.conf.5.html)
