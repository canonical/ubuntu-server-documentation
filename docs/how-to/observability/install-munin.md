---
myst:
  html_meta:
    description: Set up Munin performance monitoring system with master and node configuration for network-wide server resource monitoring on Ubuntu.
---

(install-munin)=
# How to install and configure Munin

The monitoring of essential servers and services is an important part of system administration. This guide will show you how to set up [Munin](https://munin-monitoring.org/) for performance monitoring.

In this example, we will use two servers with {term}`hostnames <hostname>`: **`server01`** and **`server02`**. 

`Server01` will be set up with the `munin` package to gather information from the network. Using the `munin-node` package, `server02` will be configured to send information to `server01`.

## Prerequisites

Before installing Munin on `server01`, {ref}`Apache2 will need to be installed <introduction-to-web-servers>`. The default configuration is fine for running a `munin` server.

## Install `munin` and `munin-node`

First, on `server01` install the `munin` package. In a terminal enter the following command:

```bash
sudo apt install munin
```

Now on `server02`, install the `munin-node` package:

```bash
sudo apt install munin-node
```

## Configure `munin`

On `server01` edit the `/etc/munin/munin.conf` file, adding the IP address for `server02`:

```text
## First our "normal" host.
[server02]
       address 172.18.100.101
```

```{note}
Replace `server02` and `172.18.100.101` with the actual hostname and IP address for your server.
```

Then, if you wish to access the munin reports from a different host other than `server01`, you will also need to edit the `Directory` directives in `/etc/apache2/conf-enabled/munin.conf`. For instance, you may want to allow access to some specific IP address. To do so, add the following snippet below each `Require local` entry:

```text
    Require ip 172.18.100.1
```

```{note}
Replace `172.18.100.1` with the actual IP address for the host you want to allow.
```

## Configure `munin-node`

Next, configure `munin-node` on `server02`. Edit `/etc/munin/munin-node.conf` to allow access by `server01`:

```text
allow ^172\.18\.100\.100$
```

```{note}
Replace `^172\.18\.100\.100$` with the IP address for your `munin` server.
```

Now restart `munin-node` on `server02` for the changes to take effect:

```bash
sudo systemctl restart munin-node.service
```

## Test the setup

In a browser, go to `http://server01/munin`, and you should see links to nice graphs displaying information from the standard **munin-plugins** for disk, network, processes, and system. However, it should be noted that since this is a new installation, it may take some time for the graphs to display anything useful.


## Additional Plugins

The `munin-plugins-extra` package contains performance checks and additional services such as {term}`DNS`, {term}`DHCP`, and Samba, etc. To install the package, from a terminal enter:

```bash
sudo apt install munin-plugins-extra
```

Be sure to install the package on both the server and node machines.

```{note}
The `munin` package recommends `munin-node`, which recommends `munin-plugins-extra`. This means that in the most common use cases, you will already have `munin-plugins-extra` installed after following the instructions in this page.
```

## References

- See the [Munin](https://munin-monitoring.org/) website for more details.

- Specifically the [Munin Documentation](https://munin.readthedocs.io/en/latest/) page includes information on additional plugins, writing plugins, etc.
