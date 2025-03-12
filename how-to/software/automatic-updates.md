(automatic-updates)=
# Automatic updates

The `unattended-upgrades` package can be used to automatically update installed packages and can be configured to update all packages or to only install security updates. First, install the package by entering the following in a terminal:

```bash
sudo apt install unattended-upgrades
```

To configure `unattended-upgrades`, edit `/etc/apt/apt.conf.d/50unattended-upgrades`.

The `Allowed-Origins` section specifies which release pockets will be used to gather updates from. See the [Ubuntu Packaging Guide](https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/#pockets) for additional information about each pocket. Adjust the section to fit your needs:

```text
Unattended-Upgrade::Allowed-Origins {
        "${distro_id}:${distro_codename}";
        "${distro_id}:${distro_codename}-security";
//      "${distro_id}:${distro_codename}-updates";
//      "${distro_id}:${distro_codename}-proposed";
//      "${distro_id}:${distro_codename}-backports";
};
```

Certain packages can also be excluded and therefore will not be automatically updated. To block a package, add it to the list:

```text
Unattended-Upgrade::Package-Blacklist {
//      "vim";
//      "libc6";
//      "libc6-dev";
//      "libc6-i686";
};
```

> **Note**:
> The double “//” serve as comments, so whatever follows "//" will not be evaluated.

To enable automatic updates, edit `/etc/apt/apt.conf.d/20auto-upgrades` and set the appropriate APT configuration options:

```text
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
```

The above configuration updates the package list, then downloads and installs available upgrades every day. These actions are triggered by timer units at a set time but with a random delay:  `apt-daily.timer` and `apt-daily-upgrade.timer`. These timers activate the corresponding services that run the `/usr/lib/apt/apt.systemd.daily` script.

However, it may happen that if the server is off at the time the timer unit elapses, the timer will be triggered immediately at the next startup. As a result, they will often run on system startup 
and thereby cause immediate activity and hold the apt-lock.

In many cases this is beneficial, but in some cases it might be counter-productive; examples are administrators with many shut-down machines or VM images that are only started for some quick action, which is delayed or even blocked by the unattended upgrades. To adapt this behaviour, we can change/override the configuration of both APT's timer units [`apt-daily-upgrade.timer, apt-daily.timer`]. To do so, use `systemctl edit <timer_unit>` and override the *Persistent* attribute, for example with `Persistent=delay`:

```
[Timer]
Persistent=delay
```

The local download archive is cleaned every week. On servers upgraded to newer versions of Ubuntu, depending on your responses, the file listed above may not be there. In this case, creating a new file of the same name should also work.

> **Note**:
> You can read more about `apt` *Periodic* configuration options in the `apt.conf(5)` manpage and in the `/usr/lib/apt/apt.systemd.daily` script header.

The results of `unattended-upgrades` will be logged to `/var/log/unattended-upgrades`.

## Notifications

Configuring `Unattended-Upgrade::Mail` in `/etc/apt/apt.conf.d/50unattended-upgrades` will enable `unattended-upgrades` to email an administrator detailing any packages that need upgrading or have problems.

Another useful package is `apticron`. `apticron` will configure a cron job to email an administrator information about any packages on the system that have updates available, as well as a summary of changes in each package.

To install the `apticron` package, enter the following command in a terminal:

```bash
sudo apt install apticron
```

Once the package is installed, edit `/etc/apticron/apticron.conf`, to set the email address and other options:

```text
EMAIL="root@example.com"
```
