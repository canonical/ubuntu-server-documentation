---
myst:
  html_meta:
    description: Configure an Ubuntu system as an LDAP client using nslcd and NSS to make directory users and groups available for local authentication.
---

(ldap-client)=
# Set up an LDAP client

This guide explains how to configure an Ubuntu machine as a [Lightweight Directory Access Protocol (LDAP)](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol) client, so that users and groups stored in an LDAP directory become available on the system for authentication. This enables users to log in via SSH or other services backed by [Pluggable Authentication Modules (PAM)](https://en.wikipedia.org/wiki/Pluggable_Authentication_Module) using their LDAP credentials.

The approach used here is `nslcd` with `libnss-ldapd` and `libpam-ldapd`. The Name Service Switch ({term}`NSS`) and PAM modules communicate with the `nslcd` daemon, which maintains a single shared LDAP connection rather than each process opening its own. This keeps the setup lightweight and easy to debug.

```{note}
Ubuntu also supports [SSSD](https://sssd.io/) as an alternative LDAP client. SSSD provides credential caching and offline authentication. If you need those features, see {ref}`sssd-with-ldap` instead.
```

## Prerequisites

- A reachable LDAP server. To set one up, see {ref}`install-openldap`.
- The server's base Distinguished Name ({term}`DN`) and URI.
- The system CA certificates must trust the LDAP server's TLS certificate. See {ref}`ldap-and-tls` for guidance on TLS setup.

## Install the LDAP client daemon

Install `nslcd` and its PAM integration library:

```bash
sudo apt install nslcd libpam-ldapd libnss-ldapd
```

The installer prompts for your LDAP server URI and base DN. For example:

- **LDAP server URI:** `ldaps://ldap.example.com`
- **Base DN:** `dc=example,dc=com`

Installing `libnss-ldapd` updates `/etc/nsswitch.conf` to include `ldap` as a source for `passwd`, `group`, and `shadow` lookups.

## Configure nslcd

Review and adjust `/etc/nslcd.conf`. A minimal configuration looks like this:

```text
# /etc/nslcd.conf
uid nslcd
gid nslcd

uri ldaps://ldap.example.com

base dc=example,dc=com

tls_reqcert demand
tls_cacertfile /etc/ssl/certs/ca-certificates.crt
```

Adjust `uri` and `base` to match your directory. The `tls_reqcert demand` setting ensures the server certificate is verified. See {manpage}`nslcd.conf(5)` for all available options.

## Set up PAM

The installer updates `/etc/pam.d/common-*` automatically. To confirm that LDAP authentication and automatic home directory creation are enabled, run:

```bash
sudo pam-auth-update
```

Select **LDAP Authentication** and **Create home directory on login** in the interactive menu.

Restart `nslcd` to apply the configuration:

```bash
sudo systemctl restart nslcd
```

## Test the configuration

Verify that a known LDAP user is visible to the system:

```bash
id <username>
```

List all users known to {term}`NSS`, including those from LDAP:

```bash
getent passwd
```

List all groups:

```bash
getent group
```

If the output includes users and groups from the LDAP directory, {term}`NSS` integration is working correctly.

If this doesn't work, you can inspect live LDAP queries.
Stop the `nslcd` service and run it in the foreground in "debug" mode:

```bash
sudo systemctl stop nslcd.service
sudo nslcd -n -d
```

Press {kbd}`Ctrl+C` to stop this debug session.

You can iterate with configuration or setup adjustments until the log output and `getent` results are satisfying.


Finally, restart the service via {ref}`systemctl`:

```bash
sudo systemctl start nslcd.service
```


## Configure home directories

By default, `nslcd` uses the `homeDirectory` attribute from the LDAP directory. You can remap this — or any other {manpage}`passwd(5)` field — in `/etc/nslcd.conf` using `map` directives. For example, to construct home directory paths locally regardless of what the LDAP directory provides:

```text
map passwd homeDirectory /home/$uid
```

See {manpage}`nslcd.conf(5)` for the full list of mappable attributes.

## Restrict login access

By default, all users visible via LDAP can log in. To restrict which users are permitted, use `pam_access`.

Edit `/etc/security/access.conf` to define the allowed users and groups:

```conf
# Allow members of specific LDAP groups
+:(some-admin-group) (some-user-group):ALL
# Allow the local root user and members of the local "login" group (group name is customizable)
+:root (login):ALL
# Deny everyone else
-:ALL:ALL
```

Replace `some-admin-group` and `some-user-group` with your actual LDAP group names.

To process this config file, activate the `pam_access` module by creating a PAM configuration snippet at `/usr/share/pam-configs/ldap-access`:

```text
Name: LDAP group-based login access
Default: yes
Priority: 128
Auth-Type: Additional
Auth:
        required    pam_access.so nodefgroup
Account-Type: Primary
Account:
        required    pam_access.so nodefgroup
Session-Type: Additional
Session:
        required    pam_access.so nodefgroup
```

Apply the configuration to add these modules to `/etc/pam.d/common-*`:

```bash
sudo pam-auth-update --enable ldap-access --enable ldap --enable mkhomedir
```

```{note}
Local users not in any listed LDAP group can be permitted to log in by adding them to a local `login` group.
The `login` group is allowed to log in through `/etc/security/access.conf`, see above.
Create the group and add users as needed:

    sudo groupadd -r login
    sudo usermod -aG login <username>
```

## Grant sudo access to an LDAP group

You can grant "administration privileges" via `sudo` through group memberships in your LDAP directory.

To allow members of an LDAP group to use `sudo` access, add an entry to `/etc/sudoers` using {manpage}`visudo(8)`:

```text
%your-admin-group   ALL=(ALL) ALL
```

To allow `sudo` usage without entering a password, add this entry instead using {manpage}`visudo(8)`:
```text
%your-admin-group   ALL=(ALL) NOPASSWD: ALL
```

Replace `your-admin-group` with the relevant LDAP group name.
Granting `sudo` access with a remote group like this is no different from using local groups.

## Retrieve SSH public keys from LDAP

If your LDAP schema stores SSH public keys (for example in the `sshPublicKey` attribute), you can configure `sshd` to retrieve them automatically. Add the following to `/etc/ssh/sshd_config`:

```text
AuthorizedKeysCommand /usr/local/bin/ssh-ldap-key %u
AuthorizedKeysCommandUser nobody
```

The following Python script can serve as `/usr/local/bin/ssh-ldap-key`. It performs an anonymous LDAP search for the given username and prints any `sshPublicKey` values it finds. Install the `python3-ldap3` package before use:

```bash
sudo apt install python3-ldap3
```

```python
#!/usr/bin/env python3
"""Fetch SSH public keys for a user from an LDAP directory."""

import argparse
import logging
import ldap3


def main():
    cli = argparse.ArgumentParser(description="SSH key fetcher from LDAP")
    cli.add_argument("username")
    cli.add_argument("--ldap-server", default="ldaps://ldap.example.com")
    cli.add_argument("--base-dn", default="dc=example,dc=com")
    cli.add_argument("--verbose", "-v", action="count", default=0)
    args = cli.parse_args()

    log_level = (logging.WARNING, logging.INFO, logging.DEBUG)[min(args.verbose, 2)]
    logging.basicConfig(level=log_level, format="[%(asctime)s] %(message)s")

    for key in fetch_keys(args.username, args.ldap_server, args.base_dn):
        print(key)


def fetch_keys(user, server, basedn):
    conn = ldap3.Connection(server)
    if not conn.bind():
        raise RuntimeError(f"anonymous bind to {server!r} failed")

    uid = ldap3.utils.conv.escape_filter_chars(user)
    ok = conn.search(
        basedn,
        f"(&(objectClass=inetOrgPerson)(uid={uid}))",
        attributes=["sshPublicKey"],
    )
    if not ok:
        raise RuntimeError(f"LDAP search failed: {conn.result}")
    if not conn.entries:
        return []
    if len(conn.entries) > 1:
        raise RuntimeError(f"ambiguous username: {len(conn.entries)} entries returned")

    return [
        ldap3.utils.conv.to_unicode(key)
        for key in conn.entries[0].sshPublicKey
    ]


if __name__ == "__main__":
    main()
```

Make the script executable and owned by root:

```bash
sudo install -o root -g root -m 0755 ssh-ldap-key /usr/local/bin/ssh-ldap-key
```

After modifying `sshd_config`, restart the SSH service:

```bash
sudo systemctl restart ssh
```

## Further reading

- {ref}`install-openldap`
- {ref}`sssd-with-ldap`
- {ref}`ldap-and-tls`
- {manpage}`nslcd(8)`, {manpage}`nslcd.conf(5)`, {manpage}`pam_access(8)`, {manpage}`visudo(8)`
