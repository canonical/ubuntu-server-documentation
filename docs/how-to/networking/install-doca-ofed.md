---
myst:
  html_meta:
    description: Install DOCA-OFED on Ubuntu 26.04 LTS
---

(install-doca-ofed)=
# Install and maintain DOCA-OFED

This guide explains how to install and maintain DOCA-OFED on Ubuntu Server.

```{note}
DOCA-OFED is available for Ubuntu 26.04 LTS (Resolute Raccoon).
```

### Determine your kernel flavor

Use {manpage}`uname(1)` to identify your running kernel variant:

```bash
uname -r
```

For example, if `uname -r` returns `6.17.0-20-generic`, install:

```bash
sudo apt install -y doca-ofed-generic
```

## Available metapackages

The following DOCA-OFED metapackages are currently provided:

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

To install the latest available DOCA-OFED version:

1. Add the stable DOCA PPA:

   Use {manpage}`add-apt-repository(1)`:

   ```bash
   sudo add-apt-repository -y ppa:canonical-nvidia/doca-stable
   ```

1. Install the DOCA-OFED metapackage that matches your kernel flavor:

   Use {manpage}`apt(8)`:

   ```bash
   sudo apt install -y doca-ofed-<your_kernel_flavor>
   ```

1. Reboot the machine.

## Maintain and upgrade DOCA-OFED

When a newer DOCA-OFED package for your platform is published, it appears in:

```bash
apt list --upgradable
```

For regular system updates, run:

```bash
sudo apt update && sudo apt full-upgrade
```

Then reboot the machine.

```{warning}
Use `sudo apt full-upgrade` for DOCA-OFED updates. Do not use only `sudo apt upgrade` for this workflow.
```

## Collect a sosreport for support

If you need to collect an sosreport:

1. Find the installed `doca-ofed-userspace` package and note the `doca_version` suffix:

   ```bash
   apt list --installed | grep doca-ofed-userspace
   ```

1. Install the matching sosreport package:

   ```bash
   sudo apt install doca-sosreport-<doca_version>
   ```

1. Follow NVIDIA's sosreport instructions.