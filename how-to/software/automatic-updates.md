(automatic-updates)=
# Automatic updates

Ubuntu Server will apply security updates automatically, without user interaction. This is done via the `unattended-upgrades` package, which is installed by default.

But as the name suggests, it can apply other types of updates, and with interesting options alongside. For example:

 - It can reboot the system, if an update warrants it.
 - It can apply other types of updates, not just security.
 - It can block certain updates from ever being applied automatically.

And more. Let's explore some of these options.

> **IMPORTANT**:
>
> Just adding another package repository to an Ubuntu system WILL NOT make *unattended-upgrades* consider it for updates! This is explained "Where to pick updates from " **XXX HELP WITH LINKING XXX** later in this document.

## Configuration layout
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
Unattended upgrades performs the equivalent of `apt-get update` and `apt-get upgrade` (see {ref}`Package management <package-management>` for details on these commands **XXX HELP WITH LINKING XXX**). First, it refreshes the package lists, to become aware of the new state of the package repositories. Then it checks which upgrades are available and applies them.

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

In many cases this is beneficial, but in some cases it might be counter-productive; examples are administrators with many shut-down machines or VM images that are only started for some quick action, which is delayed or even blocked by the unattended upgrades. To change this behaviour, we can change/override the configuration of both APT's timer units `apt-daily-upgrade.timer` and `apt-daily.timer`. To do so, use `systemctl edit <timer_unit>` and override the *Persistent* attribute setting it to *false*:

```ini
[Timer]
Persistent=false
```

With this change, the timer will trigger the service only on the next scheduled time. In other words, it won't catch up to the run it missed while the system was off. See the explanation for the *Persistent* option in [systemd.timer manpage](https://manpages.ubuntu.com/manpages/noble/en/man5/systemd.timer.5.html) for more details.

## Where to pick updates from

