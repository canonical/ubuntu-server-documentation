(chrony-client)=
# Synchronize time using chrony

Ubuntu uses `chrony` for synchronizing time, which is installed by default as of Ubuntu 25.10. You can optionally use `timedatectl`/`timesyncd` to {ref}`synchronize time using systemd <timedatectl-and-timesyncd>`.

## Check status of `chrony` client

The current status of time synchronization can be checked with the `timedatectl status` command, which is available via `systemd` and will produce output like this:

```text
               Local time: Mo 2025-06-16 15:21:46 CEST
           Universal time: Mo 2025-06-16 13:21:46 UTC
                 RTC time: Mo 2025-06-16 13:21:46
                Time zone: Europe/Berlin (CEST, +0200)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

For more details on time accuracy, `chrony` can be queried directly, using the `chronyc -N tracking` command, producing output like this:
```text
Reference ID    : B97DBE7B (2.ntp.ubuntu.com)
Stratum         : 3
Ref time (UTC)  : Mon Jun 16 13:06:04 2025
System time     : 0.000000004 seconds slow of NTP time
Last offset     : +0.001758954 seconds
RMS offset      : 0.017604901 seconds
Frequency       : 3.889 ppm slow
Residual freq   : +0.202 ppm
Skew            : 1.458 ppm
Root delay      : 0.022837413 seconds
Root dispersion : 0.003050051 seconds
Update interval : 1032.5 seconds
Leap status     : Normal
```

### Network Time Security (NTS)

`chrony` supports "Network Time Security" (NTS) and enables it by default, using the Ubuntu NTS pools. This is done by specifying a `server` or `pool` as usual. Afterwards, options can be listed and it is there that `nts` can be added. For example:

```text
server <server-fqdn-or-IP> iburst nts
# or as concrete example
pool 1.ntp.ubuntu.com iburst maxsources 1 nts prefer
```

For **validation of NTS enablement**, one can list the time sources in use by executing the `chronyc -N sources` command, to find the timeserver in use, as indicated by the `^*` symbol in the first column. Then check the `authdata` of that connection using `sudo chronyc -N authdata`. If the client was able to successfully establish a NTS connection, it will show the `Mode: NTS` field and non-zero values for `KeyID`, `Type` and `KLen`:

```text
$ sudo chronyc -N authdata
Name/IP address             Mode KeyID Type KLen Last Atmp  NAK Cook CLen
=========================================================================
1.ntp.ubuntu.com             NTS     6   30  128  14d    0    0    8   64
2.ntp.ubuntu.com             NTS     6   30  128  14d    0    0    8   64
3.ntp.ubuntu.com             NTS     1   30  128  27d    0    0    8   64
4.ntp.ubuntu.com             NTS     2   30  128  20d    0    0    5   64
ntp-bootstrap.ubuntu.com     NTS     3   30  128   7d    0    0    8   64
```

### NTS related constraints

**Key Exchange port:** NTS/KE uses a separate port (4460/tcp)** to negotiate
security parameters, which are then used via the normal NTP port (123/udp).
This is a new deployment, running on different IP addresses than the
traditional Ubuntu NTP pool.

:::{warning}
  If the network does not allow access to the Ubuntu NTS servers and required
  ports, with the default configuration is in place, `chrony` will not be able
  to adjust the system's clock. To revert to NTP, edit the configuration file
  in `/etc/chrony/sources.d/ubuntu-ntp-pools.sources` and revert to using
  the listed NTP servers in favor of the NTS ones.
:::

**Bad Clocks and secure time syncing:** NTS is based on TLS, and TLS needs a
  reasonably correct clock. Due to that, an NTS-based sync might fail if the
  clock is too far off. On hardware affected by this problem, one can consider
  using the `nocerttimecheck` option, which allows to set the number of times
  that the time can be synced without checking validation and expiration.

:::{note}
  A new CA is installed in `/etc/chrony/nts-bootstrap-ubuntu.crt` that is
  used specifically for the Ubuntu NTS bootstrap server, needed for when the
  clock is too far off. This is added to certificate set ID "1", and defined
  via `/etc/chrony/conf.d/ubuntu-nts.conf`.
:::

## Configure chrony

An admin can control the timezone and how the system clock should relate to the `hwclock` using the common `timedatectl [set-timezone/set-local-rtc]` commands, provided by `systemd`. For more specific actions, like adding of time-sources, the `chronyc` command can be used. See `man chronyc` for more details.

One can edit configuration in `/etc/chrony/sources.d/` to add/remove server lines. By default these servers are configured:

```text
# Use NTS by default
# NTS uses an additional port to negotiate security: 4460/tcp
# The normal NTP port remains in use: 123/udp
pool 1.ntp.ubuntu.com iburst maxsources 1 nts prefer
pool 2.ntp.ubuntu.com iburst maxsources 1 nts prefer
pool 3.ntp.ubuntu.com iburst maxsources 1 nts prefer
pool 4.ntp.ubuntu.com iburst maxsources 1 nts prefer
# The bootstrap server is needed by systems without a hardware clock, or a very
# large initial clock offset. The specified certificate set is defined in
# /etc/chrony/conf.d/ubuntu-nts.conf.
pool ntp-bootstrap.ubuntu.com iburst maxsources 1 nts certset 1
```

After adding or removing sources, they can be reloaded using `sudo chrony reload sources`.

Of the pool, `2.ubuntu.pool.ntp.org` and `ntp.ubuntu.com` also support IPv6, if needed. If you need to force IPv6, there is also `ipv6.ntp.ubuntu.com` which is not configured by default.

### Time sources provided by DHCP (option 42)

`chrony` consumes time sources provided by DHCP (option 42). Those could be traditional, non-authenticated NTP sources. Should one want to avoid this behavior, overruling the choices made by a local DHCP administrator, it can be disabled in `/etc/chrony/chrony.conf`. To do that one would comment out the corresponding setting:
```
# Use time sources from DHCP.
# sourcedir /run/chrony-dhcp
```

### Chrony time-daemon

`chronyd` itself is a normal service, so you can check its status in more detail using:

```
systemctl status chrony.service
```

The output produced will look something like this:
```
● chrony.service - chrony, an NTP client/server
     Loaded: loaded (/usr/lib/systemd/system/chrony.service; enabled; preset: enabled)
     Active: active (running) since Mon 2025-06-02 11:27:09 CEST; 2 weeks 0 days ago
       Docs: man:chronyd(8)
             man:chronyc(1)
             man:chrony.conf(5)
   Main PID: 36027 (chronyd)
      Tasks: 2 (limit: 28388)
     Memory: 5.8M (peak: 6.8M swap: 604.0K swap peak: 4.5M)
        CPU: 5.038s
     CGroup: /system.slice/chrony.service
             ├─36027 /usr/sbin/chronyd -F 1
             └─36028 /usr/sbin/chronyd -F 1

    Jun 02 11:27:09 questing chronyd[36027]: Using right/UTC timezone to obtain leap second data
    Jun 02 11:27:09 questing chronyd[36027]: Loaded seccomp filter (level 1)
    Jun 02 11:27:09 questing chronyd[36027]: Added pool 1.ntp.ubuntu.com
    Jun 02 11:27:09 questing chronyd[36027]: Added pool 2.ntp.ubuntu.com
    Jun 02 11:27:09 questing chronyd[36027]: Added pool 3.ntp.ubuntu.com
    Jun 02 11:27:09 questing chronyd[36027]: Added pool 4.ntp.ubuntu.com
    Jun 02 11:27:09 questing chronyd[36027]: Added pool ntp-bootstrap.ubuntu.com
    Jun 02 11:27:09 questing systemd[1]: Started chrony.service - chrony, an NTP client/server.
```

Default configuration such as `sourcedir`, `ntsdumpdir` or `rtcsync` is provided in `/etc/chrony/chrony.conf` and additional config files can be stored in `/etc/chrony/conf.d/`. The NTS servers from which to fetch time for `chrony` are in defined in `/etc/chrony/sources.d/ubuntu-ntp-pools.sources`. There are more advanced options documented in the {manpage}`chrony.conf(5)` manual page. Common use cases are specifying an explicit trusted certificate. After changing any part of the config file you need to restart `chrony`, as follows:

```bash
sudo systemctl restart chrony.service
```

## Next steps

If you would now like to also serve the Network Time Protocol via `chrony`, this guide will walk you through {ref}`how to configure your chrony setup <serve-ntp-with-chrony>`.

## References

- {manpage}`chronyc(1)` manual page

- {manpage}`chronyd(8)` manual page

- {manpage}`chrony.conf(5)` manual page
