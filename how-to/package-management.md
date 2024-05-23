# Package management

Ubuntu features a comprehensive package management system for installing, upgrading, configuring, and removing software.

It provides access to an organised base of over 60,000 software packages for your Ubuntu computer, and includes the ability to resolve dependencies and check for software updates.

Several tools are available for interacting with Ubuntu's package management system, from command-line utilities that can be easily automated by system administrators, to an easy-to-use graphical interface for those new to Ubuntu.

## Introduction

Ubuntu's package management system is derived from the same system used by the Debian GNU/Linux distribution. The package files contain all the necessary files, metadata, and instructions to implement a particular function or software application on your Ubuntu computer.

Debian package files typically have the extension `.deb`, and usually exist in **repositories**, which are collections of packages typically found online, or on physical media such as CD-ROMs. Packages are normally in a pre-compiled binary format; installation is quick and requires no software compilation.

Many packages use **dependencies**. Dependencies are additional packages required by a given package for it to function properly. For example, the speech synthesis package `festival` depends upon the package `alsa-utils`, which is a package supplying the [Advanced Linux Sound Architecture (ALSA)](https://www.alsa-project.org/wiki/Main_Page) sound library tools needed for audio playback. For `festival` to function, it -- and all of its dependencies -- must be installed. The software management tools in Ubuntu will do this automatically.

## Advanced Packaging Tool

The `apt` command is a powerful command-line tool, which works with Ubuntu's Advanced Packaging Tool (APT). The commands contained within `apt` provide the means to install new software packages, upgrade existing software packages, update the package list index, and even upgrade the entire Ubuntu system.

Actions of the `apt` command, such as installation and removal of packages, are logged in the `/var/log/dpkg.log` log file.

Some examples of popular uses for `apt` include:

### Installing packages

As an example, to install the `nmap` network scanner, run the following command:

```bash
sudo apt install nmap
```

> **Tip**:
> You can install or remove multiple packages at once by separating them with spaces.

### Removing packages

To remove the package installed in the previous example, run the following:

```bash    
sudo apt remove nmap
```    

Adding the `--purge` option to `apt remove` will remove the package configuration files as well. This may or may not be what you want, so use it with caution.
    
> **Note**:
> While `apt` is a command-line tool, it is intended to be used interactively, and not to be called from non-interactive scripts. The `apt-get` command should be used in scripts (perhaps with the `--quiet` flag). For basic commands the syntax of the two tools is identical.

### Updating the package index
 
The APT package index is a database of available packages from the repositories defined in the `/etc/apt/sources.list` file and in the `/etc/apt/sources.list.d` directory. To update the local package index with the latest changes made in the repositories, type the following:
    
```bash
sudo apt update
```
  
### Upgrading packages 

Installed packages on your computer may periodically have upgrades available from the package repositories (e.g., security updates). To upgrade your system, first update your package index and then perform the upgrade -- as follows:
    
```bash
sudo apt update
sudo apt upgrade
```
    
For details on how to upgrade to a new Ubuntu release, see our [guide on upgrading releases](how-to-upgrade-your-release.md). For further information about using APT, read the comprehensive [APT User's Guide](https://www.debian.org/doc/user-manuals#apt-guide), or type `apt help`.

## Aptitude

Launching Aptitude with no command-line options will give you a menu-driven, text-based frontend to the APT system. Many of the common package management functions, such as installation, removal, and upgrade, can be performed in Aptitude with single-key commands, which are typically lowercase letters.

Aptitude is best suited for use in a non-graphical terminal environment to ensure the command keys work properly. You can start the menu-driven interface of Aptitude as a regular user by typing the following command at a terminal prompt:

```bash
sudo aptitude
```

When Aptitude starts, you will see a menu bar at the top of the screen and two panes below the menu bar. The top pane contains package categories, such as "New Packages" and "Not Installed Packages". The bottom pane contains information related to the packages and package categories.

Using Aptitude for package management is relatively straightforward thanks to its user interface. The following are examples of common package management functions as performed in Aptitude:

### Installing packages

To install a package, locate it in the "Not Installed Packages" category by using the keyboard arrow keys and the <kbd>Enter</kbd> key.

Highlight the desired package, then press the <kbd>+</kbd> key. The package entry should turn **green**, which indicates it has been marked for installation. Now press <kbd>g</kbd> to be presented with a summary of package actions. Press <kbd>g</kbd> again, and the package will be downloaded and installed. When finished, press <kbd>Enter</kbd> to return to the menu.

### Remove Packages

To remove a package, locate it in the "Installed Packages" category by using the keyboard arrow keys and the <kbd>Enter</kbd> key.

Highlight the package you want to remove, then press the <kbd>-</kbd> key. The package entry should turn **pink**, indicating it has been marked for removal. Now press <kbd>g</kbd> to be presented with a summary of package actions. Press <kbd>g</kbd> again, and the package will be removed. When finished, press <kbd>Enter</kbd> to return to the menu.

### Updating the package index 

To update the package index, press the <kbd>u</kbd> key.

### Upgrade packages

To upgrade packages, first update the package index as detailed above, and then press the <kbd>U</kbd> key to mark all packages with available updates. Now press <kbd>g</kbd>, which will present you with a summary of package actions. Press <kbd>g</kbd> again to begin the download and installation. When finished, press <kbd>Enter</kbd> to return to the menu.

The first column of information displayed in the package list (in the top pane) lists the current state of the package (when viewing packages). It uses the following key to describe the package state:

- **i** : Installed package

- **c** : Package not installed, but package configuration remains on the system

- **p** : Purged from system

- **v** : Virtual package

- **B** : Broken package

- **u** : Unpacked files, but package not yet configured

- **C** : Half-configured - configuration failed and requires fix

- **H** : Half-installed - removal failed and requires a fix

To exit Aptitude, simply press the <kbd>q</kbd> key and confirm you want to exit. Many other functions are available from the Aptitude menu by pressing the <kbd>F10</kbd> key.

### Command-line Aptitude

You can also use Aptitude as a command-line tool, similar to `apt`. To install the `nmap` package with all necessary dependencies (as in the `apt` example), you would use the following command:

```bash
sudo aptitude install nmap
```

To remove the same package, you would use the command:

```bash
sudo aptitude remove nmap
```

Consult the [Aptitude manpages](https://manpages.ubuntu.com/manpages/man8/aptitude-curses.8.html) for full details of Aptitude's command-line options.

## dpkg

`dpkg` is a package manager for Debian-based systems. It can install, remove, and build packages, but unlike other package management systems, it cannot automatically download and install packages -- or their dependencies. 

APT and Aptitude are newer, and layer additional features on top of `dpkg`. This section covers using `dpkg` to manage locally installed packages.

### List packages

To list *all* packages in the system’s package database (both installed and uninstalled) run the following command from a terminal prompt:

```bash
dpkg -l
```

Depending on the number of packages on your system, this can generate a large amount of output. Pipe the output through `grep` to see if a specific package is installed:

```bash
dpkg -l | grep apache2
```
    
Replace `apache2` with any package name, part of a package name, or a regular expression.

### List files

To list the files installed by a package, in this case the `ufw` package, enter:
   
```bash
dpkg -L ufw
```

If you are unsure which package installed a file, `dpkg -S` may be able to tell you. For example:
    
```bash
dpkg -S /etc/host.conf 
base-files: /etc/host.conf
```

The output shows that the `/etc/host.conf` belongs to the base-files package.
    
> **Note**:
> Many files are automatically generated during the package install process, and even though they are on the filesystem, `dpkg -S` may not know which package they belong to.

### Installing a deb file

You can install a local `.deb` file by entering:

```bash
sudo dpkg -i zip_3.0-4_amd64.deb
```

Change `zip_3.0-4_amd64.deb` to the actual file name of the local `.deb` file you wish to install.

### Uninstalling packages

You can uninstall a package by running:

```bash
sudo dpkg -r zip
```
    
> **Caution**:
> Uninstalling packages using `dpkg`, is **NOT** recommended in most cases. It is better to use a package manager that handles dependencies to ensure that the system is left in a consistent state. For example, using `dpkg -r zip` will remove the `zip` package, but any packages that depend on it will still be installed and may no longer function correctly as a result.

For more `dpkg` options see the [`dpkg` manpage](https://manpages.ubuntu.com/manpages/en/man1/dpkg.1.html): `man dpkg`.

## APT configuration

Configuration of the APT system repositories is stored in the `/etc/apt/sources.list` file and the `/etc/apt/sources.list.d` directory. An example of this file is referenced here, along with information on adding or removing repository references from the file.

You can edit the file to enable and disable repositories. For example, to disable the requirement to insert the Ubuntu CD-ROM whenever package operations occur, simply comment out the appropriate line for the CD-ROM, which appears at the top of the file:

```text
# no more prompting for CD-ROM please
# deb cdrom:[DISTRO-APT-CD-NAME - Release i386 (20111013.1)]/ DISTRO-SHORT-CODENAME main restricted
```

### Extra repositories

In addition to the officially-supported package repositories available for Ubuntu, there are also community-maintained repositories which add thousands more packages for potential installation. Two of the most popular are the *universe* and *multiverse* repositories. These repositories are not officially supported by Ubuntu, but because they are maintained by the community they generally provide packages which are safe for use with your Ubuntu computer.

For more information, see our guide on [using third-party repositories](../explanation/third-party-repository-usage.md).

> **Warning**:
> Be advised that neither *universe* nor *multiverse* contain officially-supported packages. In particular, there may not be security updates for these packages.
>
> Packages in the *multiverse* repository often have licensing issues that prevent them from being distributed with a free operating system, and they may be illegal in your locality.

Many other package sources are available -- sometimes even offering only one package, as in the case of packages provided by the developer of a single application. You should always be cautious when using non-standard package sources/repos, however. Research the packages and their origins carefully before performing any installation, as some packages could render your system unstable or non-functional in some respects.

By default, the *universe* and *multiverse* repositories are enabled. If you would like to disable them, edit `/etc/apt/sources.list` and comment out the following lines:

```text
deb http://archive.ubuntu.com/ubuntu DISTRO-SHORT-CODENAME universe multiverse
deb-src http://archive.ubuntu.com/ubuntu DISTRO-SHORT-CODENAME universe multiverse
    
deb http://us.archive.ubuntu.com/ubuntu/ DISTRO-SHORT-CODENAME universe
deb-src http://us.archive.ubuntu.com/ubuntu/ DISTRO-SHORT-CODENAME universe
deb http://us.archive.ubuntu.com/ubuntu/ DISTRO-SHORT-CODENAME-updates universe
deb-src http://us.archive.ubuntu.com/ubuntu/ DISTRO-SHORT-CODENAME-updates universe
    
deb http://us.archive.ubuntu.com/ubuntu/ DISTRO-SHORT-CODENAME multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ DISTRO-SHORT-CODENAME multiverse
deb http://us.archive.ubuntu.com/ubuntu/ DISTRO-SHORT-CODENAME-updates multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ DISTRO-SHORT-CODENAME-updates multiverse
    
deb http://security.ubuntu.com/ubuntu DISTRO-SHORT-CODENAME-security universe
deb-src http://security.ubuntu.com/ubuntu DISTRO-SHORT-CODENAME-security universe
deb http://security.ubuntu.com/ubuntu DISTRO-SHORT-CODENAME-security multiverse
deb-src http://security.ubuntu.com/ubuntu DISTRO-SHORT-CODENAME-security multiverse
```
<h2 id='heading--automatic-updates'>Automatic updates</h2>

The `unattended-upgrades` package can be used to automatically update installed packages and can be configured to update all packages or to only install security updates. First, install the package by entering the following in a terminal:

```bash
sudo apt install unattended-upgrades
```

To configure `unattended-upgrades`, edit `/etc/apt/apt.conf.d/50unattended-upgrades` and adjust the following to fit your needs:

```text
Unattended-Upgrade::Allowed-Origins {
        "${distro_id}:${distro_codename}";
        "${distro_id}:${distro_codename}-security";
//      "${distro_id}:${distro_codename}-updates";
//      "${distro_id}:${distro_codename}-proposed";
//      "${distro_id}:${distro_codename}-backports";
};
```

Certain packages can also be excluded and therefore will not be automatically updated. To block a package, add it to the list:

```text
Unattended-Upgrade::Package-Blacklist {
//      "vim";
//      "libc6";
//      "libc6-dev";
//      "libc6-i686";
};
```

> **Note**:
> The double “//” serve as comments, so whatever follows "//" will not be evaluated.

To enable automatic updates, edit `/etc/apt/apt.conf.d/20auto-upgrades` and set the appropriate APT configuration options:

```text
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
```

The above configuration updates the package list, then downloads and installs available upgrades every day. These actions are triggered by timer units at a set time but with a random delay:  `apt-daily.timer` and `apt-daily-upgrade.timer`. These timers activate the corresponding services that run the `/usr/lib/apt/apt.systemd.daily` script.

However, it may happen that if the server is off at the time the timer unit elapses, the timer will be triggered immediately at the next startup. As a result, they will often run on system startup 
and thereby cause immediate activity and hold the apt-lock.

In many cases this is beneficial, but in some cases it might be counter-productive; examples are administrators with many shut-down machines or VM images that are only started for some quick action, which is delayed or even blocked by the unattended upgrades. To adapt this behaviour, we can change/override the configuration of both APT's timer units [`apt-daily-upgrade.timer, apt-daily.timer`]. To do so, use `systemctl edit <timer_unit>` and override the *Persistent* attribute, for example with `Persistent=delay`:

```
[Timer]
Persistent=delay
```

The local download archive is cleaned every week. On servers upgraded to newer versions of Ubuntu, depending on your responses, the file listed above may not be there. In this case, creating a new file of the same name should also work.

> **Note**:
> You can read more about `apt` *Periodic* configuration options in the `apt.conf(5)` manpage and in the `/usr/lib/apt/apt.systemd.daily` script header.

The results of `unattended-upgrades` will be logged to `/var/log/unattended-upgrades`.

### Notifications

Configuring `Unattended-Upgrade::Mail` in `/etc/apt/apt.conf.d/50unattended-upgrades` will enable `unattended-upgrades` to email an administrator detailing any packages that need upgrading or have problems.

Another useful package is `apticron`. `apticron` will configure a cron job to email an administrator information about any packages on the system that have updates available, as well as a summary of changes in each package.

To install the `apticron` package, enter the following command in a terminal:

```bash
sudo apt install apticron
```

Once the package is installed, edit `/etc/apticron/apticron.conf`, to set the email address and other options:

```text
EMAIL="root@example.com"
```

## Further reading

Most of the material covered in this chapter is available in the respective man pages, many of which are available online.

- The [Installing Software](https://help.ubuntu.com/community/InstallingSoftware) Ubuntu wiki page has more information.
- The [APT User's Guide](https://www.debian.org/doc/user-manuals#apt-guide) contains useful information regarding APT usage.
- For more information about systemd timer units (and systemd in general), visit the [systemd man page](https://manpages.ubuntu.com/manpages/en/man1/systemd.1.html) and [systemd.timer man page](https://manpages.ubuntu.com/manpages/en/man5/systemd.timer.5.html).
- See the [Aptitude user's manual](https://www.debian.org/doc/user-manuals#aptitude-guide) for more Aptitude options.
- The [Adding Repositories HOWTO (Ubuntu Wiki)](https://help.ubuntu.com/community/Repositories/Ubuntu) page contains more details on adding repositories.
