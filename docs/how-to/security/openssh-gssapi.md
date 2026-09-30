---
myst:
  html_meta:
    description: How to use OpenSSH with GSSAPI/Kerberos authentication on Ubuntu.
---

(openssh-gssapi)=
# OpenSSH with GSSAPI/Kerberos authentication

OpenSSH can be configured to use {term}`GSSAPI`/{term}`Kerberos` authentication, which allows users to authenticate using their Kerberos tickets. This is particularly useful in environments where Kerberos is already in use, such as in many enterprise networks.

This guide assumes you have a working Kerberos realm, and does not cover setting one up. For background on Kerberos concepts, see {ref}`Introduction to Kerberos <introduction-to-kerberos>`; to deploy a realm on Ubuntu, see {ref}`the Kerberos how-to guides <how-to-kerberos>`.

## Which OpenSSH package to use

The packages to install depend on the Ubuntu release in use:

::::{tab-set}

:::{tab-item} Ubuntu Resolute 26.04 LTS and earlier

The GSSAPI/Kerberos support is included in the main OpenSSH packages:

* `openssh-server` on the server
* `openssh-client` on the client

:::

:::{tab-item} Ubuntu Stonking 26.10 and later

The GSSAPI/Kerberos support is split into separate packages, so use these:

* `openssh-server-gssapi` on the server
* `openssh-client-gssapi` on the client

:::

::::

To connect to a remote host using GSSAPI/Kerberos authentication, both the client and the server need to support it.

## Configure OpenSSH on the server

GSSAPI/Kerberos support is available on the server, but not enabled by default. To enable it, edit the OpenSSH server configuration file `/etc/ssh/sshd_config` and add or uncomment the following line:

```text
GSSAPIAuthentication yes
```

See the {manpage}`sshd_config(5)` manual page for other GSSAPI/Kerberos configuration options.

Restart the OpenSSH server to apply the changes:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo systemctl restart ssh.service
```

In order to participate in a Kerberos realm, the OpenSSH server needs to have a so-called service principal in the Kerberos database. The service principal for OpenSSH is of the form `host/<hostname>@<REALM>`, where `<hostname>` is the fully qualified domain name of the server and `<REALM>` is the Kerberos realm.

The service principal needs to be created in the Kerberos database and a keytab file needs to be generated for it. The keytab file should be placed in `/etc/krb5.keytab` on the OpenSSH server.

:::{note}
For more information on service principals, consult {ref}`Kerberos service principals <configure-service-principals>`.
:::

To create the service principal and extract its key into the keytab, use the {manpage}`kadmin(1) <kadmin.mit(1)>` tool on the OpenSSH server. You need a principal with administrative privileges in the Kerberos realm for this. The `kadmin` tool is in the `krb5-user` package:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install krb5-user
```

During installation, it will ask you for the Kerberos realm, and the KDC (Key Distribution Center) and Admin server hostnames. This guide uses the `EXAMPLE.COM` realm, and `server.example.com` as the hostname of the OpenSSH server.

Create the service principal, and extract its key into `/etc/krb5.keytab`. Run `kadmin` with `sudo`, because writing to `/etc/krb5.keytab` requires root privileges. Each command asks for the password of the administrative principal:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo kadmin -p ubuntu/admin@EXAMPLE.COM -q "addprinc -randkey host/server.example.com@EXAMPLE.COM"
```

```{terminal}
:copy:
:user:
:host:
:dir:
sudo kadmin -p ubuntu/admin@EXAMPLE.COM -q "ktadd host/server.example.com@EXAMPLE.COM"
```

:::{note}
`user/admin` is normally how administrative principals are named. You would have the normal `user@REALM` principal for everyday tasks, and the admin "instance" (denoted by `/admin`) is recognized as having extra privileges. See {ref}`Configure the Kerberos server <install-a-kerberos-server-configure>` for more information.
:::

The contents of the keytab can be verified with the {manpage}`klist(1) <klist.mit(1)>` command:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo klist -ke

Keytab name: FILE:/etc/krb5.keytab
KVNO Principal
---- --------------------------------------------------------------------------
   2 host/server.example.com@EXAMPLE.COM (aes256-cts-hmac-sha384-192)
   2 host/server.example.com@EXAMPLE.COM (aes256-cts-hmac-sha1-96)
   2 host/server.example.com@EXAMPLE.COM (aes128-cts-hmac-sha1-96)
```

The server is now ready to accept GSSAPI/Kerberos authentication from clients that have valid Kerberos tickets.

