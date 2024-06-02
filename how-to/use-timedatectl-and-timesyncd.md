(use-timedatectl-and-timesyncd)=
# Use timedatectl and timesyncd

Ubuntu uses `timedatectl` and `timesyncd` for synchronising time, and they are installed by default as part of `systemd`. You can optionally use `chrony` to [serve the Network Time Protocol](how-to-serve-the-network-time-protocol-with-chrony.md).

In this guide, we will show you how to configure these services.

> **Note**:
> If `chrony` is installed, `timedatectl` steps back to let `chrony` handle timekeeping. This ensures that no two time-syncing services will be in conflict. 

## Check status of `timedatectl`

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

If `chrony` is running, it will automatically switch to:

```text
[...]
 systemd-timesyncd.service active: no 
```

### Configure `timedatectl`

By using `timedatectl`, an admin can control the timezone, how the system clock should relate to the `hwclock` and whether permanent synchronisation should be enabled. See `man timedatectl` for more details.

## Check status of `timesyncd`

`timesyncd` itself is a normal service, so you can check its status in more detail using:

```
systemctl status systemd-timesyncd
```

The output produced will look something like this:

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

### Configure `timesyncd`

The server from which to fetch time for `timedatectl` and `timesyncd` can be specified in `/etc/systemd/timesyncd.conf`. Additional config files can be stored in `/etc/systemd/timesyncd.conf.d/`. The entries for `NTP=` and `FallbackNTP=` are space-separated lists. See `man timesyncd.conf` for more details.

## Next steps

If you would now like to serve the Network Time Protocol via `chrony`, this guide will walk you through [how to install and configure your setup](how-to-serve-the-network-time-protocol-with-chrony.md).

## References

- [Freedesktop.org info on timedatectl](https://www.freedesktop.org/software/systemd/man/timedatectl.html)

- [Freedesktop.org info on systemd-timesyncd service](https://www.freedesktop.org/software/systemd/man/systemd-timesyncd.service.html#)

- See the [Ubuntu Time wiki page](https://help.ubuntu.com/community/UbuntuTime) for more information.
