---
myst:
  html_meta:
    description: Install NVIDIA's DOCA-OFED on Ubuntu 26.04 LTS and later releases.
---

(install-doca-ofed)=
# Install and maintain DOCA-OFED

This guide explains how to install and maintain DOCA-OFED on Ubuntu Server.

:::{note}
[DOCA-OFED](https://developer.nvidia.com/networking/doca) is NVIDIA's distribution of OpenFabrics Enterprise Distribution (OFED) drivers and userspace libraries for high-performance networking.

DOCA-OFED is available for Ubuntu 26.04 LTS (Resolute Raccoon).
:::

## Available metapackages

The following DOCA-OFED metapackages are provided:

| Metapackage | Kernel flavor |
| --- | --- |
| `doca-ofed-aws` | `aws` |
| `doca-ofed-aws-64k` | `aws-64k` |
| `doca-ofed-azure` | `azure` |
| `doca-ofed-azure-fde` | `azure-fde` |
| `doca-ofed-gcp` | `gcp` |
| `doca-ofed-gcp-64k` | `gcp-64k` |
| `doca-ofed-generic` | `generic` |
| `doca-ofed-generic-64k` | `generic-64k` |
| `doca-ofed-generic-64k-hwe-26.04` | `generic-64k-hwe-26.04` |
| `doca-ofed-generic-64k-hwe-26.04-edge` | `generic-64k-hwe-26.04-edge` |
| `doca-ofed-generic-hwe-26.04` | `generic-hwe-26.04` |
| `doca-ofed-generic-hwe-26.04-edge` | `generic-hwe-26.04-edge` |
| `doca-ofed-oracle` | `oracle` |
| `doca-ofed-oracle-64k` | `oracle-64k` |

## Install DOCA-OFED

To install the latest available DOCA-OFED version for your kernel flavor, use {manpage}`uname(1)` to identify your running kernel variant:

```{terminal}
:copy:
:user:
:host:
:dir:
uname -r
```

Add the stable DOCA PPA using {manpage}`add-apt-repository(1)`:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo add-apt-repository -y ppa:canonical-nvidia/doca-stable
```

Install the DOCA-OFED metapackage that matches your kernel flavor with {manpage}`apt(8)`:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install -y doca-ofed-<your_kernel_flavor>
```

For example, if `uname -r` returns `6.17.0-20-generic`, you should install:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install -y doca-ofed-generic
```

Finally, reboot the machine.

## Maintain and upgrade DOCA-OFED

When a newer DOCA-OFED package for your platform is published, it appears in:

```{terminal}
:copy:
:user:
:host:
:dir:
apt list --upgradable
```

For regular system updates, run:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt update && sudo apt full-upgrade
```

Then reboot the machine.

:::{warning}
Use `sudo apt full-upgrade` for DOCA-OFED updates. Do not use only `sudo apt upgrade` for this workflow. (DOCA-OFED updates from our PPA require uninstalling the old version's package names and installing the new version's package names (ex: `doca-ofed-userspace-3.3` is uninstalled, and `doca-ofed-userspace-3.4` is installed on update). `sudo apt upgrade` will hold such updates back.)
:::

## Collect a sosreport for support

If you need to collect a sosreport as part of a support request to NVIDIA, first find the installed `doca-ofed-userspace` package and note the `doca_version` suffix:

```{terminal}
:copy:
:user:
:host:
:dir:
apt list --installed | grep doca-ofed-userspace
```

Next, install the matching sosreport package:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install doca-sosreport-<doca_version>
```

Then, follow NVIDIA's sosreport instructions.