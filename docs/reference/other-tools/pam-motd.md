---
myst:
  html_meta:
    description: "Reference documentation for pam_motd, the PAM infrastructure that generates and displays message-of-the-day on login at an Ubuntu Server."
---

(pam-motd)=
# pam_motd

When logging into an Ubuntu server you may have noticed the informative Message Of The Day (MOTD).

## Packages adding to MOTD

There are various packages that add to the MOTD by placing configuration in `/etc/update-motd.d/`.

### Landscape-sysinfo

Here one example that is about system information obtained and displayed due to landscape:

  - *`landscape-common`:* provides the core libraries of `landscape-client`, which is needed to manage systems with [Landscape](https://ubuntu.com/landscape) (proprietary). Yet the package also includes the `landscape-sysinfo` utility which is responsible for displaying core system data involving CPU, memory, disk space, etc. For instance:

    ```text
    System load:             0.0
    Usage of /:              25.7% of 8.55GB
    Memory usage:            31%
    Swap usage:              0%
    Processes:               125
    Users logged in:         0
    IPv4 address for enp5s0: 10.185.198.41
    IPv6 address for enp5s0: fd42:50cb:3a48:1f2c:216:3eff:fe27:c18a
    ```

    ```{note}
    You can run `landscape-sysinfo` manually at any time.
    ```

  - *`update-notifier-common`:* provides information on available package updates, impending {term}`filesystem checks (fsck) <fsck>`, and required reboots (e.g.: after a kernel upgrade).

`pam_motd` executes the scripts in `/etc/update-motd.d` in order based on the number prepended to the script. The output of the scripts is written to `/var/run/motd`, keeping the numerical order, then concatenated with `/etc/motd.tail`.

## Other default MOTD entries

The default content in `/etc/update-motd.d/` in 26.04 covers (most of them only deliver output if there is something meaningful to report):

  * base-files establishing the basic mechanism: `00-header`, `10-help-text,`, `50-motd-news`
  * base-files also provides Ubuntu news: `50-motd-news`
  * landscape info about the system: `50-landscape-sysinfo`
  * fwupd presents potential firmware updates: `85-fwupd`
  * update-notifier-common reports about available updates: `90-updates-available`
  * ubuntu-pro-client mentioned expiring pro subscriptions: `91-contract-ua-esm-status`
  * ubuntu-release-upgrader-core suggests upgrades: `91-release-upgrade`
  * unattended-upgrades informs if updates could not be installed automatically: `92-unattended-upgrades`
  * update-notifier-common notifies if the HWE kernel might go end of life: `95-hwe-eol`
  * overlayroot reports if any overlays are active: `97-overlayroot`
  * update-notifier-common suggests regular filesystem checks: `98-fsck-at-reboot`
  * update-notifier-common also hints if a reboot is required: `98-reboot-required`

## Resources

  - See the {manpage}`update-motd(5)` manual page for more options available to update-motd.

  - The Debian Package of the Day [weather](https://debaday.debian.net/2007/10/04/weather-check-weather-conditions-and-forecasts-on-the-command-line/) article has more details about using the weather utility.
