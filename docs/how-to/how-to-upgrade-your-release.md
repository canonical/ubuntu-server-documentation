(how-to-upgrade-your-release)=
# Upgrade your release

In this page we show how to upgrade an Ubuntu Server or Ubuntu cloud image to the next release.

We recommend running a Long Term Support (LTS) release as it provides 5 years of standard support and security updates, whereas interim releases are only supported for nine months.

After the initial standard support period ends for an LTS release, an extended maintenance period is available via an [Ubuntu Pro subscription](http://ubuntu.com/pro), which provides coverage for an additional five years and is available for free on up to five machines. Find out more about the [release lifecycle and support period](https://ubuntu.com/about/release-cycle) for your release.

## Upgrade paths

Ubuntu supports the ability to upgrade from one LTS to the next in sequential order. For example, a user on Ubuntu 16.04 LTS can upgrade to Ubuntu 18.04 LTS, but cannot jump directly to Ubuntu 20.04 LTS. To do this, the user would need to upgrade twice: once to Ubuntu 18.04 LTS, and then upgrade again to Ubuntu 20.04 LTS.

## Pre-upgrade checklist

To ensure a successful upgrade, review the following items:

* Check the release notes (for the new release) for any known issues or important changes. Release notes for each release are found on the [Ubuntu Wiki releases page](https://wiki.ubuntu.com/Releases).

* Fully update the system. The upgrade process works best when the current system has all the latest updates installed. You should confirm that these commands complete successfully and that no further updates are available. We also suggest rebooting the system after all the updates are applied, to ensure the latest kernel is being run. To upgrade, run the following commands:

  ```bash
  sudo apt update
  sudo apt upgrade
  ```

* Check that there is enough free disk space for the upgrade. Upgrading a system will include downloading new packages, which is likely to be on the order of hundreds of new packages. Systems with additional software installed may therefore require a few gigabytes of free disk space.

* The upgrade process takes time to complete. You should have dedicated time to participate in the upgrade process.

* Third-party software repositories and personal package archives (PPAs) are disabled during the upgrade. However, any software installed from these repositories is not removed or downgraded. Software installed from these repositories is the most common cause of upgrade issues.

* Backup all your data. Although upgrades are normally safe, there is always a chance that something could go wrong. It is extremely important that the data is safely copied to a backup location to allow restoration if there are any problems during the upgrade process.

## Upgrade the system

We recommend upgrading the system using the `do-release-upgrade` command on Server edition and cloud images. This command can handle system configuration changes that are sometimes needed between releases. To begin the process, run the following command:

```bash
sudo do-release-upgrade
```

> **Note**:
> Upgrading to a development release of Ubuntu is available using the `-d` flag. However, using the development release (or the `-d` flag) is **not recommended** for production environments. 

Upgrades from one LTS release to the next one are only available after the first point release. For example, Ubuntu 18.04 LTS will only upgrade to Ubuntu 20.04 LTS after the 20.04.1 point release. If users wish to update before the point release (e.g., on a subset of machines to evaluate the LTS upgrade) users can force the upgrade via the `-d` flag.

### Pre-upgrade summary

Before making any changes the command will first do some checks to verify the system is ready to upgrade, and provide a summary of the upgrade before proceeding. If you accept the changes, the process will begin to update the system’s packages:

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

### Package removal

After all packages are updated, you can choose to remove any obsolete, no-longer-needed packages:

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

- For a complete list of releases and current support status see the [Ubuntu Wiki Releases](https://wiki.ubuntu.com/Releases) page.
