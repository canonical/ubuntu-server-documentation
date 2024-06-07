(about-time-synchronisation)=
# Time synchronisation

Network Time Protocol (NTP) is a networking protocol for synchronising time over a network. Basically, a client requests the current time from a server, and uses it to set its own clock.

Behind this simple description, there is a lot of complexity. There are three tiers of NTP servers; tier one NTP servers are connected to atomic clocks, while tier two and tier three three servers spread the load of actually handling requests across the Internet.

The client software is also a lot more complex than you might expect. It must factor in communication delays and adjust the time in a way that does not upset all the other processes that run on the server. Luckily, all that complexity is hidden from you\!

By default, Ubuntu uses `timedatectl`/`timesyncd` to synchronise time, and they are available by default. See our guide If you would like to know [how to configure `timedatectl` and `timesyncd`](../how-to/use-timedatectl-and-timesyncd.md).

Users can also optionally [use `chrony` to serve NTP](../how-to/how-to-serve-the-network-time-protocol-with-chrony.md).

## How time synchronisation works

Since Ubuntu 16.04, `timedatectl`/`timesyncd` (which are part of `systemd`) replace most of `ntpdate`/`ntp`.

### About `timesyncd`

`timesyncd` replaces not only `ntpdate`, but also the client portion of `chrony` (formerly `ntpd`). So, on top of the one-shot action that `ntpdate` provided on boot and network activation, `timesyncd` now regularly checks and keeps your local time in sync. It also stores time updates locally, so that after reboots the time monotonically advances (if applicable).

### About `timedatectl`

If `chrony` is installed, `timedatectl` steps back to let `chrony` handle timekeeping. This ensures that no two time-syncing services can conflict with each other. 

`ntpdate` is now considered deprecated in favor of `timedatectl` (or `chrony`) and is no longer installed by default. `timesyncd` will generally keep your time in sync, and `chrony` will help with more complex cases. But if you had one of a few known special `ntpdate` use cases, consider the following:

  - If you require a one-shot sync, use: `chronyd -q`
  - If you require a one-shot time check (without setting the time), use: `chronyd -Q`

While use of `ntpd` is no longer recommended, this also still applies to `ntpd` being installed to retain any previous behaviour/config that you had through an upgrade. However, it also implies that on an upgrade from a former release, `ntp`/`ntpdate` might still be installed and therefore renders the new `systemd`-based services disabled.

## Further reading

- [ntp.org: home of the Network Time Protocol project](http://www.ntp.org/)
- [pool.ntp.org: project of virtual cluster of timeservers](http://www.pool.ntp.org/)

- [Freedesktop.org info on timedatectl](https://www.freedesktop.org/software/systemd/man/timedatectl.html)
- [Freedesktop.org info on systemd-timesyncd service](https://www.freedesktop.org/software/systemd/man/systemd-timesyncd.service.html#)

- [Chrony FAQ](https://chrony-project.org/faq.html)
- [Feeding chrony from GPSD](https://gpsd.gitlab.io/gpsd/gpsd-time-service-howto.html#_feeding_chrony_from_gpsd) 

- Also see the [Ubuntu Time wiki page](https://help.ubuntu.com/community/UbuntuTime) for more information.