In `/etc/apt/apt.conf.d/50unattended-upgrades`, the `Allowed-Origins` section specifies which repositories will be used to gather updates from. See the [Ubuntu Packaging Guide](https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/#pockets) for additional information about each official repository that Ubuntu uses.

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
>
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
The `Origin` field is a standard field used in package repositories. By default, *unattended-upgrades* will ship with only official Ubuntu repositories configured, which is the configuration shown above. To have the system apply upgrades automatically from other repositories, its *Origin* needs to be added to this configuration option.

A very popular package repository type is a [Launchpad PPA](https://help.launchpad.net/Packaging/PPA). PPAs are normally referred to using the format *ppa:\<user\>/\<name\>*. For example, the PPA at https://launchpad.net/~canonical-server/+archive/ubuntu/server-backports is also referred to as `ppa:canonical-server/server-backports`.

To use a PPA in the *Allowed-Origins* configuration, we need its *Origin* field. For PPAs, it is in the format *LP-PPA-\<user\>-\<name\>*. Adding it to the `Allowed-Origins` configuration would result in the following (continuing from the example above):
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
    "LP-PPA-canonical-server-server-backports:${distro_codename}";
};
```

Note that due to the hyphens that are both a separator, and also part of the name in this case, once everything is written out like above, it becomes difficult to see at a glance which part is the username, and which part is the PPA name. But that's ok, because it's the whole text that matters.

Now when the tool runs, that PPA will be considered for upgrades and is listed in *Allowed origins*:
```text
2025-03-13 22:44:29,802 INFO Starting unattended upgrades script
2025-03-13 22:44:29,803 INFO Allowed origins are: o=Ubuntu,a=noble, o=Ubuntu,a=noble-security, o=UbuntuESMApps,a=noble-apps-security, o=UbuntuESM,a=noble-infra-security, o=LP-PPA-canonical-server-server-backports,a=noble
2025-03-13 22:44:29,803 INFO Initial blacklist:
2025-03-13 22:44:29,803 INFO Initial whitelist (not strict):
2025-03-13 22:44:33,029 INFO Option --dry-run given, *not* performing real actions
2025-03-13 22:44:33,029 INFO Packages that will be upgraded: ibverbs-providers libibverbs1 rdma-core
2025-03-13 22:44:33,029 INFO Writing dpkg log to /var/log/unattended-upgrades/unattended-upgrades-dpkg.log
2025-03-13 22:44:34,421 INFO All upgrades installed
2025-03-13 22:44:34,855 INFO The list of kept packages can't be calculated in dry-run mode.
```

The correct *Origin* value to use is available in the repository's `InRelease` (or, for older formats, the `Release` file), which can be found at the URL of the repository, or locally on the system after an *apt-get update* command was run. Locally these files are in the `/var/lib/apt/lists/` directory. For example, for the PPA case, we have:

```text
/var/lib/apt/lists/ppa.launchpadcontent.net_canonical-server_server-backports_ubuntu_dists_noble_InRelease
```

Which has contents:
```text
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Origin: LP-PPA-canonical-server-server-backports
Label: Server Team Backports
Suite: noble
Version: 24.04
Codename: noble
Date: Tue, 03 Dec 2024  6:00:43 UTC
Architectures: amd64 arm64 armhf i386 ppc64el riscv64 s390x
Components: main
Description: Ubuntu Noble 24.04
(...)
```
And there we can see the *Origin*.


## How to block certain packages
Specific packages can also be excluded from an update. This is controlled via the `Unattended-Upgrade::Package-Blacklist` configuration option in `/etc/apt/apt.conf.d/50unattended-upgrades`, which contains a list of [Python Regular Expressions](https://docs.python.org/3/howto/regex.html). Each line of this list is checked against the available package updates, and if there is a match, that package is not upgraded.

> **Note**:
>
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
>
> The regular expressions used here behave as if the "`^`" character is present at the start, i.e., the `libc6$` expression will match `libc6`, but will NOT match `glibc6` for example.

Of course, this being a regular expression means we could also write the above like this:
```text
Unattended-Upgrade::Package-Blacklist {
    "libc(6|-bin)$";
}
```
Just be careful to not overuse the power of regular expressions: readability is key.

## Notifications
Besides logging, `unattended-upgrades` can also send out reports via email. There are two options that control this behavior in `/etc/apt/apt.conf.d/50unattended-upgrades`:

 - `Unattended-Upgrade::Mail "user@example.com";`: If set to an email address, this option wil trigger an email to this address containing an activity report. When this value is empty, or not set, (which is the default), no report is sent.
 - `Unattended-Upgrade::MailReport "on-change";`: This option controls when a report is sent:
   - `always`: Always send a report, regardless if upgrades were applied or not.
   - `only-on-error`: Only send a report if there was an error.
   - `on-change`: Only send a report if upgrades were applied. This is the default value.

> **Note**:
>
> Sending out emails like this requires the separate configuration of a package like [ssmtp](https://manpages.ubuntu.com/manpages/noble/man8/ssmtp.8.html) or another minimalistic mail client that is capable of sending messages to a mail server.

### Notification examples
Here are some email examples (lines wrapped for better legibility).

No changes applied, no errors. This would only be sent if `Unattended-Upgrade::MailReport` is set to `always`:
```email
Subject: unattended-upgrades result for <hostname>: SUCCESS

Unattended upgrade result: No packages found that can be upgraded
 unattended and no pending auto-removals

Unattended-upgrades log:
Starting unattended upgrades script
Allowed origins are: o=Ubuntu,a=noble, o=Ubuntu,a=noble-security,
 o=UbuntuESMApps,a=noble-apps-security,
 o=UbuntuESM,a=noble-infra-security, o=Ubuntu,a=noble,
 o=Ubuntu,a=noble-security, o=UbuntuESMApps,a=noble-apps-security,
 o=UbuntuESM,a=noble-infra-security
Initial blacklist:
Initial whitelist (not strict):
No packages found that can be upgraded unattended and no pending auto-removals
```

Upgrades applied, no errors. This is the default email report, when `Unattended-Upgrade::MailReport` is set to `on-change `:
```email
Subject: unattended-upgrades result for nuc1: SUCCESS

Unattended upgrade result: All upgrades installed

Packages that were upgraded:
 linux-firmware

Package installation log:
Log started: 2025-03-13  06:19:10
Preparing to unpack
 .../linux-firmware_20240318.git3b128b60-0ubuntu2.10_amd64.deb ...
Unpacking linux-firmware (20240318.git3b128b60-0ubuntu2.10) over
 (20240318.git3b128b60-0ubuntu2.9) ...
Setting up linux-firmware (20240318.git3b128b60-0ubuntu2.10) ...
Processing triggers for initramfs-tools (0.142ubuntu25.5) ...
update-initramfs: Generating /boot/initrd.img-6.8.0-55-generic

Running kernel seems to be up-to-date.

The processor microcode seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
Log ended: 2025-03-13  06:19:26



Unattended-upgrades log:
Starting unattended upgrades script
Allowed origins are: o=Ubuntu,a=noble, o=Ubuntu,a=noble-security,
 o=UbuntuESMApps,a=noble-apps-security,
 o=UbuntuESM,a=noble-infra-security, o=Ubuntu,a=noble,
 o=Ubuntu,a=noble-security, o=UbuntuESMApps,a=noble-apps-security,
 o=UbuntuESM,a=noble-infra-security
Initial blacklist:
Initial whitelist (not strict):
Packages that will be upgraded: linux-firmware
Writing dpkg log to /var/log/unattended-upgrades/unattended-upgrades-dpkg.log
All upgrades installed
```

## Reboots
Sometimes a system needs to be rebooted to fully apply an update. Such updates can use a mechanism in Ubuntu to let the system know that a reboot is recommended. `unattended-upgrades` can benefit from this mechanism and optionally reboot the system automatically when needed.

Reboots can be very disruptive, specially if the system fails to come back. There are some configuration options where this behavior can be adjusted:

 * `Unattended-Upgrade::Automatic-Reboot "false";`: If this option is set to `true`, the system will be rebooted ***without confirmation*** at the end of an upgrade run if a reboot was requested. The default value is `false`.
 * `Unattended-Upgrade::Automatic-Reboot-WithUsers "true";`: Automatically reboot even if there are users currently logged in when `Unattended-Upgrade::Automatic-Reboot` (the option above) is set to `true`. The default value is `true`.
 * `Unattended-Upgrade::Automatic-Reboot-Time "now";`: If automatic reboot is enabled and needed, reboot at the specific time instead of immediately. The time value is passed as-is to the [shutdown](https://manpages.ubuntu.com/manpages/noble/en/man8/shutdown.8.html) command. It can be the text "now" (which is the default), or in the format "hh:mm" (hours:minutes), or an offset in minutes specified like "+m". Note that if using "hh:mm", it will be in the local system's timezone.

> **Note**
>
> For more information about this time specification for the reboot, and other options like cancelling a scheduled reboot, see the [shutdown manpage](https://manpages.ubuntu.com/manpages/noble/en/man8/shutdown.8.html)

Below are the logs of an *unattended-upgrades* run that started at 20:43. The tool installed the available upgrades and detected that a reboot was requested, which was scheduled using the configured `Automatic-Reboot-Time` (20:45 in this example):
```text
2025-03-13 20:43:25,923 INFO Starting unattended upgrades script
2025-03-13 20:43:25,924 INFO Allowed origins are: o=Ubuntu,a=noble, o=Ubuntu,a=noble-security, o=UbuntuESMApps,a=noble-apps-security, o=UbuntuESM,a=noble-infra-security
2025-03-13 20:43:25,924 INFO Initial blacklist:
2025-03-13 20:43:25,924 INFO Initial whitelist (not strict):
2025-03-13 20:43:29,082 INFO Packages that will be upgraded: libc6 python3-jinja2
2025-03-13 20:43:29,082 INFO Writing dpkg log to /var/log/unattended-upgrades/unattended-upgrades-dpkg.log
2025-03-13 20:43:39,532 INFO All upgrades installed
2025-03-13 20:43:40,201 WARNING Found /var/run/reboot-required, rebooting
2025-03-13 20:43:40,207 WARNING Shutdown msg: b"Reboot scheduled for Thu 2025-03-13 20:45:00 UTC, use 'shutdown -c' to cancel."
```

## When to consider disabling automatic updates
While automatic security updates are enabled in Ubuntu by default, in some situations it might make sense to disable this feature, or carefully limit its reach.

Here are some considerations.

### Systems which just get redeployed
Some systems are not meant to receive updates, and just get redeployed instead from a new base image. This is very common in cloud and container based applications, where out-of-date instances are destroyed and replaced with newer ones. Such systems are usually very lean and very focused on the applications they run, and might not even have tools to self-update installed.

Just keep in mind that the security exposure is still there: it's just the update mechanism that is different, and comes in the form of a new deployment. The update still has to happen somewhere, it's just not at runtime. Until that new deployment is done, outdated software might still be running.

### Manual steps required
While Ubuntu updates rarely require manual steps to complete an upgrade (at most a reboot can be required), it could be plausible that other applications require some manual steps after or before an update is applied. If that is the case, and if such steps cannot be safely automated, then maybe *unattended-upgrades* should be disabled on such systems. But do make an effort to consider blocklisting such packages instead, if they are known to trigger such manual steps. In that case, the system can still benefit from all the other upgrades that might become available.

### Too much of a risk
Even with all the care in the world, applying updates to a running system comes with risk. Ubuntu believes that risk to be less than the risk of NOT applying a security update, which is why *unattended-upgrades* will apply security updates by default. But for some specific systems, the risk vs benefit equation might favor staying put and not applying an update unless specifically requested.

Always keep in mind, however, that specific packages can be blocked from receiving updates. For example, if a particular system runs a critical application that could break if certain libraries on the system are updated, then perhaps an acceptable compromise is to block these library packages from receiving upgrades, instead of disabling the whole feature.

### Fleet management
The *unattended-upgrades* feature is helpful, does its job, and even sends out reports. But it's not meant to be a replacement for fleet management software. If a large number of Ubuntu systems needs to be kept updated, other solutions are better suited for the job. Such large deployments usually come with much stricter and wider requirements, like:
 * compliance reports: How many systems are up-do-date, how many are still behind, for how long has a system been exposed to a known vulnerability, etc.
 * maintenance windows: Different systems might require different maintenance windows. Some can be updated anytime, others only on weekends, etc.
 * canary rollouts: The ability to rollout updates to an initial group of systems, and over time increase the number of systems which will receive the update.

An example of such a Fleet Management software for Ubuntu systems is [Landscape](https://ubuntu.com/landscape).


## Testing and troubleshooting
It's possible to test some configuration changes to *unattended-upgrade* without having to wait for the next time it would run. The `unattended-upgrade` tool has a [manual page](https://manpages.ubuntu.com/manpages/noble/man8/unattended-upgrade.8.html) which explains all its command-line options. Here are the most useful ones for testing and troubleshooting:

 * `-v`: Show a more verbose output.
 * `--dry-run`:  Just simulate what would happen, without actually making any changes.

For example, let's say we want to check if the PPA origin was included correctly in the *Allowed-Origins* configuration, and if an update that we know is available would be considered. After we add `"LP-PPA-canonical-server-server-backports:${distro_codename}";` to `Allowed-Origins` in `/etc/apt/apt.conf.d/50unattended-upgrades`, we can run the tool in verbose and dry-run modes to check what would happen:

```bash
sudo unattended-upgrade -v --dry-run
```

Which produces this output, in this example scenario:
```text
Starting unattended upgrades script
Allowed origins are: o=Ubuntu,a=noble, o=Ubuntu,a=noble-security, o=UbuntuESMApps,a=noble-apps-security, o=UbuntuESM,a=noble-infra-security, o=LP-PPA-canonical-server-server-backports,a=noble
Initial blacklist:
Initial whitelist (not strict):
Option --dry-run given, *not* performing real actions
Packages that will be upgraded: rdma-core
Writing dpkg log to /var/log/unattended-upgrades/unattended-upgrades-dpkg.log
/usr/bin/unattended-upgrade:567: DeprecationWarning: This process (pid=1213) is multi-threaded, use of fork() may lead to deadlocks in the child.
  pid = os.fork()
/usr/bin/dpkg --status-fd 10 --no-triggers --unpack --auto-deconfigure /var/cache/apt/archives/rdma-core_52.0-2ubuntu1~backport24.04.202410192216~ubuntu24.04.1_amd64.deb
/usr/bin/dpkg --status-fd 10 --configure --pending
All upgrades installed
The list of kept packages can't be calculated in dry-run mode.
```

Of note, we see:
 * `Allowed origins` include `o=LP-PPA-canonical-server-server-backports,a=noble`, which is the PPA we included.
 * The `rdma-core` package would be updated.

Let's check this `rdma-core` package with the command `apt-cache policy rdma-core`:
```text
rdma-core:
  Installed: 50.0-2build2
  Candidate: 52.0-2ubuntu1~backport24.04.202410192216~ubuntu24.04.1
  Version table:
     52.0-2ubuntu1~backport24.04.202410192216~ubuntu24.04.1 500
        500 https://ppa.launchpadcontent.net/canonical-server/server-backports/ubuntu noble/main amd64 Packages
 *** 50.0-2build2 500
        500 http://br.archive.ubuntu.com/ubuntu noble/main amd64 Packages
        100 /var/lib/dpkg/status
```
And indeed, there is an update available from that PPA, and the next time *unattended-upgrade* runs on its own, it will apply that update. In fact, if the `--dry-run` option is removed, the update will be installed.
