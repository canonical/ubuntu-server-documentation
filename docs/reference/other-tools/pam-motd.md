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
  * [ubuntu-pro-client](https://documentation.ubuntu.com/pro-client/en/latest/explanations/motd_messages/) mentioned expiring pro subscriptions: `91-contract-ua-esm-status`
  * ubuntu-release-upgrader-core suggests upgrades: `91-release-upgrade`
  * unattended-upgrades informs if updates could not be installed automatically: `92-unattended-upgrades`
  * update-notifier-common notifies if the HWE kernel might go end of life: `95-hwe-eol`
  * overlayroot reports if any overlays are active: `97-overlayroot`
  * update-notifier-common suggests regular filesystem checks: `98-fsck-at-reboot`
  * update-notifier-common also hints if a reboot is required: `98-reboot-required`

## Customization

You can modify the configuration provided by the system or consider to add your
own dynamic information to the MOTD by adding to `/etc/update-motd.d/`.

This is example is not meant to be serious, instead it is a bit of fun to
demonstrate the usage of `pam_motd` for own messages.

```bash
#!/bin/bash

# 1. Get timestamp and and calculate nearest sysadminday
NOW=$(date +%s)
THIS_YEAR=$(date +%Y)
TARGET_PREV=$(date -d "$((THIS_YEAR-1))-08-01 last friday" +%s)
TARGET_CURR=$(date -d "$THIS_YEAR-08-01 last friday" +%s)
TARGET_NEXT=$(date -d "$((THIS_YEAR+1))-08-01 last friday" +%s)

# 2. Loop to find the shortest distance
MIN_DIFF=9999999999
CHOSEN_DAYS=0
TIMING=""
for TARGET in $TARGET_PREV $TARGET_CURR $TARGET_NEXT; do
    # Calculate difference
    DIFF=$(( (TARGET - NOW) / 86400 ))

    # Get absolute value for comparison
    if [ $DIFF -lt 0 ]; then
        ABS_DIFF=$((DIFF * -1))
        CURRENT_TIMING="ago"
    else
        ABS_DIFF=$DIFF
        CURRENT_TIMING="in"
    fi

    # Update if this is the closest date found so far
    if [ $ABS_DIFF -lt $MIN_DIFF ]; then
        MIN_DIFF=$ABS_DIFF
        CHOSEN_DAYS=$ABS_DIFF
        TIMING=$CURRENT_TIMING
    fi
done

# 3. Report to gain some admin-love
if [ "$CHOSEN_DAYS" -eq 0 ]; then
    echo -e "System Administrator Appreciation Day is Today! Gifts welcome."
elif [ "$TIMING" == "ago" ]; then
    echo -e "System Administrator Appreciation Day is ${CHOSEN_DAYS} days ago but we'd appreciate to be treated well every day."
else
    echo -e "System Administrator Appreciation Day is in ${CHOSEN_DAYS} days but we'd appreciate to be treated well every day."
fi
```

Then make it executable

```bash
chmod +x /etc/update-motd.d/98-admin-reminder
```

On next login you should now be greeted with that as part of the message of the day.

```text
$ ssh ubuntu@yoursystem
...
System Administrator Appreciation Day is 181 days ago but we'd appreciate to be treated well every day.
```


```{note}
Be careful as this will be executed on every login, the usual pattern to prevent
that from slowing down logins is to do anything even slightly complex
asynchronously and only `cat` pre-generated content in the actual MOTD handling.
Furthermore consider using stamp files to only update at regular intervals
instead of at every login.
This example was meant to be kept simple, but the existing serious MOTD entries
placed there by the packages make use of such, please look at those for writing
your own.
```

## Resources

  - See the {manpage}`update-motd(5)` manual page for more options available to update-motd.

  - The Debian Package of the Day [weather](https://debaday.debian.net/2007/10/04/weather-check-weather-conditions-and-forecasts-on-the-command-line/) article has more details about using the weather utility.
