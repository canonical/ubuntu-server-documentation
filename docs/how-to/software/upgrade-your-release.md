---
myst:
  html_meta:
    description: Upgrade Ubuntu Server to the next major LTS release with this comprehensive guide covering pre-upgrade checklist, do-release-upgrade, and troubleshooting.
---

(upgrade-your-release)=
# How to upgrade your Ubuntu release

In this page we show how to upgrade an Ubuntu Server or Ubuntu cloud image to the next major release. This is different from your regular software updates.

We recommend running a Long Term Support (LTS) release as it provides 5 years of standard support and security updates, whereas interim releases are only supported for nine months.

After the initial standard support period ends for an LTS release, an extended maintenance period is available via an [Ubuntu Pro subscription](https://ubuntu.com/pro), which provides coverage for an additional five years and is available for free on up to five machines. Find out more about the [release lifecycle and support period](https://ubuntu.com/about/release-cycle) for your release.

## Understanding Upgrade Paths
You can only upgrade from one LTS release directly to the **next sequential LTS release**. For example, if you are on Ubuntu 16.04 LTS, you can upgrade to Ubuntu 18.04 LTS.
However, you cannot skip releases (e.g. jump from 16.04 LTS to 20.04 LTS).If you need to reach a later LTS, you will have to upgrade in stages: first to Ubuntu 18.04 LTS, then to Ubuntu 20.04 LTS, and so on.


## Pre-upgrade checklist

Before starting a major release upgrade, it's important to prepare your system to ensure a smooth transition. This step is essential, so we need to review the following items:

* **Review Releases notes:** Always check the **release notes** for the new Ubuntu version we are moving to. This can be found on the [Ubuntu Wiki Releases Page](https://wiki.ubuntu.com/Releases).

* **Fully update the current system:** The release upgrade process requires that the current system has all the latest updates installed. This is a standard **package upgrade**: **apt update** will refresh package index database, and **apt upgrade** will download and install the latest versions of installed packages.

  1. Run these commands to ensure everything is up to date:

      ```bash
      sudo apt update
      sudo apt upgrade
      ```
  2. Confirm both commands complete successfully and no further updates are available.

  3. After applying all updates, it may be necessary to **reboot your system.** The release upgrade process will let you know if that's needed, but you can also check manually before: if the file `/run/reboot-required` exists, then you will need to reboot.

* **Check that there is enough free space:** A release upgrade involves downloading hundreds of new packages, which can be several gigabytes. Make sure you have enough free disk space.

* **Dedicate time for the upgrade:** This is an interactive process. The release upgrade will sometimes stop and ask questions, so you should monitor the upgrade and be available to respond.

* **Understand Third-party repositories:**  Third-party software repositories and Personal Package Archives (PPAs) are disabled during the release upgrade. While software installed from these sources will not be removed, it's the most common cause of upgrade issues. Be prepared to re-enable them or find updated versions after the upgrade.

* **Backup all your data:**  Although upgrades are normally safe, there is always a chance that something could go wrong. It is extremely important that the data is safely copied to a backup location to allow restoration if any problems occur.

## Upgrade the system

We recommend upgrading the system using the `do-release-upgrade` command on Server edition and cloud images. This command can handle system configuration changes that are sometimes needed between releases.

To start the process, run this command:

```bash
sudo do-release-upgrade
```

```{note}
Upgrading to a development release of Ubuntu is available using the `-d` flag. However, using the development release (or the `-d` flag) is **not recommended** for production environments. 
```

Upgrades from one LTS release to the next one are only available after the first point release. For example, Ubuntu 18.04 LTS will only upgrade to Ubuntu 20.04 LTS after the 20.04.1 point release. If users wish to update before the point release (e.g., on a subset of machines to evaluate the LTS upgrade) users can force the upgrade via the `-d` flag.

### Pre-upgrade summary

Before making any changes the command `do-release-upgrade` will first do some checks to verify the system is ready to upgrade, and provide a summary of the upgrade before proceeding. If you accept the changes, the process will begin to update the system’s packages:

```text
Do you want to start the upgrade?  


5 installed packages are no longer supported by Canonical. You can  
still get support from the community.  

4 packages are going to be removed. 117 new packages are going to be  
installed. 424 packages are going to be upgraded.  

You have to download a total of 262 M. This download will take about  
33 minutes with a 1Mbit DSL connection and about 10 hours with a 56k  
modem.  

Fetching and installing the upgrade can take several hours. Once the  
download has finished, the process cannot be canceled.  

Continue [yN]  Details [d]
```

### Configuration changes

During the upgrade process you may be presented with a message to make decisions about package updates. These prompts occur when there are existing configuration files (e.g. edited by the user) and the new package configuration file are different. Below is an example prompt:

```text
Configuration file '/etc/ssh/ssh_config'
 ==> Modified (by you or by a script) since installation.
 ==> Package distributor has shipped an updated version.
   What would you like to do about it ?  Your options are:
    Y or I  : install the package maintainer's version
    N or O  : keep your currently-installed version
      D     : show the differences between the versions
      Z     : start a shell to examine the situation
 The default action is to keep your current version.
*** ssh_config (Y/I/N/O/D/Z) [default=N] ?
```

You should look at the differences between the files and decide what to do. The default response is to keep the current version of the file. There are situations where accepting the new version, like with `/boot/grub/menu.lst`, is required for the system to boot correctly with the new kernel.

### Removing Obsolete Packages

After all packages are updated, you can choose to remove any obsolete packages that are no longer needed:

```text
Remove obsolete packages?  


30 packages are going to be removed.  

Continue [yN]  Details [d]
```

### Reboot

Finally, when the upgrade is complete you are prompted to reboot the system. The system is not considered upgraded until this reboot occurs:

```text
System upgrade is complete.

Restart required  

To finish the upgrade, a restart is required.  
If you select 'y' the system will be restarted.  

Continue [yN]
```

## Further reading

- For a complete list of releases and current support status, see the [List of releases](https://documentation.ubuntu.com/project/release-team/list-of-releases/) page.
