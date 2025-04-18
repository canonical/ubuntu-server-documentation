(about-apt-upgrade-and-phased-updates)=
# About apt upgrade and phased updates


You may have noticed recently that updating your system with `apt upgrade` sometimes produces a weird message about packages being kept back...like this one:

```bash
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Calculating upgrade... Done
The following packages have been kept back:
  (Names of <X> held back packages listed here)
0 upgraded, 0 newly installed, 0 to remove and <X> not upgraded.
```

If you’ve ever used combinations of packages from different releases or third party repos, you may be familiar with this message already. However, it has become a much more common occurrence due to something called "phased updates".

## What are phased updates?

Phased updates are software updates that are rolled out in stages, rather than being provided to everyone at the same time. Initially, the update is provided only to a small subset of Ubuntu machines. As the update proves to be stable, it is provided to an ever-increasing number of users until everyone has received it (i.e., when the update is "fully phased").

The good news is, you don't need to do anything about the "packages kept back" message -- you can safely ignore it. Once the update has been deemed safe for release, you will receive the update automatically.

## Why is Ubuntu doing this?

Although updates are thoroughly tested before they get released at all, sometimes bugs can be hidden well enough to escape our attention and make it into a release -- especially in highly specific use cases that we didn’t know we needed to test. This can obviously cause problems for our users, and used to be the norm before we phased updates through `apt`.

Update phasing makes it much easier for us to detect serious breakages early on -- before they have a chance to cause problems for the majority of our users. It gives us the opportunity to hold back the update until the bugs are fixed.

In other words, it directly benefits our users by increasing the safety, stability and reliability of Ubuntu.

The phasing system makes it so that different sets of users are chosen to be the first to get the updates, so that there isn't one group of unlucky people who always get potentially broken updates soon after release.

```{note}
It should be mentioned here that security updates are *never* phased.
```

## Can I turn off phased updates?

That depends on how stable you need your system to be. If you just want to avoid any notices about packages being held back during `apt` updates, and you're willing to be one of the first people to get updates whenever they're released, you can turn off phased updates. Be warned, though -- if an update *is* broken, you will almost always be in the first set of people to get it (i.e., you're basically volunteering yourself as a guinea pig for the early update releases!). It will get rid of the "held back packages" in `apt` message, though.

If that doesn't sound like something you want, leave phased updates on (this is the default). You will still temporarily get the "held back packages" message, but your machine will be more protected from updates that might otherwise break it -- and once the packages are ready to be safely installed on your system, they will no longer be held back.

## Can I `apt upgrade` the individual packages? (and should I?)

While you can *technically* get around phased updates by running `apt install` on individual held back packages, it's not recommended. You're unlikely to break your machine by doing this -- as long as the package is being held back due to update phasing. 

If you want to `apt upgrade` a package, you should first carefully examine the proposed changes that `apt` would make before you proceed. If the package update was kept back for a reason unrelated to phasing, `apt` may be forced to remove packages in order to complete your request, which could then cause problems elsewhere. 

## How do I turn off phased updates?
 
If you're sure that you want to disable phased updates, reverting to the old behaviour, you can change `apt`'s configuration by creating a file in `/etc/apt/apt.conf.d` called `99-Phased-Updates` (if `/etc/apt/apt.conf.d/99-Phased-Updates` doesn't already exist). In the file, simply add the following lines:

```bash
Update-Manager::Always-Include-Phased-Updates true;
APT::Get::Always-Include-Phased-Updates true;
```

Again, please only do this if you really know what you're doing and are absolutely sure you need to do it (for instance, if you are intentionally installing all the latest packages to help test them -- and don't mind if your system breaks). We definitely don't recommend turning off phased updates if you're a newer user.

## Why is this suddenly happening now?

Phased updates have been part of the update-manager on Ubuntu Desktop for quite a while (since 13.04, in fact!), but were [implemented in APT in 21.04](https://discourse.ubuntu.com/t/phased-updates-in-apt-in-21-04/20345). It now works on all versions of Ubuntu (including Ubuntu Server, Raspberry Pi, and containers). Since this includes the 22.04 LTS, it's now getting a lot more attention as a result!

## How does it actually work?

Phased updates depend on a value derived from your machine's "Machine ID", as well as the package name and package version. The neat thing about this is that phasing is determined completely at the client end; no identifiable information (or indeed any new information at all) is ever sent to the server to achieve update phasing.

When the software update is released, the initial subset of machines to receive the update first is chosen at random. Only if there are no problems detected by the first set of users will the update be made available to everyone.

For more detailed information, including about how changes to phasing are timed, you can check the Ubuntu [wiki page on phased updates](https://wiki.ubuntu.com/PhasedUpdates).

## How can I find out more information about currently phased packages?

You can find out the phasing details of a package by using the `apt policy` command:

```bash
apt policy <package>
```

For example, at the time of writing, the package `libglapi-mesa` has a phased update. Running `apt policy libglapi-mesa` then produces an output like this:

```bash
libglapi-mesa:
  Installed: 22.0.5-0ubuntu0.3
  Candidate: 22.2.5-0ubuntu0.1~22.04.1
  Version table:
 	22.2.5-0ubuntu0.1~22.04.1 500 (phased 20%)
    	500 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages
 *** 22.0.5-0ubuntu0.3 100
    	100 /var/lib/dpkg/status
 	22.0.1-1ubuntu2 500
    	500 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages
```

In this output you can see that this package is 20% phased.

You can see the status of all packages currently being phased in Ubuntu at https://people.canonical.com/~ubuntu-archive/phased-updates.html

## Further reading

- The details in this page are based on this [excellent post on AskUbuntu](https://askubuntu.com/questions/1431940/what-are-phased-updates-and-why-does-ubuntu-use-them) by AskUbuntu user *ArrayBolt3*. This page is therefore licensed under Creative Commons Attribution-ShareAlike license, distributed under the terms of [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

- You can check on the progress of the current [phasing Ubuntu Stable Release Updates](https://people.canonical.com/~ubuntu-archive/phased-updates.html).

- There is also more detail on how phased updates work in the [Ubuntu wiki](https://wiki.ubuntu.com/PhasedUpdates), the [Error Tracker](https://wiki.ubuntu.com/ErrorTracker/PhasedUpdates), and the [`apt` preferences manpage](https://manpages.ubuntu.com/manpages/jammy/man5/apt_preferences.5.html).
