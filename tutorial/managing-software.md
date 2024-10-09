(managing-software)=
# Managing your software

If you are new to Ubuntu, you may be wondering what to do after installation.
After all, Ubuntu is endlessly customisable according to your needs.

To help you get the most from your Ubuntu experience, this tutorial will walk
you through managing the software on your Ubuntu machine. Although we'll be
using Ubuntu Server as our example, this tutorial is equally applicable to the
Ubuntu Desktop.

There are two types of software found in Ubuntu: **Debian packages** and
**snaps** -- we will learn about both!

## Create the virtual machine

To avoid making changes to your computer we will set up a virtual machine (VM)
to launch our server and run the commands.

Multipass is great for quickly creating Ubuntu virtual machines, so we will use
that. On Ubuntu, you can install Multipass by running the following command in
your terminal:

```bash
sudo snap install multipass
```

Multipass can also be installed on Windows, Mac and other Linux distributions
[using these instructions](https://multipass.run/docs/tutorial#install-multipass).

Once you have installed Multipass, it is straightforward to launch a new VM.
Let us launch our VM using the 24.04 LTS release (`noble`), and let's also give
it the name `tutorial` using the following command. The default VM created with
this command will need **5 GiB of disk space**, and **1 GiB of memory**:

```bash
multipass launch noble --name tutorial
```

Multipass will download the most recent daily **image** and create the VM for
us. It may take a little time, depending on the speed of your internet
connection.

The **image** is the collection of files we need to install and run Ubuntu. We
don't need to specify "server" or "desktop" anywhere in our command, because
the image is the same for both. The only difference between Ubuntu Server and
Ubuntu Desktop is the subset of software packages we use from the image - we
will see this later!

Now we can access the VM by running:

```bash
multipass shell tutorial
```

We will get a "Welcome to Ubuntu 24.04 LTS" message. Notice that when we run
this command, the terminal username changes to `ubuntu` and the hostname
changes to `tutorial`:

```bash
ubuntu@tutorial
```

This shows that we are inside the VM, where we will run all of our commands. 

## Updating the system with APT

The first thing we always want to do with a new system (whether a VM or a
"live" machine) is to run an update to make sure we have the latest versions
of all the default software. 

Debian packages, commonly referred to as **"debs"** are the standard software
in Ubuntu. They can be identified by the `.deb` file extension and usually come
in a pre-compiled binary format (so you don't need to compile it yourself).

Your system software (and other deb packages) are handled through the
[Advanced Packaging Tool](https://ubuntu.com/server/docs/package-management#advanced-packaging-tool)
(APT). APT is a package *repository*; it contains both the **database** of the
packages available in Ubuntu, and it contains the **packages** themselves.

There are two commands we need for updating our system: `update` and `upgrade`,
which we will always run in that order.

### apt update

The `apt update` command is about the **database**. Any bug fixes in a package
(or new versions since your last update) will be stored in the metadata about
that package in the database (the **package index**).

When we run the `update` command it updates the APT database on our machine,
fetching the newest available metadata from the package index:

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

As we can see, it checks ("hits") the various archives (**pockets**) that
updates can come from for the 24.04 LTS release (`noble-security`, `noble`,
`noble-updates` and `noble-backports` -- remember these, as we'll come back to
them later). It has found some packages that can be upgraded to newer versions.
If we want to see which packages those are, we can run the command hinted in
the output:

```bash
apt list --upgradable
```

The output tells us:
- the package name and where the update will come from
  (e.g. `base-files/noble-updates`),
- the most up-to-date package version available (e.g. `13ubuntu10.1`)
- the hardware version the update is for (e.g. `amd64`), and
- what package version is currently installed (e.g. `13ubuntu10`)

The specific packages included in this list will change over time, but the
output will be structured like this:

```text
Listing... Done
base-files/noble-updates 13ubuntu10.1 amd64 [upgradable from: 13ubuntu10]
bsdextrautils/noble-updates 2.39.3-9ubuntu6.1 amd64 [upgradable from: 2.39.3-9ubuntu6]
bsdutils/noble-updates 1:2.39.3-9ubuntu6.1 amd64 [upgradable from: 1:2.39.3-9ubuntu6]
cloud-init/noble-updates 24.2-0ubuntu1~24.04.2 all [upgradable from: 24.1.3-0ubuntu3.3]
[...]
```

### apt upgrade

The `apt upgrade` command is about the **packages** on your system. After we
have updated the database by running `apt update` we can upgrade the packages
to their newest versions by running:

```bash
sudo apt upgrade
```

The `upgrade` command looks at the metadata in the package index we just
updated, finds the packages with available upgrades, and lists them for us. It
also asks us to confirm if we want to do the upgrade. Let's type <kbd>Y</kbd>
to confirm that we want to, and the upgrade will proceed. This may take a few
minutes.

```{tip}
You can use the `-y` flag, which is a shorthand for `--assume-yes`. If we ran
the command `sudo apt upgrade -y` it would proceed with the upgrade without
asking us to confirm. Shorthand versions of flags are common -- for most
packages, you can check which flags are equivalent using
[the manual pages](https://manpages.ubuntu.com/). 
```

In the output, we'll see where `apt upgrade` is fetching the upgrade from for
each package. For example:

```text
Get:1 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libopeniscsiusr amd64 2.1.9-3ubuntu5.1 [49.1 kB]
```

APT combines the various elements; the package name (`libopeniscsiusr`),
version (`2.1.9-3ubuntu5.1`), source (`noble-updates/main`), etc into a single
URL that it can use for the download. It then unpacks the package and applies
the upgrade to the system.

```{note}
These commands only upgrade the packages for the release of Ubuntu that we are
using (24.04 LTS). If we wanted to upgrade to the next release of Ubuntu, we
would use the `do-release-upgrade` command. See this guide on
{ref}`how to upgrade your release <upgrade-your-release>` for more information.
```

It's important to know that `apt upgrade` will only handle packages that can be
straightforwardly upgraded. If the package has **dependency** issues (i.e., the
version you have "depends" on other packages that also need to be added,
upgraded or removed), you would need to use `sudo apt dist-upgrade` instead.
The `dist-upgrade` command is able to resolve conflicts between package
versions, but it *could* end up removing some packages -- so although
`apt upgrade` is safe to use unattended (in a script, for example), you should
only use `dist-upgrade` when you can pay attention to it.

### Searching APT

Now we're up-to-date, we can start exploring! As with any other database, we
can search APT to find software. Let's say that we want to find a webserver,
for example. We can run the following command:

```bash
apt search webserver
```

This will return us a long list of all "webserver" packages it can find. But
some of the descriptions don't actually contain the text "webserver" -- like in
this section of the list:

```text
inotify-tools/noble 3.22.6.0-4 amd64
  command-line programs providing a simple interface to inotify

ipcalc/noble 0.51-1 all
  parameter calculator for IPv4 addresses

iwatch/noble 0.2.2-10 all
  realtime filesystem monitoring program using inotify
```

We can use `apt show` to inspect the description and summary details of any
package, so let's take a closer look at `ipcalc` from our list:

```bash
apt show ipcalc
```

The summary has been replaced with `[...]` for brevity, but we can see that the
text "webserver" is in the long description of the "Description" field.

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

In many places, you will see reference to `apt-get` and `apt-cache` instead of
`apt`. Historically, the *database* part of APT was accessed using `apt-cache`
(e.g. `apt-cache show ipcalc`), and the *packages* part of APT used `apt-get`
(e.g. `apt-get install ipcalc`).

APT has recently been streamlined, so although it uses `apt-get` and
`apt-cache` "behind the scenes", you don't need to worry about remembering
which command to use -- you can use `apt` directly. To find out more,
refer to the manual pages for these commands. Type `man apt`, `man apt-get` or
`man apt-cache` in your terminal to access them.

## Installing deb packages

For the following examples, we're going to use two popular webserver packages:
Apache2 and nginx. However, we won't install anything just yet -- let's just
take a look at the commands involved to understand what's happening.

Installing deb packages using APT is done using the `apt install` command. We
can install a single package:

```bash
sudo apt install apache2
```

Or multiple packages at once, by including them in a space-separated list like
this:

```bash
sudo apt install apache2 nginx
```

### Dependencies

As we hinted earlier, packages often come with **dependencies** -- other
packages that *your* package needs so it can function. Sometimes, a package
might depend on a specific version of another package. If a package has
dependencies, then installing a package via `apt` will also install any
dependencies, which ensures the software can function properly.

We can see what dependencies a package has using the `install` command. Let's
run the following command, but we don't want to proceed yet, so let's type
<kbd>n</kbd> when it prompts us:

```bash
sudo apt install apache2
```

The output below tells us:
- which packages we have but don't need (we'll talk about that in the
  "autoremove" section),
- additional packages that will be installed (these are our dependencies),
- suggested packages (which we'll discuss in the next section), and
- a summary of which *new* packages will be present on the system after the
  install is done (which in this case is `apache2` itself, and all its
  dependencies).

```text
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  linux-headers-6.8.0-39 linux-headers-6.8.0-39-generic linux-image-6.8.0-39-generic linux-modules-6.8.0-39-generic linux-tools-6.8.0-39
  linux-tools-6.8.0-39-generic
Use 'sudo apt autoremove' to remove them.
The following additional packages will be installed:
  apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
Suggested packages:
  apache2-doc apache2-suexec-pristine | apache2-suexec-custom www-browser
The following NEW packages will be installed:
  apache2 apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
0 upgraded, 10 newly installed, 0 to remove and 0 not upgraded.
Need to get 2083 kB of archives.
After this operation, 8094 kB of additional disk space will be used.
Do you want to continue? [Y/n] 
```

Let's try and make sense of this output. 

#### Types of dependencies

The relationship between a package and any other packages follows the
[Debian policy on binary dependencies](https://www.debian.org/doc/debian-policy/ch-relationships.html#binary-dependencies-depends-recommends-suggests-enhances-pre-depends),
which we'll briefly look at here. The most common ones you might come
across are: `depends`, `recommends`, and `suggests`(although there are
others!), so we'll take a look at these three.

- **depends**: Absolutely required, the package won't work without it.
- **recommends**: Strongly dependent, but not absolutely necessary (which means
  the package will work better with it, but can still function without it)
- **suggests**: Not needed, but may enhance the usefulness of the package in
  some way.

We can see, using `apt show`, exactly which packages fall into each of these
categories. Let's use Apache2 as our example again:

```bash
apt show apache2
```

If we look only at the sections on dependencies, we can see that `ssl-cert` is
a recommended package:

```text
Package: apache2
Version: 2.4.58-1ubuntu8.4
[...]
Provides: httpd, httpd-cgi
Pre-Depends: init-system-helpers (>= 1.54~)
Depends: apache2-bin (= 2.4.58-1ubuntu8.4), apache2-data (= 2.4.58-1ubuntu8.4), apache2-utils (= 2.4.58-1ubuntu8.4), media-types, perl:any, procps
Recommends: ssl-cert
Suggests: apache2-doc, apache2-suexec-pristine | apache2-suexec-custom, www-browser, ufw
[...]
```

In Ubuntu, the default configuration of `apt install` is set to install
recommended packages alongside `depends`, so when we ran the
`apt install apache2` command, `ssl-cert` was included in the packages
to be installed (even though it's only recommended, and not strictly needed).

We can override this behaviour by passing the `--no-install-recommends` flag to
our command, like this:

```bash
sudo apt install apache2 --no-install-recommends
```

Then the output becomes the following (let's type <kbd>n</kbd> at the prompt
again to avoid installing for now):

```text
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0
Suggested packages:
  apache2-doc apache2-suexec-pristine | apache2-suexec-custom www-browser
Recommended packages:
  ssl-cert
The following NEW packages will be installed:
  apache2 apache2-bin apache2-data apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0
0 upgraded, 9 newly installed, 0 to remove and 25 not upgraded.
Need to get 2065 kB of archives.
After this operation, 8026 kB of additional disk space will be used.
```

Now, we see that `ssl-cert` is only mentioned as a recommended package, but is
excluded from the list of packages to be installed.

There is a second flag we could pass -- the `--install-suggests` flag. This
will not only install the strict dependencies and recommended packages, but
*also* the suggested packages. From our previous output, it doesn't look like
too much, right? It's only four additional packages.

But actually, if we run this command:

```bash
sudo apt install apache2 --install-suggests
```

There is now an extremely long list of suggested packages (which I will not
output here, but you can try it for yourself!). In fact, the number of
suggested packages is so long that there is not enough space in this VM to
install them all, so it won't even give us the option to proceed:

```text
[...]
0 upgraded, 4598 newly installed, 2 to remove and 0 not upgraded.
Need to get 7415 MB of archives.
After this operation, 19.6 GB of additional disk space will be used.
E: You don't have enough free space in /var/cache/apt/archives/.
```

This is because each of these suggested packages also comes with their own
lists of dependencies, including suggested, all of which would also be
installed. It's perhaps clear to see why this is not the default setting!

#### What if we remove a dependency?

We'll go into more detail about removing packages later, but for now, let's see
what happens if we remove a required dependency. First, we should (finally!)
install the `apache2` package:

```bash
sudo apt install apache2
```

Now when we are prompted whether we want to continue, let's press <kbd>Y</kbd>
to install the package.

One of the required dependencies is the `apache2-data` package. Let's try to
remove it using `apt remove`:

```bash
sudo apt remove apache2-data
```

Once again, `apt` won't proceed without confirmation, so we get the following
output:

```text
[...]
The following packages were automatically installed and are no longer required:
  apache2-bin apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  apache2 apache2-data
0 upgraded, 0 newly installed, 2 to remove and 25 not upgraded.
After this operation, 1342 kB disk space will be freed.
Do you want to continue? [Y/n]
```

Let's break this down a little bit, because there are some subtle differences
here that we want to understand before we proceed.

- "The following packages were automatically installed and are no longer
  required"

  These were other dependencies that `apache2` needed, but none of them depend
  upon `apache2-data`, so even if we remove `apache2` and `apache2-data` they
  would still be functional -- they just aren't used by any other installed
  packages...and so have no reason to be there anymore.

- "The following packages will be REMOVED"

  These are the packages that will be removed directly - we've told `apt` we
  want to remove `apache2-data`, so that's included, but it also will remove
  `apache2` itself! This is because `apache2-data` is a required dependency,
  and `apache2` won't function *at all* without it.

Let's now choose <kbd>Y</kbd> to confirm we want to remove this dependency.

#### Autoremove dependencies

So, we have removed the `apache2` and `apache2-data` packages, but the other
dependencies that were installed alongside `apache2` are still there. The
output of our `remove` command gave us the hint about how to deal with these
redundant packages -- the `autoremove` command:

```bash
sudo apt autoremove
```

Once again, `apt` gives us a summary of the operation we requested, but let's
choose <kbd>n</kbd> for now:

```text
[...]
The following packages will be REMOVED:
  apache2-bin apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0 ssl-cert
0 upgraded, 0 newly installed, 8 to remove and 6 not upgraded.
After this operation, 6751 kB disk space will be freed.
Do you want to continue? [Y/n] 
```

You may be wondering why we don't need to specify any packages when we call the
`autoremove` command -- after all, we've just been dealing with packages
related to `apache2`. This is because `apt` will check all the packages on your
system. It examines the dependency tree, and if the original reason for the
package to be installed no longer exists (i.e., it isn't needed by anything),
it will be flagged for autoremoval.

But!

We might, in the future, uninstall Apache2 without uninstalling the redundant
packages at the time. We might have found another use for `ssl-cert`, perhaps
in a script that makes use of SSL certificates. So how can we keep the
`ssl-cert` package, even though it's flagged for autoremoval?

We can solve this problem, and un-flag the `ssl-cert` package for removal, by
*manually* installing it:

```bash
sudo apt install ssl-cert
```

This sets `ssl-cert` to **manually installed**.

```text
[...]
ssl-cert is already the newest version (1.1.2ubuntu1).
ssl-cert set to manually installed.
The following packages were automatically installed and are no longer required:
  apache2-bin apache2-utils libapr1t64 libaprutil1-dbd-sqlite3 libaprutil1-ldap libaprutil1t64 liblua5.4-0
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 6 not upgraded.
```

If the `ssl-cert` package is manually installed on our system, by us, then
`apt` knows the package is wanted, and we can see that it has been removed
from the autoremove list so our next autoremove will not uninstall it. Let's
test this, just to make sure!

```bash
sudo apt autoremove
```

Select <kbd>Y</kbd> when prompted this time, and then we can run
`apt list ssl-cert` to quickly see if our `ssl-cert` package is still on the
system:

```bash
ubuntu@tutorial:~$ apt list ssl-cert
Listing... Done
ssl-cert/noble,now 1.1.2ubuntu1 all [installed]
```

If you're curious, you can also run `apt list apache2` to see how the output
differs for a package that was once installed and then removed!

## Customise configuration

In general, the default package configuration should just work well, and work
"out of the box" when it's installed. But it's almost inevitable that, sooner
or later, we'll want to customise the package so that it better fits our own
purposes.

Before we try to customise the package, we should probably look at what files
are included in it. We can check this using `dpkg`, which is the
[Debian package manager](https://manpages.ubuntu.com/manpages/en/man1/dpkg.1.html).
Although APT is now more commonly used for basic package handling, `dpkg`
retains some really helpful commands for examining files and finding out
package information. It's installed by default on Ubuntu systems so we can use
it directly:

```bash
dpkg --listfiles ssl-cert
```

This gives us the following list of files and their directory structure:

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
/usr/share/doc/ssl-cert/changelog.gz
/usr/share/doc/ssl-cert/copyright
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/ssl-cert
[...]
```

If we find a file but we're not sure what package it comes from, `dpkg` can
help us there too! Let's use the example of one of the files from the previous
output: `/usr/share/ssl-cert/ssleay.cnf` and do a search for it using `dpkg`:

```bash
dpkg --search /usr/share/ssl-cert/ssleay.cnf
```

This will provide us with the package name for the given file:

```bash
ssl-cert: /usr/share/ssl-cert/ssleay.cnf
```

### Conffiles

Most of a package's configuration is handled through
[configuration files](https://www.debian.org/doc/debian-policy/ap-pkg-conffiles.html#automatic-handling-of-configuration-files-by-dpkg)
(often known as **conffiles**).

Package conffiles are different from all other files delivered in a package.
A package may have any number of conffiles (including none!). Conffiles are
explicitly marked by the package maintainer during development to protect them
from being automatically upgraded, whilst all other types of files are not --
any changes you make to regular files *will be overwritten* during an upgrade. 

### How upgrades are handled

Since a conffile can be changed by us, we might end up with conflicts when the
package maintainer changes those same files. Therefore, it's important to
understand how such conflicts are handled.

We can show the four possible upgrade scenarios using the following table. What
happens during an upgrade depends on whether the conffile on our system has
been changed by us ("changed/not changed by user"), and whether the default
content has been changed by the package maintainer ("same as/changed from
default"):

| The conffile is...          | **same as default**  | **changed from default**  |
| ---                         | ---                  | ---                       |
| **...changed by user**      | Keep user's changes  | Ask user                  |
| **...not changed by user**  | No changes to make   | Apply changes from update |

### Identifying conffiles

Out of the list of files in a package, how do we know which ones are the
conffiles?

After all, they are not marked by any particular file extension, and
although they are often found in the `/etc/` directory, they don't *have* to be
there. As we saw before, the only thing conffiles have in common is that the
package maintainer decided to mark them as such.

But that's our clue! So once more, `dpkg` can come to our rescue. The
following command will show us the subset of files in a package that have been
marked as "conffiles" by the maintainer:

```bash
dpkg-query --show -f='${Conffiles}\n' apache2
```

Unlike `dpkg --listfiles`, this query *also* gives us a string of letters and
numbers. This string is known as the **"MD5 checksum"** or **"MD5 hash"**. 

```text
 /etc/apache2/apache2.conf 354c9e6d2b88a0a3e0548f853840674c
 /etc/apache2/conf-available/charset.conf e6fbb8adf631932851d6cc522c1e48d7
 /etc/apache2/conf-available/security.conf 332668933023a463046fa90d9b057193
 /etc/apache2/envvars e4431a53c868ae0dfcde68564f3ce6a7
 /etc/apache2/magic a6d370833a02f53db6a0a30800704994
[...]
```

We see the checksum of a specific file by running this command:

```bash
md5sum /etc/apache2/apache2.conf
```

Which returns us the checksum followed by the file:

```bash
354c9e6d2b88a0a3e0548f853840674c  /etc/apache2/apache2.conf
```

You might well be wondering "why do we care about that?" since they match (in
this example).

The checksum is like a fingerprint - it's unique for every *version* of a file,
so any time the file is changed it will get a new checksum -- which allows us
to see **if a file has been changed** from the default. 

### Verifying checksums

Let's set up a situation so we can poke a bit at this idea. We can start by
making some changes to a conffile. In Apache2, the main conffile is
`/etc/apache2/apache2.conf`, so let's use that. In a situation where we are
setting up a new webserver, we might reasonably want to increase the `LogLevel`
from "warn" to "debug" to get more debugging messages, so let's run this
command and use `sed` to make that change in the conffile:

```bash
sudo sed -e 's/LogLevel warn/LogLevel debug/' -i /etc/apache2/apache2.conf
```

Then, we'll restart our Apache2 server so that we can activate our configuration
changes:

```bash
sudo systemctl restart apache2
```

Now if we run the `md5sum` command again, we can see the hash changed:

```bash
ubuntu@tutorial:~$ md5sum /etc/apache2/apache2.conf

1109a77001754a836fb4a1378f740702  /etc/apache2/apache2.conf
```

This works great if we know that there's a file *we* changed, but what about if
someone else tampered with a file, and we don't know which one? In that case,
we can use:

```bash
dpkg --verify apache2
```

This will verify the checksums of the files on our system against those held in
the package index for `apache2`, and return a rather strange looking result
if (or when) it finds a mismatch:

```text
??5?????? c /etc/apache2/apache2.conf
```

Which is exactly what we were expecting to see, since we know we changed this
file.

But what if something else was messed with...something that shouldn't be, and
something not changed by us? Let's make a "silly" change to a different file to
test this -- in this case, changing all instances of the word "warning" to
"silly" in a random package file:

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
You might have noticed there's a "c" next to the top line but not the
bottom -- the "c" shows the file is a conffile.
```

`dpkg` can tell that the file has been changed, but won't tell us what the
change was. However, since the file in question is not a conffile, we know that
the change *won't be preserved* if we upgrade the package. This means that we
can overwrite the changes and restore the default package content by
"reinstalling" Apache2:

```bash
sudo apt install --reinstall apache2
```

By using the `--reinstall` flag, we can force `apt` to re-unpack all of the
default content. If we then verify once more...

```bash
dpkg --verify apache2
```

...we can see that our change to the conffile has been preserved because
`dpkg` the checksums are different, but the `a2enmod` file isn't
listed anymore because it has been restored to the default. Phew!

```{note}
We can use `sudo apt install <package>` to upgrade an installed package, but
this will only upgrade to the latest version. In our case, we were already on
the latest version of Apache2, so we needed to force APT to re-unpack the
content to overwrite our "silly" changes.
```

## Removing packages

Since we have just reinstalled the Apache2 package, we know it is in good
shape. But what if we decide we're done with it and just want to remove it? 
Then we can run:

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

Let's type <kbd>Y</kbd> to proceed. 

As before, we see that the dependencies will still be there even when `apache2`
has been removed. Let's check with `dpkg`...

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

As it turns out, removing a package doesn't automatically remove the conffiles.
But -- this is intentional, for our convenience.

By leaving the conffiles in place, if we decide to reinstall `apache2` again
in the future, we don't need to spend time setting up all our configuration
again.

Let's see the difference in installing `apache2` after it has been installed
(and removed) compared to the first time we installed it:

```bash
sudo apt install apache2
```

Notice that it did not ask us to confirm if we wanted to proceed this time.
Why not? As we saw earlier, the "Y/n" confirmation is shown when there are
dependencies, and we know that Apache2 *has* dependencies.

...Ah! But this time, we didn't run `autoremove` when we uninstalled Apache2,
so the dependencies are still installed on our system. This means that when we
ask `apt` to install `apache2` now, there is nothing missing and we are getting
*exactly* what we are asking for.

Since the dependencies and conffiles are still there, we can use our former
config immediately. It even retains the changes we made before, which we can
verify by looking at the checksum again:

```bash
md5sum /etc/apache2/apache2.conf
```

### Removing and purging

What if we decide that we don't want the changed conffiles? Perhaps we want
to go back to the default installation, or we know we won't want to use the
package ever again -- how can we ensure that all the conffiles are removed at
the same time as we remove the package?

In that case, we can use the `--purge` flag with the `remove` command:

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

If we look very carefully, we see a little asterisk in the output.

```bash
The following packages will be REMOVED:
  apache2*
```

This tiny indicator tells us that the package will be removed AND purged.
However, it still does not remove the dependencies (or the conffiles
of those dependencies).

Let's type <kbd>Y</kbd> again to confirm we want to proceed. Then, once the
removal is complete, we can check the list once more:

```bash
dpkg --listfiles apache2
```

And this time, the output is very different!

```bash
dpkg-query: package 'apache2' is not installed
Use dpkg --contents (= dpkg-deb --contents) to list archive files contents.
```

```{note}
We could also use the `dpkg-query --show -f='${Conffiles}\n' apache2` command
from earlier, and `dpkg-query` will find no packages matching `apache2`.
```

There are other ways to change package files. If you would like to read more,
check out our
{ref}`guide to changing package files <changing-package-files>`.

## What else is on our system?

As we saw earlier, we can search the APT package database for keywords using
`apt search <keyword>` to find software we might want to install. We can also
see all the packages we already have using `apt list`, although it can be
easier to navigate and more informative if we use `dpkg -l` instead -- then we
can use the up and down arrow keys on our keyboard to scroll (or press
<kbd>Q</kbd> to return to our terminal prompt).

For every package, we can see what versions of it exist in the database:

```bash
apt policy apache2
```

This will return a summary of all the versions that exist on our particular
Ubuntu release, ordered by "most recent" first:

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

We know that Apache2 isn't installed right now, because we removed and purged
it, which is why the installed version shows as "none":

```text
Installed: (none)
```

If we were to install the default package, we would get this one:

```text
Candidate: 2.4.58-1ubuntu8.4
```

Under each version we are also shown the **source**. The newest version
(`2.4.58-1ubuntu8.4`) comes from `noble-updates` (main) and `noble-security`
(main). The *original* version (`2.4.58-1ubuntu8`) comes from `noble` (main).
This tells us that this was the version released with the with 24.04 LTS
(Noble Numbat).

### Installing older package versions

We can install specific older versions if we want to, for example, to satisfy
dependency requirements of another package. We can do that by specifying the
package name and version:

```bash
sudo apt install <package=version>
```

However, this can be tricky and often leads to conflicts in dependency
versions as APT always wants to install the most recent version. We can see an
example of this if we run the following command:

```bash
sudo apt install apache2=2.4.58-1ubuntu8
```

APT warns us that the version of apache2 we want to install depends
on earlier versions of the dependencies, but it helpfully tells us which
dependency versions we need to successfully install the package we want.

```bash
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

So, all we need to do is first install the dependencies, and then run the
install command again. Remember that we can install multiple packages at once
by separating them with spaces:

```bash
sudo apt install apache2-bin=2.4.58-1ubuntu8 \
  apache2-data=2.4.58-1ubuntu8 \
  apache2-utils=2.4.58-1ubuntu8 \
  apache2=2.4.58-1ubuntu8
```

In this case we're also breaking the command over multiple lines using
backslashes (`\`) to make it easier to read, but it will still be run as a
single command.

APT will warn us that we are downgrading the package, but let us press
<kbd>Y</kbd> to confirm (when prompted), and it will go ahead and downgrade us
anyway. Let's run the following command again:

```bash
apt policy apache2
```

And we'll get confirmation that we're running on an older version:

```bash
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

### APT sources

You may be wondering by now "where exactly do all these packages come from?".
We've spotted a few sources very briefly throughout this tutorial, but haven't
paid direct attention to them yet. Let's take a little time now to define what
we mean by all these different sources that APT can pull packages from.

There is a system file that defines what we mean by all the different sources.
We can view the file by running the following command:

```bash
cat /etc/apt/sources.list.d/ubuntu.sources
```

The APT repository is split into four **components**:

|                          | Open source     | Closed source   |
| ---                      | ---             | ---             |
| **Officially supported** | main            | restricted      |
| **Community supported**  | universe        | multiverse      |

- **main** contains the open-source packages that are officially supported by
  Canonical. These packages are either installed on every Ubuntu machine, or
  are very widely used for various types of systems.
- **universe** holds all other open-source packages in Ubuntu, which are
  typically maintained by the Debian and Ubuntu communities, but may also
  include additional security coverage from Canonical under
  [Ubuntu Pro](https://ubuntu.com/pro), which is available free for personal
  use on up to five machines.
- **restricted** contains the packages that are officially supported by
  Canonical but are not available under a completely free license.
- **multiverse** contains community-maintained proprietary software -- these
  packages are completely unsupported by Canonical.

Every Ubuntu release (`noble`, `jammy`, etc) is also split into **pockets**
which are related to the development/release lifecycle:

- **release** contains the packages as they are at release time.
- **proposed** contains package updates while they are being tested.
- Once an update is released, they come from either **security** or **updates**
  depending on whether they are a security-related update or not.
- And **backports**, which contains packages that were not available at release
  time.

This is why earlier, we saw that some updates came from `noble-updates` or
`noble-security`. The original version of the apache2 package that we saw came
from `noble` -- the release pocket only takes the name of the Ubuntu release. 

If you would like more information about the Ubuntu release process, or to
learn more about the sort of terminology you might come across, you may
be interested in the
[Ubuntu Packaging Guide](https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/).

### Building from source

Although APT is the preferred way to install packages on your system, due to
its ability to handle depedencies and keep software up-to-date, not every
package is available in the APT repository -- especially if they are so old
they are no longer maintained, or conversely, are the newest version still in
development!

We can handle deb packages that aren't in the APT repository using `dpkg` --
all we need is to download the deb, and we can run a command like this to
install it:

```bash
sudo dpkg -i <package name>
```

However, it is also possible to obtain software by building it from the source.
Doing this requres us to handle all the dependencies manually, and is is best
avoided if possible on a live system as it can become quite complicated and can
{ref}`have unintended consequences <third-party-repository-usage>`. But --
since we are using a VM anyway, let us take a look at how this done!

We've already seen how to handle missing or conflicting dependecies, and we
have also seen how to verify checksums -- these are both important aspects to
installing packages from source, so let's put our new knowledge to work!

#### Downloading the files

Now that we're running an old version of `apache2` on our system, let us build
the most up-to-date development version (`2.4.62` at the time of writing) from
source. We are fortunate, since Apache2 has instructions for building the
package on the
[Apache2 download site](https://httpd.apache.org/download.cgi#apache24). The
instructions will be different for every package (and not every package comes
with instructions), but the principles are the same.

All the package files are contained in a compressed single file called a
"tarball" (which has the `.tar.gz` file extension). The maintainers should also
provide the files needed to verify the package -- in the case of Apache2, they
do! Let's first download the tarball:

```bash
wget https://dlcdn.apache.org/httpd/httpd-2.4.62.tar.gz
```

#### Verifying the checksums

For this particular version of `apache` there is no MD5 checksum file so we
can't use the `md5sum` tool we used earlier. But, there *are* SHA256 and SHA512
checksum files. Let's download the SHA256 checksum file -- it's advised to
download these from the official source, so let's do that:

```bash
wget https://downloads.apache.org/httpd/httpd-2.4.62.tar.gz.sha256
```

Then we can verify the package download against that checksum using the
`sha256sum` tool:

```bash
sha256sum -c httpd-2.4.62.tar.gz.sha256
```

Which should return:

```bash
httpd-2.4.62.tar.gz: OK
```

This tells us that the package file is validated. If the output returned
`FAILED` then we would know something is wrong with it. In that case, we would
want to download the file again (from a trusted source, preferably). We
definitely wouldn't want to install it if the check fails! 

In our case, since we obtained the package from a trusted source (the official
website) and the checksums matched, we can proceed with the installation.

#### Unpacking and installing

First,  let's "un-tar" the tarball:

```bash
tar -xvzf httpd-2.4.62.tar.gz
```

This will unpack the contents of the tarball into a directory of the same name,
which we can change to:

```bash
cd httpd-2.4.62
```

If we run `ls --all` we can see a list of all the files that are contained in
the package.

There are a couple of dependencies that we'll want to install that don't come
packaged with the development version, so let's install those now:

```bash
sudo apt install autoconf libtool-bin
```

Next we'll want to configure the source tree -- the prefix is the most
important option, so let's set that (for the sake of this example, we'll just
set it to the default location):

```bash
./configure --prefix=/usr/local/apache2
```

Configuration is an important step, because this is where the Makefiles are
created that will allow us to install the package. It will take a few moments
as it checks all the files.

Next, we want to compile by running `make`, and then install by running
`make install`:

```bash
make
make install
```

Now at this point, we could consider ourselves done, but installing this way
means that there's no easy way to uninstall or update the package in the
future since the package managers (`apt` and `dpkg`) can't track them. So one
thing we can do is to create an installable deb package (which will help to
make removal easier!) -- to do that, we can use the `fpm` utility.
This is a Ruby package that needs to be installed via `gem`:

```bash
sudo apt install ruby ruby-dev gcc
gem install fpm
```

Then we can create the package:

```bash
fpm -s dir -t deb -n apache2-custom -v 2.4.62 /usr/local/apache2
```

Now if we do `ls` again we will see a new file has turned up:

```bash
apache2-custom_2.4.62_amd64.deb
```

Now that we have a deb file, we can install it using `dpkg`:

```bash
sudo dpkg -i apache2-custom_2.4.62_amd64.deb
```

If we then wanted to remove it later, we could do so again using `dpkg`. Let's
do that now:

```bash
sudo dpkg -r apache2-custom
```

However, this will often leave a lot of files behind and certainly doesn't
provide a clean uninstall. You will often need to check the Makefile to see
where other files might have been placed, and manually remove them. It also
won't remove any dependencies -- or even track the dependencies we installed,
so we'd need to remove those manually too!

Definitely not an easy process!

If a particular package is not available in the APT repositories, it's often
worth checking to see if the software is available as a **snap** before we
resort to building packages ourselves from the source. 

## Snaps

Snaps are a newer, self-contained software format that were developed to be
a more portable and easy-to-use alternative to debs. They come with all their
dependencies pre-bundled so that there is no need for a package management tool
to track dependencies, and they run inside sandboxed environments that limit
their interactions with the rest of the system.

Instead of **versions** as we have them in debs, snaps use the concept of
[**channels**](https://snapcraft.io/docs/channels) to define which release of a
snap is installed.

By default, snaps are kept automatically up-to-date, so we don't need to
remember to update and upgrade them. There are times on a live system, such as
a server in a production environment, where we might not want to have updates
automatically applied. In those cases, we can
[turn off automatic updates](https://snapcraft.io/docs/managing-updates) and
refresh the system snaps when it's convenient (for example, during a
maintenance window).

If you would like to try out snaps, we recommend the excellent
[quickstart tour](https://snapcraft.io/docs/quickstart-tour) tutorial in the
snap documentation. Feel free to continue using the VM we've been using in
this tutorial while exploring!

## Completion!

Once you are finished and want to leave the tutorial, you can run:

```bash
exit
```

This will take you out of the VM and back to your live machine. Then, you can
run the following commands to delete the VM and remove it completely from your
machine:

```bash
multipass delete tutorial
multipass purge
```

## Summary

Congratulations, we made it to the end! We've covered a lot of material in this
tutorial, so let's do a quick recap of what we've learned:

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

* We even learned how to downgrade to older versions of APT packages, and all
  about APT sources.

**Customising packages**

* How to find the conffiles in a package:
  * `dpkg-query --show -f='${Conffiles}\n' <package>`

* How to see if package files have been changed:
  * `dpkg --verify <package>`

* ...And if a non-conffile has been changed by accident, we can fix it with:
  * `sudo apt install --reinstall <package>`

* We know that our changes to conffiles are always safely preserved, while
  changes to non-conffiles are reverted at the next upgrade or security fix.

* Importantly, we know how to verify checksums with either `md5sum` or similar
  tools, which helps us to more safely build packages from source.

* And finally, we learned about snaps!


