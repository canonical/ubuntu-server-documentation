(automatic-updates)=
# Automatic updates

Ubuntu Server will apply security updates automatically, without user interaction. This is done via the `unattended-upgrades` package, which is installed by default.

But as the name suggests, it can apply other types of updates, and with interesting options alongside. For example:

 - It can reboot the system, if an update warrants it.
 - It can apply other types of updates, not just security.
 - It can block certain updates from ever being applied automatically.

And more. Let's explore some of these options.

## Overview
If for some reason the package is not present, it can be installed with the following command:

```bash
sudo apt install unattended-upgrades
```

Important files and directories:

 - `/etc/apt/apt.conf.d/50unattended-upgrades`: This file contains the options that control the behavior of the tool, such as if a reboot should be scheduled or not, or which packages are blocked from being upgraded.
 - `/etc/apt/apt.conf.d/20auto-upgrades`: This file is used to control whether the unattended upgrade should be enabled or not, and how often it should run.
 - `/var/log/unattended-upgrades`: This directory contains detailed logs of each unattended upgrade run.

Right after installation, automatic installation of security updates will be enabled, including [Expanded Security Maintenance (ESM)](https://ubuntu.com/security/esm) if that is available on the system. By default, `unattended-upgrades` runs once per day.

## Enabling and disabling unattended upgrades
Unattended upgrades performs the equivalent of `apt-get update` and `apt-get upgrade` (see {ref}`Package management <package-management>` for details on these commands XXX HELP WITH LINKING XXX). First, it refreshes the package lists, to become aware of the new state of the package repositories. Then it checks which upgrades are available and applies them.

These two steps are controlled via the `Update-Package-Lists` and `Unattended-Upgrade` options in `/etc/apt/apt.conf.d/20auto-upgrades`:
```text
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```
The value for each option is a time-based value. When used just as a number, it means number of days. If set to zero, that action is disabled. If set to `1` (the default), then it means every day. A value of `2` means every two days, and so on.

Therefore, to disable unattended upgrades, set these options to zero:
```text
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Unattended-Upgrade "0";
```

These actions are triggered by systemd timer units at a set time but with a random delay: `apt-daily.timer` and `apt-daily-upgrade.timer`. These timers activate the corresponding services that run the `/usr/lib/apt/apt.systemd.daily` script.

However, it may happen that if the server is off at the time the timer unit elapses, the timer may be triggered immediately at the next startup (still subject to the *RandomizedDelaySec* value). As a result, they may often run on system startup and thereby cause immediate activity and hold the apt-lock.

In many cases this is beneficial, but in some cases it might be counter-productive; examples are administrators with many shut-down machines or VM images that are only started for some quick action, which is delayed or even blocked by the unattended upgrades. To adapt this behaviour, we can change/override the configuration of both APT's timer units `apt-daily-upgrade.timer` and `apt-daily.timer`. To do so, use `systemctl edit <timer_unit>` and override the *Persistent* attribute setting it to *false*:

```ini
[Timer]
Persistent=false
```

See the explanation for the *Persistent* option in [systemd.timer manpage](https://manpages.ubuntu.com/manpages/noble/en/man5/systemd.timer.5.html) for more details.

## Where to pick updates from

In `/etc/apt/apt.conf.d/50unattended-upgrades`, the `Allowed-Origins` section specifies which release pockets will be used to gather updates from. See the [Ubuntu Packaging Guide](https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/#pockets) for additional information about each pocket.

This is the default:
```text
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    // Extended Security Maintenance; doesn't necessarily exist for
    // every release and this system may not have it installed, but if
    // available, the policy for updates is such that unattended-upgrades
    // should also install from here by default.
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
//  "${distro_id}:${distro_codename}-updates";
//  "${distro_id}:${distro_codename}-proposed";
//  "${distro_id}:${distro_codename}-backports";
};
```

> **Note**:
> The double “//” indicates a comment, so whatever follows "//" will not be evaluated.

If you want to also allow non-security updates to be applied automatically, then uncomment the line about `-updates`, like so:
```text
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    // Extended Security Maintenance; doesn't necessarily exist for
    // every release and this system may not have it installed, but if
    // available, the policy for updates is such that unattended-upgrades
    // should also install from here by default.
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
    "${distro_id}:${distro_codename}-updates";
//  "${distro_id}:${distro_codename}-proposed";
//  "${distro_id}:${distro_codename}-backports";
};
```

## How to block certain packages
Specific packages can also be excluded from an update. This is controlled via the `Unattended-Upgrade::Package-Blacklist` configuration option in `/etc/apt/apt.conf.d/50unattended-upgrades`, which contains a list of [Python Regular Expressions](https://docs.python.org/3/howto/regex.html). Each line of this list is checked against the available package updates, and if there is a match, that package is not upgraded.

> **Note**:
> Keep in mind that blocking a package might prevent other updates from being installed if they depend on the blocked package!

For example, this will block all packages that start with `linux-` from being automatically upgraded:
```text
Unattended-Upgrade::Package-Blacklist {
    "linux-";
}
```

A more specific configuration like the one below will block only the `libc6` and `libc-bin` packages from being automatically upgraded:
```text
Unattended-Upgrade::Package-Blacklist {
    "libc6$";
    "libc-bin$";
}
```
Here, the use of the `$` character marks the end of the package name (in regular expression terms, it's the end of the line, i.e., the end of the match).
> **Note**:
> The regular expressions used here behave as if the "`^`" character is present at the start, i.e., the `libc6$` expression will match `libc6`, but will NOT match `glibc6` for example.

Of course, this being a regular expression means we could also write the above like this:
```text
Unattended-Upgrade::Package-Blacklist {
    "libc(6|-bin)$";
}
```
Just be careful to not overuse the power of regular expressions: readability is key.

## Notifications

Configuring `Unattended-Upgrade::Mail` in `/etc/apt/apt.conf.d/50unattended-upgrades` will enable `unattended-upgrades` to email an administrator detailing any packages that need upgrading or have problems.

> **Note**:
> Sending out emails from unattended services and jobs like these requires separate configuration of a package like `ssmtp` or another minimalistic mail client that is capable to send messages to a mail server.

## Reboots
TBD

## Including other origins
TBD

## Fleet considerations
TBD

## Integration with Pro
TBD

## When should it be disabled
TBD

## Testing/troubleshooting
TBD
