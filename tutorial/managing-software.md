(managing-software)=
# Managing your software

If you are new to Ubuntu, you may be wondering what to do after installation. After all, Ubuntu is endlessly customizable according to your needs. There are two types of software found in Ubuntu: **Debian packages** and **snaps** -- we will learn about both!

To help you get the most from your Ubuntu experience, this tutorial will walk you through managing the software on your Ubuntu machine. This tutorial can be completed using either Ubuntu Server or Ubuntu Desktop.

To avoid making changes to your computer we will set up a virtual machine (VM), which will provide us with a safe environment to run the commands in. Multipass is great for quickly creating Ubuntu virtual machines, so we will use that.

## Prerequisites

* **Knowledge:**

  None! You don't even need to use an Ubuntu machine -- Multipass will give us an Ubuntu environment to play with.

* **Hardware:**

  The default Multipass VM will need **5** {term}`GB` **of disk space**, and **1 GiB of memory**.

* **Software: -- Multipass**

  * On Ubuntu, you can install Multipass by running the following command in your terminal (you can open a terminal window by pressing {kbd}`Ctrl` + {kbd}`Alt` + {kbd}`T` together):

    ```bash
    sudo snap install multipass
    ```
    
    Or you can install it directly from [the Multipass page](https://snapcraft.io/multipass) in the online snap store (make sure to select the "latest/stable" version from the dropdown menu next to the install button).

  * Multipass can be installed on Windows, Mac and other Linux distributions [using these instructions](https://multipass.run/docs/tutorial#install-multipass).

## Create the virtual machine

Once you have installed and run Multipass, it is straightforward to launch a new VM. Let us launch a VM using the Ubuntu 24.04 LTS release (codename `noble`), and let's give our VM the name `tutorial` using the following command in our terminal window:

```bash
multipass launch noble --name tutorial
```

Multipass will download the most recent daily **image** and create the VM for us. It may take a little time, depending on the speed of your internet connection.

An Ubuntu **image** is a collection of files we need to install and run Ubuntu. We don't need to specify "server" or "desktop" anywhere in our command, because the image is the same for both. The only difference between Ubuntu Server and Ubuntu Desktop is the subset of software packages we use from the Ubuntu Archive - we will see this later!

Now we can access the VM by running:

```bash
multipass shell tutorial
```

We will get a "Welcome to Ubuntu" message. Notice that when we run this command, the terminal username changes to `ubuntu` and the {term}`hostname` changes to `tutorial`:

```bash
ubuntu@tutorial
```

This shows that we are inside the VM, and this is where we will run all our commands.

## Updating the system with APT

The first thing we always want to do with a new system (whether a VM, container, bare metal, or cloud instance) is to make sure we have the latest versions of all the pre-installed software. 

Debian packages, commonly referred to as **debs**, are the standard software package format in Ubuntu. They can be identified by the `.deb` file extension. 

Every Linux distribution has their own preferred **package manager** for installing, updating and removing packages. In Ubuntu, the default package manager is [Advanced Packaging Tool](https://wiki.debian.org/AptCLI) (or APT, for short).

APT handles all of your system software (and other deb packages). It provides an interface to the Ubuntu Archive *repository*, so it can access both the **database** of all the packages available in Ubuntu, and the means to handle the **packages** themselves.

There are two APT commands we need to update our system: `update` and `upgrade`, which we will always run in that order.

### apt update

The `apt update` command is about the **database**. Any bug fixes in a package (or new versions since your last update) will be stored in the metadata about that package in the database (the **package index**).

When we run the `update` command it updates the APT database on our machine, fetching the newest available metadata from the package index:

```bash
sudo apt update
```

We will see an output like this:

```text
Hit:1 http://security.ubuntu.com/ubuntu noble-security InRelease
Hit:2 http://archive.ubuntu.com/ubuntu noble InRelease
Hit:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:4 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
88 packages can be upgraded. Run 'apt list --upgradable' to see them.
```

As we can see, it checks ("hits") the various archives (**pockets**) that updates can come from for the 24.04 LTS release (`noble-security`, `noble`, `noble-updates` and `noble-backports` -- remember these, as we'll come back to them later). It has found some packages that can be upgraded to newer versions. If we want to see which packages those are, we can run the command hinted in the output:

```bash
apt list --upgradable
```

The output tells us:

- the package name and where the update will come from (e.g. `base-files/noble-updates`),
- the most up-to-date package version available (e.g. `13ubuntu10.1`)
- the hardware version the update is for (e.g. `amd64`), and
- what package version is currently installed (e.g. `13ubuntu10`)

The specific packages included in this list changes over time, so the exact packages shown will be different, but the output will be structured like this:

```text
Listing... Done
base-files/noble-updates 13ubuntu10.1 amd64 [upgradable from: 13ubuntu10]
bsdextrautils/noble-updates 2.39.3-9ubuntu6.1 amd64 [upgradable from: 2.39.3-9ubuntu6]
bsdutils/noble-updates 1:2.39.3-9ubuntu6.1 amd64 [upgradable from: 1:2.39.3-9ubuntu6]
cloud-init/noble-updates 24.2-0ubuntu1~24.04.2 all [upgradable from: 24.1.3-0ubuntu3.3]
[...]
```

### apt upgrade

The `apt upgrade` command is about the **packages** on your system. It looks at the metadata in the package index we just updated, finds the packages with available upgrades, and lists them for us. Once we've checked the proposed upgrade and are happy to proceed, it will then install the newer versions for us.

After we have updated the database (which we did by running `apt update`) we can then upgrade the packages to their newest versions by running:

```bash
sudo apt upgrade
```

When we run this command, it will ask us to confirm if the summary of proposed changes that will be made to our system is what we want.

Let's type {kbd}`Y`, then press {kbd}`Enter` to confirm that yes, we do want that, and then the upgrade will proceed. This may take a few minutes.

```{tip}
You can use the `-y` flag, which is a shorthand for `--assume-yes`. If we ran the command `sudo apt upgrade -y` it would proceed with the upgrade without asking us to confirm. Shorthand versions of flags are common -- for most packages, you can check which flags are equivalent using [the manual pages](https://manpages.ubuntu.com/) or using the `man` command, as we'll see later.
```

In the output, we'll see where `apt upgrade` is fetching the upgrade from for each package. For example:

```text
Get:1 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libopeniscsiusr amd64 2.1.9-3ubuntu5.1 [49.1 kB]
```

APT combines the various elements; the package name (`libopeniscsiusr`), version (`2.1.9-3ubuntu5.1`), source (`noble-updates/main`), etc into a single URL that it can use for the download. The package is then unpacked, and the upgrade applied to the system.

```{note}
These commands only upgrade the packages for the release of Ubuntu that we are using (24.04 LTS). If we wanted to upgrade the entire system to the next release of Ubuntu (e.g. from 22.04 LTS to 24.04 LTS), we would use the `do-release-upgrade` command. See this guide on {ref}`how to upgrade your release <upgrade-your-release>` for more information.
```

It's important to know that `apt upgrade` will only handle packages that can be straightforwardly upgraded. If the package has **dependency** issues (i.e., the version you have "depends" on other packages that also need to be added, upgraded or removed), you would need to use `sudo apt dist-upgrade` instead. The `dist-upgrade` command is able to resolve conflicts between package versions, but it *could* end up removing some packages -- so although `apt upgrade` is safe to use unattended (in a script, for example), you should only use `dist-upgrade` when you can pay attention to it.

### Searching with APT

Now we're up-to-date, we can start exploring! As with any other database, we can search the list of available packages using APT in order to find software. Let's say that we want to find a webserver, for example. We can run the following command:

```bash
apt search webserver
```

This will return us a long list of all "webserver" packages it can find. But some of the descriptions don't actually contain the text "webserver" -- like in this section of the list:

```text
inotify-tools/noble 3.22.6.0-4 amd64
  command-line programs providing a simple interface to inotify

ipcalc/noble 0.51-1 all
  parameter calculator for IPv4 addresses

iwatch/noble 0.2.2-10 all
  realtime filesystem monitoring program using inotify
```

We can use `apt show` to inspect the description and summary details of any package, so let's take a closer look at `ipcalc` from our list:

```bash
apt show ipcalc
```

The summary has been replaced with `[...]` for brevity, but we can see that the text "webserver" is in the long description of the "Description" field.

```text
Package: ipcalc
Version: 0.51-1
[...]
APT-Sources: http://archive.ubuntu.com/ubuntu noble/universe amd64 Packages
Description: parameter calculator for IPv4 addresses
 ipcalc takes an IPv4 address and netmask and calculates the resulting
 broadcast, network, Cisco wildcard mask, and host range. By giving a
 second netmask, you can design sub- and supernetworks. It is also
 intended to be a teaching tool and presents the results as
 easy-to-understand binary values.
 .
 Originally, ipcalc was intended for use from the shell prompt, but a
 CGI wrapper is provided to enable colorful HTML display through a
 webserver.
 You can find it in /usr/share/doc/ipcalc/examples directory.
```

In many places, you will see reference to `apt-get` and `apt-cache` instead of `apt`. Historically, the *database* part of APT was accessed using `apt-cache` (e.g. `apt-cache show ipcalc`), and the *packages* part of APT used `apt-get` (e.g. `apt-get install ipcalc`).

APT has recently been streamlined, so although it uses `apt-get` and `apt-cache` "behind the scenes" (and these commands do still work), we don't need to worry about remembering which command to use -- we can use the more convenient `apt` directly. To find out more about these packages and how to use them (or indeed, any package in Ubuntu!) we can refer to the manual pages.

Run `man apt`, `man apt-get` or `man apt-cache` in the terminal to access the manuals for these packages on the command line, or view the same content in the [online manual pages](https://manpages.ubuntu.com).

## Installing deb packages

For the examples for this section, we're going to use the popular webserver package, [Apache2](https://httpd.apache.org/).

APT gives us a lot of details about what will be included in the installation, and it's always important to understand the implications of a command *before* we run it. We'll be taking a close look at the details APT gives us, so we need to be careful in this section.

When we run a command that asks us "`Do you want to continue? [Y/n]`", make sure to type {kbd}`N` for "no" and then press {kbd}`Enter` unless instructed otherwise -- this will let us see the output of the commands without making changes that then need to be undone.

Installing deb packages using APT is done using the `apt install` command. We can install either a single package, or a list of packages at once, by including their names in a space-separated list after the `install` command, in this format:

```text
sudo apt install <package 1> <package 2> <package 3>
```

### About `sudo`

We've seen the `sudo` prefix in a couple of commands already, and you may be wondering what that's about. In Linux, system tasks (like installing software) need elevated administrator permissions. These permissions are often called "root access", and a user with root access is called a "root user".

However, it can be dangerous to operate your machine as a root user -- since root access gives you full system control the whole time, it allows you to change or delete important system files. It's very easy to accidentally break your system in root mode!

Instead, we use `sudo` (which is short for `superuser do`). This command is a safety feature that grants regular users *temporary* (per command) admin privileges to make system changes. It's still important for us to always understand what a command does before we run it, but using `sudo` means we purposefully limit any potential mistakes to a single command.

### About dependencies

As we hinted earlier, packages often come with **dependencies** -- other packages that *your* package needs so it can function. Sometimes, a package might depend on a specific version of another package. If a package has dependencies, then installing a package via `apt` will also install any dependencies, which ensures the software can function properly.

APT tells us how it will resolve any dependency conflicts or issues when we run the `install` command. Let's try this for ourselves, but remember, we **don't** want to proceed with the install yet, so let's type {kbd}`N` when it asks us if we want to continue:

```bash
sudo apt install apache2
```

The output should be similar to the below. It tells us:

- which packages we have but don't need (we'll talk about that in the "autoremove" section),
- additional packages that will be installed (these are our dependencies),
- suggested packages (which we'll discuss in the next section), and
- a summary of which *new* packages will be present on the system after the install is done (which in this case is `apache2` itself, and all its dependencies).

```text
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
Suggested packages:
  apache2-doc apache2-suexec-pristine | apache2-suexec-custom www-browser
The following NEW packages will be installed:
  apache2 apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
0 upgraded, 10 newly installed, 0 to remove and 2 not upgraded.
Need to get 2084 kB of archives.
After this operation, 8094 kB of additional disk space will be used.
Do you want to continue? [Y/n] 
```

Let's try and make sense of this output. 

#### Types of dependencies

The relationship between a package and any other packages follows the [Debian policy on binary dependencies](https://www.debian.org/doc/debian-policy/ch-relationships.html#binary-dependencies-depends-recommends-suggests-enhances-pre-depends), which we'll briefly look at here. The most common ones you might come across are: `depends`, `recommends`, and `suggests` (although there are others!), so we'll take a look at these three.

- **depends**: Absolutely required, the package won't work without it. If we try to remove a package that is depended on by another, both will be removed! 
- **recommends**: Strongly dependent, but not absolutely necessary (which means the package will work better with it, but can still function without it)
- **suggests**: Not needed, but may enhance the usefulness of the package in some way.

We can see, using `apt show`, exactly which packages fall into each of these categories. Let's use Apache2 as our example again:

```bash
apt show apache2
```

If we look only at the sections on dependencies, we can see that `ssl-cert` is a recommended package:

```text
[...]
Provides: httpd, httpd-cgi
Pre-Depends: init-system-helpers (>= 1.54~)
Depends: apache2-bin (= 2.4.58-1ubuntu8.4), apache2-data (= 2.4.58-1ubuntu8.4), apache2-utils (= 2.4.58-1ubuntu8.4), media-types, perl:any, procps
Recommends: ssl-cert
Suggests: apache2-doc, apache2-suexec-pristine | apache2-suexec-custom, www-browser, ufw
[...]
```

In Ubuntu, the default configuration of `apt install` is set to install recommended packages alongside `depends`, so when we ran the `apt install apache2` command, `ssl-cert` was included in the proposed packages to be installed (even though it's only recommended, not strictly needed).

We can override this behavior by passing the `--no-install-recommends` flag to our command, like this:

```bash
sudo apt install apache2 --no-install-recommends
```

Then the output becomes the following (type {kbd}`N` at the prompt again to avoid installing for now):

```text
[...]
The following additional packages will be installed:
  apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0
Suggested packages:
  apache2-doc apache2-suexec-pristine | apache2-suexec-custom www-browser
Recommended packages:
  ssl-cert
The following NEW packages will be installed:
  apache2 apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0
0 upgraded, 9 newly installed, 0 to remove and 25 not upgraded.
[...]
```

Now, we see that `ssl-cert` is only mentioned as a recommended package, but is excluded from the list of packages to be installed.

There is a second flag we could pass -- the `--install-suggests` flag. This will not only install the strict dependencies and recommended packages, but *also* the suggested packages. From our previous output, it doesn't look like too much, right? It's only four additional packages.

But actually, if we run this command:

```bash
sudo apt install apache2 --install-suggests
```

There is now an extremely long list of suggested packages (which I will not output here, but you can try it for yourself!). In fact, the number of suggested packages is so long that there is not enough space in this VM to install them all, so it won't even give us the option to proceed:

```text
[...]
0 upgraded, 4598 newly installed, 2 to remove and 0 not upgraded.
Need to get 7415 MB of archives.
After this operation, 19.6 GB of additional disk space will be used.
E: You don't have enough free space in /var/cache/apt/archives/.
```

This is because each of these suggested packages also comes with their own lists of dependencies, including suggested packages, all of which would *also* be installed. It's perhaps clear to see why this is not the default setting!

#### What if we remove a dependency?

We'll go into more detail about removing packages later, but for now, let's see what happens if we remove a required *dependency*. First, we should (finally!) install the `apache2` package. Let's run the following command again, but this time when we are asked whether we want to continue, let's press {kbd}`Y` and then {kbd}`Enter` to confirm, and APT will install the package:

```bash
sudo apt install apache2
```

One of the required dependencies is the `apache2-data` package. Let's try to remove it using `apt remove`:

```bash
sudo apt remove apache2-data
```

Once again, `apt` won't proceed without confirmation, so we get the following output -- let's take a look before choose anything:

```text
[...]
The following packages were automatically installed and are no longer required:
  apache2-bin apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  apache2 apache2-data
0 upgraded, 0 newly installed, 2 to remove and 2 not upgraded.
After this operation, 1342 kB disk space will be freed.
Do you want to continue? [Y/n]
```

Let's break this down a little bit, because there are some subtle differences here that we want to understand before we proceed.

- "The following packages were automatically installed and are no longer required"

  These were other dependencies that `apache2` needed, but none of them depend upon `apache2-data`, so even if we remove `apache2` and `apache2-data` they would still be functional -- they just aren't used by any other installed packages...and so have no reason to be there anymore. They won't be removed, APT is helpfully telling us so we're aware of them.

- "The following packages will be REMOVED"

  These are the packages that will be removed directly - we've told APT we want to remove `apache2-data`, so we expect that to be included, but it will also remove `apache2` itself! This is because `apache2-data` is a required dependency, and `apache2` won't function *at all* without it.
  
Let's now choose {kbd}`Y` to confirm we want to remove this dependency.

```{warning}
Removing dependencies can, at worst, cause a system to become unusable -- you should always be careful when doing so. If you remove a dependency that is part of a chain, the removals will cascade up the chain as each dependency and the package that depends on it are removed. You can end up removing more than you originally anticipated!
```

#### Autoremove dependencies

So, we have removed the `apache2` and `apache2-data` packages, but the other dependencies that were installed alongside `apache2` are still there. The output of our `remove` command gave us the hint about how to deal with these redundant packages -- the `autoremove` command:

```bash
sudo apt autoremove
```

When we run this command, `apt` once again gives us a summary of the operation we requested, but let's choose {kbd}`N` for now when it asks if we want to continue:

```text
[...]
The following packages will be REMOVED:
  apache2-bin apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
0 upgraded, 0 newly installed, 8 to remove and 2 not upgraded.
After this operation, 6751 kB disk space will be freed.
Do you want to continue? [Y/n] 
```

You may be wondering why we don't need to specify any packages when we call the `autoremove` command -- after all, we've just been dealing with packages related to `apache2`. This is because `apt` will check all the packages on your system. It examines the dependency tree, and if the original reason for the package to be installed no longer exists (i.e., it isn't needed by anything), it will be flagged for autoremoval.

But!

We might, in the future, uninstall Apache2 without uninstalling the redundant packages at the time. We might have found another use for `ssl-cert`, perhaps in a script that makes use of SSL certificates. So how can we keep the `ssl-cert` package, even though it's flagged for autoremoval?

We can solve this problem, and un-flag the `ssl-cert` package for removal, by *manually* installing it:

```bash
sudo apt install ssl-cert
```

This sets `ssl-cert` to **manually installed**. We might well wonder "why didn't APT didn't ask us to confirm anything this time?". In this case, it's because `ssl-cert` is already present on the system so APT doesn't need to install anything new.

```text
[...]
ssl-cert is already the newest version (1.1.2ubuntu1).
ssl-cert set to manually installed.
The following packages were automatically installed and are no longer required:
  apache2-bin apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.
```

If the `ssl-cert` package is manually installed on our system, by us, then `apt` knows the package is wanted, and we can see that it has been removed from the autoremove list so our next autoremove will not uninstall it. Let's test this, just to make sure!

```bash
sudo apt autoremove
```

This time we'll select {kbd}`Y` when prompted, and then we can run `apt list ssl-cert` to quickly see if our `ssl-cert` package is still on the system:

```bash
apt list ssl-cert
```

Which gives us this output, confirming that `ssl-cert` is currently installed:

```text
Listing... Done
ssl-cert/noble,now 1.1.2ubuntu1 all [installed]
```

If you're curious, you can also run `apt list apache2` to see how the output differs for a package that was once installed and then removed!

Anyway, we're not quite finished with the Apache2 package, so let's reinstall it:

```bash
sudo apt install apache2
```

And this time select {kbd}`Y` to confirm when it asks.

## Customize configuration

In general, the default package configuration should just work well, and work "out of the box" when it's installed. But it's almost inevitable that, sooner or later, we'll want to customize the package so that it better fits our own purposes.

Before we try to customize the package, we should probably look at what files are included in it. We can check this using {manpage}`dpkg(1)`, which is the Debian package manager. Although APT is now more commonly used for basic package handling, `dpkg` retains some really helpful commands for examining files and finding out package information. It's installed by default on Ubuntu systems so we can use it directly:

```bash
dpkg --listfiles ssl-cert
```

This gives us the following list of files and their directory structure (the end of the list is truncated for brevity):

```text
/.
/etc
/etc/ssl
/etc/ssl/certs
/etc/ssl/private
/lib
diverted by base-files to: /lib.usr-is-merged
/lib/systemd
/lib/systemd/system
/lib/systemd/system/ssl-cert.service
/usr
/usr/sbin
/usr/sbin/make-ssl-cert
/usr/share
/usr/share/doc
/usr/share/doc/ssl-cert
/usr/share/doc/ssl-cert/README
[...]
```

If we find a file but we're not sure what package it comes from, `dpkg` can help us there too! Let's use the example of one of the files from the previous output: `/usr/share/ssl-cert/ssleay.cnf` and do a search for it using `dpkg`:

```bash
dpkg --search /usr/share/ssl-cert/ssleay.cnf
```

This will provide us with the package name for the given file:

```bash
ssl-cert: /usr/share/ssl-cert/ssleay.cnf
```

Although this seems obvious to us, because we already know the source of this file, the `dpkg` search function is really useful for tracking down the sources of files we don't know about!

### Conffiles

Most of a package's configuration is handled through [configuration files](https://www.debian.org/doc/debian-policy/ap-pkg-conffiles.html#automatic-handling-of-configuration-files-by-dpkg) (often known as **conffiles**). Conffiles often contain things like file paths, logs and debugging configuration, kernel parameters (which can be changed to optimize system performance), access control, and other configuration settings. The actual parameters available will vary from one package to another.

Package conffiles are different from all other files delivered in a package. A package may have any number of conffiles (including none!). Conffiles are explicitly marked by the package maintainer during development to protect local configuration from being overwritten during upgrades so that your changes are saved. This is not the case for any other types of files -- changes you make to regular files in that package *will be overwritten* during an upgrade. 

### How upgrades are handled

Since a conffile can be changed by us, we might end up with conflicts when the package maintainer changes those same files. Therefore, it's important to understand how such conflicts are handled.

We can show the four possible upgrade scenarios using the following table. What happens during an upgrade depends on whether the conffile on our system has been changed by us ("changed/not changed by user"), and whether the version's default content has been changed by the package maintainer ("changed/not changed by maintainer"):

| The conffile is...         | **not changed by maintainer** | **changed by maintainer** |
|----------------------------|-------------------------------|---------------------------|
| **...changed by user**     | Keep user's changes           | Ask user                  |
| **...not changed by user** | No changes to make            | Apply changes from update |

So we can see that if we do make changes to a conffile, APT will never overwrite our changes without asking us first. 

### Identifying conffiles

Out of the list of files in a package, how do we know which ones are the conffiles?

After all, they are not marked by any particular file extension, and although they are often found in the `/etc/` directory, they don't *have* to be there. As we saw before, the only thing conffiles have in common is that the package maintainer decided to mark them as such.

But that's our clue! So once more, `dpkg` can come to our rescue. The following command will show us (`--show`) the subset of files in the `apache2` package that have been marked as "`Conffiles`" (`-f='${Conffiles}\n'`) by the maintainer and shows each on a new line (`\n`) in the output:

```bash
dpkg-query --show -f='${Conffiles}\n' apache2
```

If you want to understand more about what this command does, you can refer to the manual page by typing `man dpkg-query --show`, and it will talk you through all the options.

Unlike `dpkg --listfiles`, `dpkg-query` *also* gives us a string of letters and numbers. This string is known as the **"MD5 checksum"** or **"MD5 hash"**. 

```text
 /etc/apache2/apache2.conf 354c9e6d2b88a0a3e0548f853840674c
 /etc/apache2/conf-available/charset.conf e6fbb8adf631932851d6cc522c1e48d7
 /etc/apache2/conf-available/security.conf 332668933023a463046fa90d9b057193
 /etc/apache2/envvars e4431a53c868ae0dfcde68564f3ce6a7
 /etc/apache2/magic a6d370833a02f53db6a0a30800704994
[...]
```

We can see the checksum of a specific file by running this command:

```bash
md5sum /etc/apache2/apache2.conf
```

Which returns us the checksum followed by the file and its location:

```bash
354c9e6d2b88a0a3e0548f853840674c  /etc/apache2/apache2.conf
```

You might well be wondering "why do we care about that?" since they match (in this example).

The checksum is like a fingerprint - it's unique for every *version* of a file, so any time the file is changed it will get a new checksum -- which allows us to see **if a file has been changed** from the default. 

### Verifying checksums

Let's set up a situation so we can poke a bit at this idea. We can start by making some changes to a conffile. In Apache2, the main conffile is `/etc/apache2/apache2.conf`, so let's use that. In a situation where we are setting up a new webserver, we might reasonably want to increase the `LogLevel` from "warn" to "debug" to get more debugging messages, so let's run this command and use `sed` to make that change in the conffile:

```bash
sudo sed -e 's/LogLevel warn/LogLevel debug/' -i /etc/apache2/apache2.conf
```

We won't be prompted to confirm if we want to make these changes -- but we do need root access so we use `sudo` in our command. As we hinted in the section about `sudo`, the fact that we can make these changes without needing to confirm is why it can be so easy to break your system when you're operating as root! Try running the command without the `sudo`, and you will get a "permission denied" error.

Next, we'll restart our Apache2 server so that we can activate our configuration changes:

```bash
sudo systemctl restart apache2
```

Now if we run the `md5sum` command again, we can see the hash changed:

```bash
ubuntu@tutorial:~$ md5sum /etc/apache2/apache2.conf

1109a77001754a836fb4a1378f740702  /etc/apache2/apache2.conf
```

This works great if we know that there's a file *we* changed, but what about if someone else tampered with a file, and we don't know which one? In that case, we can use:

```bash
dpkg --verify apache2
```

This will verify the checksums of the files on our system against those held in the package index for `apache2`, and return a rather strange looking result if (or when) it finds a mismatch:

```text
??5?????? c /etc/apache2/apache2.conf
```

Which is exactly what we were expecting to see, since we know we changed this file.

But what if something else was messed with...something that shouldn't be, and something not changed by us? Let's make a "silly" change to a different file to test this -- in this case, changing all instances of the word "warning" to "silly" in a random package file:

```bash
sudo sed -e 's/warning/silly/' -i /usr/sbin/a2enmod
```

And then run the verification again with:

```bash
dpkg --verify apache2
```

We now see something that looks like this:

```bash
??5?????? c /etc/apache2/apache2.conf
??5??????   /usr/sbin/a2enmod
```

```{note}
You might have noticed there's a "c" next to the top line but not the bottom -- the "c" shows the file is a conffile.
```

`dpkg` can tell that the file has been changed, but won't tell us what the change was. However, since the file in question is not a conffile, we know that the change *won't be preserved* if we upgrade the package. This means that we can overwrite the changes and restore the default package content by "reinstalling" Apache2:

```bash
sudo apt install --reinstall apache2
```

By using the `--reinstall` flag, we can force `apt` to re-unpack all of the default content. If we then verify once more...

```bash
dpkg --verify apache2
```

Then we'll get this output:

```text
??5?????? c /etc/apache2/apache2.conf
```

...so we can see that our change to the conffile has been preserved because the checksums are different, but the `a2enmod` file isn't listed anymore because it has been restored to the default. Phew!

```{note}
We can use `sudo apt install <package>` to upgrade an installed package, but this will only upgrade to the latest version. In our case, we were already on the latest version of Apache2, so we needed to force APT to re-unpack the content to overwrite our "silly" changes.
```

## Removing packages

Since we have just reinstalled the Apache2 package, we know it is in good shape. But what if we decide we're done with it and just want to remove it? Then we can run:

```bash
sudo apt remove apache2
```

Which will give us an output like this:

```text
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3
  libaprutil1-ldap libaprutil1t64 liblua5.4-0
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  apache2
0 upgraded, 0 newly installed, 1 to remove and 44 not upgraded.
After this operation, 465 kB disk space will be freed.
Do you want to continue? [Y/n] 
```

Let's type {kbd}`Y` to proceed. 

As before, we see that the dependencies will still be there even when `apache2` has been removed. Let's check with `dpkg`...

```bash
dpkg --listfiles apache2
```

...and see what else might be left behind...

```bash
/etc
/etc/apache2
/etc/apache2/apache2.conf
/etc/apache2/conf-available
/etc/apache2/conf-available/charset.conf
/etc/apache2/conf-available/localized-error-pages.conf
/etc/apache2/conf-available/other-vhosts-access-log.conf
/etc/apache2/conf-available/security.conf
/etc/apache2/conf-available/serve-cgi-bin.conf
/etc/apache2/conf-enabled
/etc/apache2/envvars
/etc/apache2/magic
/etc/apache2/mods-available
/etc/apache2/mods-available/access_compat.load
/etc/apache2/mods-available/actions.conf
[...]
```

This looks suspiciously like the list of conffiles we saw earlier, right?

### Also removing configuration

As it turns out, removing a package doesn't automatically remove the conffiles. But -- this is intentional, for our convenience.

By leaving the conffiles in place, if we decide to reinstall `apache2` again in the future, we don't need to spend time setting up all our configuration again.

Let's see the difference in installing `apache2` after it has been installed (and removed) compared to the first time we installed it:

```bash
sudo apt install apache2
```

Notice that it did not ask us to confirm if we wanted to proceed this time. Why not? As we saw earlier, the "Y/n" confirmation is shown when there are dependencies, and we know that Apache2 *has* dependencies.

...Ah! But this time, we didn't run `autoremove` when we uninstalled Apache2, so the dependencies are still installed on our system. This means that when we ask `apt` to install `apache2` now, there is nothing missing and we are getting *exactly* what we are asking for.

Since the dependencies and conffiles are still there, we can use our former config immediately. It even retains the changes we made before, which we can verify by looking at the checksum again:

```bash
md5sum /etc/apache2/apache2.conf
```

### Removing and purging

What if we decide that we don't want the changed conffiles? Perhaps we want to go back to the default installation, or we know we won't want to use the package ever again -- how can we ensure that all the conffiles are removed at the same time as we remove the package?

In that case, we can use the `--purge` option of the `remove` command:

```bash
sudo apt remove --purge apache2
```

Which will give us this output:

```bash
[...]
The following packages were automatically installed and are no longer required:
  apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3
  libaprutil1-ldap libaprutil1t64 liblua5.4-0
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  apache2*
0 upgraded, 0 newly installed, 1 to remove and 9 not upgraded.
After this operation, 465 kB disk space will be freed.
Do you want to continue? [Y/n] 
```

If we look very carefully, we see a little asterisk (\*) in the output.

```bash
The following packages will be REMOVED:
  apache2*
```

This tiny indicator tells us that the package will be removed AND purged. However, it still does not remove the dependencies (or the conffiles of those dependencies).

Let's type {kbd}`Y` again to confirm we want to proceed. Then, once the removal is complete, we can check the list once more:

```bash
dpkg --listfiles apache2
```

And this time, the output is very different!

```bash
dpkg-query: package 'apache2' is not installed
Use dpkg --contents (= dpkg-deb --contents) to list archive files contents.
```

```{note}
We could also use the `dpkg-query --show -f='${Conffiles}\n' apache2` command from earlier, and `dpkg-query` will find no packages matching `apache2`.
```

There are other ways to change package files. If you would like to read more, check out our {ref}`guide to changing package files <changing-package-files>`.

## What else is on our system?

As we saw earlier, we can search the APT package database for keywords using `apt search <keyword>` to find software we might want to install. We can also see all the packages we already have using `apt list`, although it can be easier to navigate and more informative if we use `dpkg -l` instead -- then we can use the up and down arrow keys on our keyboard to scroll (or press {kbd}`Q` to return to our terminal prompt).

For every package, we can see what versions of it exist in the database:

```bash
apt policy apache2
```

This will return a summary of all the versions that exist on our particular Ubuntu release, ordered by "most recent" first:

```text
apache2:
  Installed: (none)
  Candidate: 2.4.58-1ubuntu8.4
  Version table:
     2.4.58-1ubuntu8.4 500
        500 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages
        500 http://security.ubuntu.com/ubuntu noble-security/main amd64 Packages
        100 /var/lib/dpkg/status
     2.4.58-1ubuntu8 500
        500 http://archive.ubuntu.com/ubuntu noble/main amd64 Packages
```

We know that Apache2 isn't installed right now, because we removed and purged it, which is why the installed version shows as "none":

```text
Installed: (none)
```

If we were to install the default package, we would get this one:

```text
Candidate: 2.4.58-1ubuntu8.4
```

Under each version we are also shown the **source**. The newest version (`2.4.58-1ubuntu8.4`) comes from `noble-updates` (main) and `noble-security` (main). The *original* version (`2.4.58-1ubuntu8`) comes from `noble` (main). This tells us that this was the version released with the with 24.04 LTS (Noble Numbat).

### Installing older package versions

We can install specific older versions if we want to, for example, to satisfy dependency requirements of another package. We can do that by specifying the package name and version:

```bash
sudo apt install <package=version>
```

However, this can be tricky and often leads to conflicts in dependency versions as APT always wants to install the most recent version. We can see an example of this if we run the following command:

```bash
sudo apt install apache2=2.4.58-1ubuntu8
```

APT warns us that the version of apache2 we want to install depends on earlier versions of the dependencies, but it helpfully tells us which dependency versions we need to successfully install the package we want.

```text
[...]
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 apache2 : Depends: apache2-bin (= 2.4.58-1ubuntu8) but 2.4.58-1ubuntu8.4 is to be installed
           Depends: apache2-data (= 2.4.58-1ubuntu8) but 2.4.58-1ubuntu8.4 is to be installed
           Depends: apache2-utils (= 2.4.58-1ubuntu8) but 2.4.58-1ubuntu8.4 is to be installed
E: Unable to correct problems, you have held broken packages.
```

So, all we need to do is first install the dependencies, and then run the install command again. Remember that we can install multiple packages at once by separating them with spaces:

```bash
sudo apt install apache2-bin=2.4.58-1ubuntu8 \
  apache2-data=2.4.58-1ubuntu8 \
  apache2-utils=2.4.58-1ubuntu8 \
  apache2=2.4.58-1ubuntu8
```

In this case we're also breaking the command over multiple lines using backslashes (`\`) to make it easier to read, but it will still be run as a single command.

APT will warn us that we are downgrading the package, but let us press {kbd}`Y` to confirm (when prompted), and it will go ahead and downgrade us anyway. Let's run the following command again:

```bash
apt policy apache2
```

And we'll get confirmation that we're running on an older version:

```text
apache2:
  Installed: 2.4.58-1ubuntu8
  Candidate: 2.4.58-1ubuntu8.4
  Version table:
     2.4.58-1ubuntu8.4 500
        500 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages
        500 http://security.ubuntu.com/ubuntu noble-security/main amd64 Packages
 *** 2.4.58-1ubuntu8 500
        500 http://archive.ubuntu.com/ubuntu noble/main amd64 Packages
        100 /var/lib/dpkg/status
```

### Where do packages come from?

You may be wondering by now "where exactly do all these packages come from?". We've spotted a few sources very briefly throughout this tutorial, but haven't paid direct attention to them yet. Let's take a little time now to define what we mean by all these different sources that APT can pull packages from.

The source behind APT is the **Ubuntu Package Archive**. This Archive splits into many layers, each with its own terminology. The different terminology is quite confusing at first, but we've seen a few of the terms already. So if we take a look, layer-by-layer, we'll see not just what all the terms mean, but how they all fit together.

Let's have a quick overview with this diagram. The general flow is that the Archive splits into **Ubuntu series**. Each series is split up into **pockets**, and then each pocket contains four **components**. If we tried to show all of this on one diagram, it would be quite extensive, so let's take a look through a single path.

```{mermaid}
flowchart TD;
  A[Ubuntu Package Archive] --> B([Splits into Ubuntu **series**]);

  B --> C[e.g., mantic];
  B --> D[noble]; 
  B --> E[oracular, etc]; 

  D --> H([Series split into **pockets**]);

  H --> I[-release];
  H --> J[-proposed];
  H --> K[-updates];
  H --> L[-security];
  H --> M[-backports];

  K --> N([Splits into **components**]);

  N --> O[main];
  N --> P[universe];
  N --> Q[restricted];
  N --> R[multiverse];

  style C fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style D fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style E fill:#fff,stroke:#cfcfcf,stroke-width:2px;

  style I fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style J fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style K fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style L fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style M fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style O fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style P fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style Q fill:#fff,stroke:#cfcfcf,stroke-width:2px;
  style R fill:#fff,stroke:#cfcfcf,stroke-width:2px;
```

#### Series

The **series** is a set of packages that are released with a specific version of Ubuntu -- they're usually referred to by their codename (e.g., `mantic`, `noble` and `oracular` in our diagram). Each version of Ubuntu may have multiple releases (for example, an LTS will have an initial release when it launches (e.g. 24.04 LTS), and then "subsequent point releases" (e.g. 24.04.1 LTS) -- these are all part of the same series (`noble`).

In practice, people often use the term "Ubuntu release" and "Ubuntu series" interchangeably.

#### Pockets

Every Ubuntu series (`noble`, `jammy`, etc) is split into **pockets**, which are related to the software development/release lifecycle:

- **-release** contains the packages as they are at release time.
- **-proposed** contains package updates while they are being tested.
- Once an update is released, they come from either **-security** or **-updates** depending on whether they are a security-related update or not.
- And **-backports**, which contains packages that were not available at release time.

This is why earlier, we saw that some updates came from `noble-updates` or `noble-security`. These refer to updates and security updates from the noble series (respectively). Pockets are usually appended to the end of the series, and it's quite common to see the hyphen (`-`) included when referring to pockets. 

Remember -- the original version of the `apache2` package we saw came from `noble`. The `-release` pocket only includes the software that was part of the original LTS release, and so it takes the name of the Ubuntu series by default (i.e., the `-release` pocket is implied). 

#### Components

Each pocket is split into four **components**, depending on whether the packages they contain are *open source* or *closed source*, and whether they are officially supported by Canonical or are maintained by the Ubuntu Community:

|                          | Open source | Closed source |
|--------------------------|-------------|---------------|
| **Officially supported** | main        | restricted    |
| **Community supported**  | universe    | multiverse    |

- **main** contains the open-source packages that are officially supported by Canonical. These packages are either installed on every Ubuntu machine, or are very widely used for various types of systems and use-cases.
- **universe** holds all other open-source packages in Ubuntu, which are typically maintained by the Debian and Ubuntu communities, but may also include additional security coverage from Canonical under [Ubuntu Pro](https://ubuntu.com/pro), which is available free for personal use on up to five machines.
- **restricted** contains the packages that are officially supported by Canonical but are not available under a completely free license.
- **multiverse** contains community-maintained proprietary software -- these packages are completely unsupported by Canonical.

If you would like more information about the Ubuntu release process, how packages are produced, or to learn more about the sort of terminology you might come across, you may be interested in the [Ubuntu Packaging Guide](https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/), which is a great resource containing all this information (and much more!).

## Installing a .deb file

Although APT is the preferred way to install packages on your system, due to its ability to handle dependencies and keep software up-to-date, not every package is available in the APT repository -- especially if they are so old they are no longer maintained, or conversely, are the newest version still in development!

We can install .deb files that aren't in the APT repository using `dpkg` -- all we need is to download the .deb file, and we can run a command like this to install it:

```bash
sudo dpkg -i <file-name.deb>
```

But -- APT is helpful here too. Even if we get a .deb file that isn't from the Ubuntu Archive, we can still install it with APT so that if there are dependencies that can be resolved automatically from the Archive -- they will be!

```bash
sudo apt install ./file-name.deb
```

If we ever do want to install a .deb file, APT is definitely the most convenient way to do it. We may still need to handle *some* dependencies manually, but now we have the knowledge to be able to do that.

Luckily, most of the packages you will ever need are likely to be found through APT. If it's not, it's worth checking if the software is available as a **snap** instead.

(tutorial_snaps)=
## Snaps

Snaps are a newer, self-contained software format that were developed to be a more portable and easy-to-use alternative to debs. They come with all their dependencies pre-bundled so that there is no need for a package management tool to track dependencies, and they run inside sandboxed environments that limit their interactions with the rest of the system.

Instead of **versions** as we have them in debs, snaps use the concept of [channels](https://snapcraft.io/docs/channels) to define which release of a snap is installed.

By default, snaps are kept automatically up-to-date, so we don't need to remember to update and upgrade them. There are times on a live system, such as a server in a production environment, where we might not want to have updates automatically applied. In those cases, we can [turn off automatic updates](https://snapcraft.io/docs/managing-updates) and refresh the system snaps when it's convenient (for example, during a maintenance window).

If you would like to try out snaps, we recommend the excellent [quickstart tour](https://snapcraft.io/docs/quickstart-tour) tutorial in the snap documentation. Feel free to continue using the VM we've been using in this tutorial while exploring!

## Completion!

Once you are finished and want to leave the tutorial, you can run:

```bash
exit
```

This will take you out of the VM and back to your live machine. Then, you can run the following commands to delete the VM and remove it completely from your machine:

```bash
multipass delete tutorial
multipass purge
```

## Summary

Congratulations, we made it to the end! We've covered a lot of material in this tutorial, so let's do a quick recap of what we've learned:

**Finding, installing and removing packages**

* How to update and upgrade all our system's software with APT:
  * `sudo apt update && sudo apt upgrade`

* How to search for software using keywords or strings:
  * `apt search <keyword>` or `apt search "some content string"` 

* How to see the description of a package, including what dependencies it has:
  * `apt show <package name>`
  
  Or how to check what package versions are available:
  * `apt policy <package>`

* How to install packages...
  * `sudo apt install <package1> <package2>`

* How to see all the files a package contains
  * `dpkg --listfiles <package>`

* How to find out what package a file belongs to:
  * `dpkg --search <path/to/file>`

* ...And how to remove packages again! As well as the difference between removing and purging.
  * `sudo apt remove <package>`

* We even learned how to downgrade to older versions of APT packages, and all about APT sources.

**Customizing package configuration**

* How to find the conffiles in a package:
  * `dpkg-query --show -f='${Conffiles}\n' <package>`

* How to see if package files have been changed:
  * `dpkg --verify <package>`

* ...And if a non-conffile has been changed by accident, we can fix it with:
  * `sudo apt install --reinstall <package>`

* We know that our changes to conffiles are always safely preserved, while changes to non-conffiles are reverted at the next upgrade or security fix.

* Importantly, we know how to verify checksums with `md5sum` or similar tools, which helps us to more safely build packages from source.

* And finally, we learned about snaps!