## Configure OpenSSH on the client

In Ubuntu, the `openssh-client` (or `openssh-client-gssapi`) package already defaults to allowing GSSAPI/Kerberos authentication, so no additional configuration is needed on the client side. However, you may want to verify that the following line is present in `/etc/ssh/ssh_config`:

```text
GSSAPIAuthentication yes
```

This can also be configured on a per-user and per-target-host basis in `~/.ssh/config`.

Like with the server options, there are multiple configuration options related to GSSAPI/Kerberos for the client. Consult the {manpage}`ssh_config(5)` manual page for more information.

Since the client needs to have a valid Kerberos ticket in order to authenticate with GSSAPI/Kerberos, you will need to obtain a ticket with {manpage}`kinit(1) <kinit.mit(1)>` before connecting to the server. Install the `krb5-user` package on the client, answering the same questions as on the server:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install krb5-user
```

:::{note}
Some Ubuntu deployments may be configured to obtain a Kerberos ticket automatically at login, in which case you may not need to run `kinit` manually. But it's still useful to have the `krb5-user` package installed, as it provides the `klist` command to verify that you have a valid ticket.
:::

First obtain the {term}`TGT` (Ticket Granting Ticket) for your user principal, if you don't have it already. This example uses an `ubuntu` principal:

```{terminal}
:copy:
:user: ubuntu
:host: client
:dir: ~
kinit

Password for ubuntu@EXAMPLE.COM:
```

Confirm you have the TGT:

```{terminal}
:copy:
:user: ubuntu
:host: client
:dir: ~
klist

Ticket cache: FILE:/tmp/krb5cc_1000
Default principal: ubuntu@EXAMPLE.COM

Valid starting     Expires            Service principal
09/29/26 21:29:39  09/30/26 07:29:39  krbtgt/EXAMPLE.COM@EXAMPLE.COM
```

And now ssh to the GSSAPI/Kerberos-enabled OpenSSH server:

```{terminal}
:copy:
:user: ubuntu
:host: client
:dir: ~
ssh server.example.com

Welcome to Ubuntu 26.04.1 LTS
...
ubuntu@server:~$
```

The server administrator can check the `/var/log/auth.log` file to verify that the user authenticated with GSSAPI/Kerberos:

```text
sshd-session[954]: Accepted gssapi-with-mic for ubuntu from 10.0.10.157 port 55992 ssh2: ubuntu@EXAMPLE.COM
```

If you log out and run `klist` on the client, you will see that you now have a service ticket for the OpenSSH server:

```{terminal}
:copy:
:user: ubuntu
:host: client
:dir: ~
klist

Ticket cache: FILE:/tmp/krb5cc_1000
Default principal: ubuntu@EXAMPLE.COM

Valid starting     Expires            Service principal
09/29/26 21:29:39  09/30/26 07:29:39  krbtgt/EXAMPLE.COM@EXAMPLE.COM
        renew until 09/30/26 21:29:37
09/29/26 21:29:59  09/30/26 07:29:39  host/server.example.com@
        renew until 09/30/26 21:29:37
        Ticket server: host/server.example.com@EXAMPLE.COM
```

## Forwarding Kerberos tickets

It is possible to forward a Kerberos ticket to the remote server when logging in via SSH. This allows the user to use their Kerberos credentials on the remote server, for example to access other services that require Kerberos authentication.

This is controlled by the client option called `GSSAPIDelegateCredentials`. To enable it, add the following line to your `~/.ssh/config` file, or have an administrator add it to the system-wide `/etc/ssh/ssh_config` file:

```text
GSSAPIDelegateCredentials yes
```

With this in place, the next time you ssh into the server, you will notice that you also have a Kerberos ticket there:

```{terminal}
:copy:
:user: ubuntu
:host: client
:dir: ~
ssh server.example.com

Welcome to Ubuntu 26.04.1 LTS
...
```

```{terminal}
:copy:
:user: ubuntu
:host: server
:dir: ~
klist

Ticket cache: FILE:/tmp/krb5cc_1000_Qvc5QcHuit
Default principal: ubuntu@EXAMPLE.COM

Valid starting     Expires            Service principal
09/29/26 21:47:13  09/30/26 07:29:39  krbtgt/EXAMPLE.COM@EXAMPLE.COM
        renew until 09/30/26 21:29:37
