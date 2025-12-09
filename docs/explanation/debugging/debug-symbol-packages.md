---
myst:
  html_meta:
    description: "Understand debug symbol packages on Ubuntu Server for debugging applications with detailed symbol information."
---

(debug-symbol-packages)=
# Debug symbol packages

If you want to debug a crash – whether in a project you are developing yourself or from a third-party package – or if you frequently need the debug symbols for specific libraries, it might be helpful to install them permanently on your system if you can’t use debuginfod.

This document describes how to set up the debugging symbol packages (`*-dbg.deb` and `*-dbgsym.ddeb`). You might need to do this when you are performing tasks like a [backtrace](https://wiki.ubuntu.com/Backtrace) or using [Valgrind](https://wiki.ubuntu.com/Valgrind).

## Debuginfod

If you are on Ubuntu Jammy (22.04) or later, you don't need to worry about installing debug symbol packages since the Ubuntu project maintains a [Debuginfod](about-debuginfod.md) server. [GNU Debugger (GDB)](https://www.sourceware.org/gdb/) and other debuginfo-consumer applications support Debuginfod (mostly) out of the box. For more information about it, please refer [to our Debuginfod guide](about-debuginfod.md).

You will only need to follow the methods outlined in this section if you are on Ubuntu Focal (20.04) or earlier.

## Getting `-dbgsym.ddeb` packages

If you are debugging without debuginfod, your first step will be to enable the `ddebs.ubuntu.com` repository as described in this section, which will provide access to the `-dbgsym` packages.

In the rare cases where the `-dbgsym` package is not available, you might need to install the `-dbg` package instead. The subsequent section (Manual install of debug packages) provides more information about this case.

### Import the signing key

Import the debug symbol archive [signing key](https://help.ubuntu.com/community/Repositories/Ubuntu#Authentication_Tab) from the Ubuntu server. On Ubuntu 18.04 LTS and newer, run the following command:

```bash
sudo apt install ubuntu-dbgsym-keyring
```

### Create a ddebs.list file

Create an `/etc/apt/sources.list.d/ddebs.list` by running the following line at a terminal:

```bash
echo "Types: deb
URIs: http://ddebs.ubuntu.com/
Suites: $(lsb_release -cs) $(lsb_release -cs)-updates $(lsb_release -cs)-proposed 
Components: main restricted universe multiverse
Signed-by: /usr/share/keyrings/ubuntu-dbgsym-keyring.gpg" | \
sudo tee -a /etc/apt/sources.list.d/ddebs.sources
```

You can also add these repositories in your software sources from the Ubuntu software center or from Synaptic (refer to [this article](https://help.ubuntu.com/community/Repositories/Ubuntu), especially the section on [adding other repositories](https://help.ubuntu.com/community/Repositories/Ubuntu#Adding_Other_Repositories)). You will need to add lines like:

```bash
deb http://ddebs.ubuntu.com focal main restricted universe multiverse
```

```{note}
Make sure you replace `focal` with the Ubuntu release name you're using.
```

### Update package list

Run the following to update your package list or click the Reload button if you used the Synaptic Package Manager:

```bash
sudo apt-get update
```

## Manual install of debug packages

To install the debug symbol package (`*-dbgsym.ddeb`) for a specific package, you can now invoke:

```bash
sudo apt-get install PACKAGE-dbgsym
```

For example, to install the debug symbols for `xserver-xorg-core`:

```bash
sudo apt-get install xserver-xorg-core-dbgsym
```

As mentioned in the section above, some packages will ship their debug symbols via `*-dbg.deb` packages instead. Using `glibc` as an example, you can install its debug symbols using:

```bash
sudo apt-get install libc6-dbg
```

This procedure will install the debug symbol package for a single package only. It is likely that the binary uses shared libraries in other packages, and their debug symbols may be needed in order to obtain a readable stack trace or perform other debugging tasks.

### The debian-goodies tool

You can use the `find-dbgsym-packages` command from the `debian-goodies` package to find debug symbols for a core file, running PID or binary path.

For a binary path it only finds debug symbols for the actual binary itself, and not any dynamically linked library dependencies or other libraries loaded at runtime. For that functionality to work you need to use either a core file or a running PID (which is the preferred method).

This tool will find both `-dbg` and `-dbgsym` style packages. However it only finds debug symbols for APT repositories that are currently enabled and updated, so you need to ensure that you enable at least the `ddebs.ubuntu.com` archive as described above. For a Launchpad PPA or the Ubuntu Cloud Archive you need to add another source line with the component changed from `main` to `main/debug`:

```bash
sudo apt install debian-goodies
find-dbgsym-packages [core_path|running_pid|binary_path]
```

## "debs" versus "ddebs"

It used to be the case that Debian/Ubuntu maintainers needed to manually create debug symbol packages as part of the packaging process, and included them in the same repository as their binary package. These debug symbol packages had the `-dbg.deb` suffix, so for example, both the `apache2-bin.deb` package and the `apache2-dbg.deb` package would be placed in the same repository. However, since the process is a manual one, not every maintainer did this, and the `.deb` package was not always kept up-to-date.

Modern package building tools automatically create the debug symbol packages when binary packages are compiled on Ubuntu servers, so the older (manual) process is no longer used. These automatically-created debug symbol packages have the `-dbgsym.ddeb` suffix. Unlike `-dbg.deb` packages, `-dbgsym.ddeb` packages are hosted in [their own separate repository](http://ddebs.ubuntu.com), since these packages are used relatively rarely.

You can choose to use either `-dbg.deb` or `-dbgsym.ddeb` packages, but for any given binary package only one debug symbol package can be used at once.
