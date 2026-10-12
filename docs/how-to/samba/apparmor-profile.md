---
myst:
  html_meta:
    description: Create and configure AppArmor security profiles for Samba daemons smbd and nmbd to enforce mandatory access controls on Ubuntu.
---

(samba-apparmor-profile)=
# Create a Samba AppArmor profile

Ubuntu comes with the AppArmor security module, which provides mandatory access controls. The default AppArmor profile for Samba may need to be adapted to your configuration. More details on using AppArmor can be found in the {ref}`AppArmor guide <apparmor>`.

There are default AppArmor profiles for `/usr/sbin/smbd` and `/usr/sbin/nmbd`, the Samba daemon binaries, as part of the `apparmor-profiles` package. 

## Install extra profiles and utilities

To install the extra profiles and utilities, enter the following command from a terminal prompt:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install apparmor-profiles apparmor-utils
```

:::{note}
This package also contains profiles for several other applications.
:::

## AppArmor profile modes

By default, the profiles for `smbd` and `nmbd` are set to 'enforce' mode. There is no need to add rules for the shares, as the `smbd` service unit takes care of doing that automatically via a helper script whenever restarted. It will inspect the exported shares in `/etc/samba/smb.conf` and add the necessary AppArmor rules via a profile snippet in `/etc/apparmor.d/samba/smbd-shares`.

It's very likely that the AppArmor profile is not generic enough for all types of Samba deployments. How to develop or adjust an AppArmor profile is out of scope for this documentation, but in order to allow the service to at least run, while at the same time logging security violations, you can switch the profile to "complain" mode.

To place the profile into "complain" mode and reload it, run:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo aa-complain /usr/sbin/smbd
```

:::{tip}
Use the `aa-status` command to check the status of the AppArmor profiles.
:::

It's advisable to monitor the output of `dmesg -T` for `audit` entries that contain AppArmor `DENIED` messages, or the `/var/log/audit/audit.log` file if you are running the `auditd` daemon.
A typical AppArmor `ALLOWED` message looks like this:

`[Fri Oct 16 17:02:21 2026] audit: type=1400 audit(1791823465.352:33784): apparmor="ALLOWED" operation="open" class="file" namespace="root//lxd-r-share-acls_<var-snap-lxd-common-lxd>" profile="smbd" name="/files/" pid=1386536 comm="smbd[127.0.0.1]" requested_mask="r" denied_mask="r" fsuid=1001001 ouid=1000000`

Whereas a `DENIED` message looks exactly the same, but will state `DENIED` instead of `ALLOWED`.

Actions blocked by AppArmor may surface as odd or unrelated errors in the application, so keep that in mind if you have the profile in "enforce" mode and are experiencing issues with Samba.

## Further reading

- For more information on how to use AppArmor, including details of the profile modes, [the Debian AppArmor guide](https://wiki.debian.org/AppArmor/HowToUse) may be helpful.

- Upstream [AppARmor Documentation](https://apparmor.net/).