```

:::{note}
Tickets can only be forwarded if allowed by the Kerberos server. That is the default, but it may be disallowed in your realm. You can check if your ticket is forwardable by running `klist -f` on the client. It should have the "`F`" flag set if it's forwardable.
:::

The ticket cache file on the server is again created in `/tmp` by default, but this time with an extra random suffix appended to the filename to avoid collisions if the same user forwards another ticket from another client.

### Ticket cache location

The ccache type and location are normally controlled by the `default_ccache_name` option in the `[libdefaults]` section of `/etc/krb5.conf` (see {manpage}`krb5.conf(5)`). This option is read by the Kerberos library, and is treated as a library-provided default for tools linked with it.

For example, to store tickets in the kernel keyring instead of a file in `/tmp`, add or edit the following line in `/etc/krb5.conf` on the client:

```text
default_ccache_name = KEYRING:persistent:%{uid}
```

Running `kinit` and then `klist` on the client confirms the change:

```{terminal}
:copy:
:user: ubuntu
:host: client
:dir: ~
kinit

Password for ubuntu@EXAMPLE.COM:
```

```{terminal}
:copy:
:user: ubuntu
:host: client
:dir: ~
klist

Ticket cache: KEYRING:persistent:1000:1000
Default principal: ubuntu@EXAMPLE.COM

Valid starting     Expires            Service principal
09/30/26 13:48:24  09/30/26 23:48:24  krbtgt/EXAMPLE.COM@EXAMPLE.COM
        renew until 10/01/26 13:48:21
```

For forwarded tickets, it's the OpenSSH server that creates the ccache, not `kinit`, and the `/etc/krb5.conf` that matters is the one on the server. The same setting on the server doesn't always take effect, though: it depends on the Ubuntu release the server is running.

OpenSSH in Ubuntu Resolute 26.04 LTS and earlier ignores the `default_ccache_name` setting in `/etc/krb5.conf` on the server, so the forwarded ticket will still be stored in `/tmp` with a random suffix.

But starting with Ubuntu Stonking 26.10, the OpenSSH server will follow the `default_ccache_name` setting in `/etc/krb5.conf` on the server by default for forwarded tickets. This OpenSSH behavior is controlled by the `KerberosUniqueCCache` option in `/etc/ssh/sshd_config`. If this option is set to `no` (the default), the server will use the `default_ccache_name` setting in `/etc/krb5.conf` to determine the location and type of the ticket cache for forwarded tickets. If it is changed to `yes`, the server will always use `/tmp` with a random suffix as in previous Ubuntu releases.

If there is no `default_ccache_name` setting in `/etc/krb5.conf` on the server, the behavior is unchanged from Ubuntu Resolute 26.04 LTS and earlier.

The following table summarizes where the OpenSSH server stores forwarded tickets:

| Ubuntu release | `default_ccache_name` on the server | `KerberosUniqueCCache` on the server | Forwarded ticket ccache |
|---|---|---|---|
| ≤ 26.04 LTS | Ignored by OpenSSH | Not available | `FILE:/tmp/krb5cc_<uid>_<random>` |
| ≥ 26.10 | Not set | `no` (default) or `yes` | `FILE:/tmp/krb5cc_<uid>_<random>` |
| ≥ 26.10 | Set | `yes` | `FILE:/tmp/krb5cc_<uid>_<random>` |
| ≥ 26.10 | Set | `no` (default) | As specified by `default_ccache_name` |

Here is an example forwarding a Kerberos ticket to an Ubuntu Stonking 26.10 server with the `default_ccache_name` set to `KEYRING:persistent:%{uid}` in `/etc/krb5.conf` on the server:

```{terminal}
:copy:
:user: ubuntu
:host: client
:dir: ~
ssh stonking-server.example.com

Welcome to Ubuntu Stonking Stingray (...)
...
```

```{terminal}
:copy:
:user: ubuntu
:host: stonking-server
:dir: ~
klist

Ticket cache: KEYRING:persistent:1000:krb_ccache_MU8uJl4
Default principal: ubuntu@EXAMPLE.COM

Valid starting     Expires            Service principal
09/30/26 14:00:40  09/30/26 23:48:24  krbtgt/EXAMPLE.COM@EXAMPLE.COM
        renew until 10/01/26 13:48:21
```

```{terminal}
:copy:
:user: ubuntu
:host: stonking-server
:dir: ~
grep default_ccache_name /etc/krb5.conf

    default_ccache_name = KEYRING:persistent:%{uid}
```

## See also

* {ref}`Introduction to Kerberos <introduction-to-kerberos>`
* {ref}`How to deploy Kerberos on Ubuntu <how-to-kerberos>`
* {ref}`Configuring Kerberos service principals <configure-service-principals>`
