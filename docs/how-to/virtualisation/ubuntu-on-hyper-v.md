---
myst:
  html_meta:
    description: Run Ubuntu virtual machines on Windows Hyper-V hypervisor for development, testing, and Linux software access without dual-booting.
---

(ubuntu-on-hyper-v)=
# How to set up Ubuntu on Hyper-V

Hyper-V is a native [type 1 hypervisor](https://en.wikipedia.org/wiki/Hypervisor#Classification) developed by Microsoft for the Windows family of operating systems, similar to Xen or VMWare {term}`ESXi`. It was first released for Windows Server in 2008, and has been available without additional charge since Windows Server 2012 and Windows 8.

Hyper-V allows Ubuntu to be run in parallel or in isolation on Windows operating systems. There are several use-cases for running Ubuntu on Hyper-V:

* To introduce Ubuntu in a Windows-centric IT environment.
* To have access to a complete Ubuntu desktop environment without dual-booting a PC.
* To use Linux software on Ubuntu that is not yet supported on the [Windows Subsystem for Linux](https://learn.microsoft.com/windows/wsl/about).

## Hyper-V system requirements

The following are typical [system requirements for Hyper-V](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/system-requirements-for-hyper-v-on-windows):

* A 64-bit processor with Second Level Address Translation (SLAT)
* CPU support for virtualization extensions and virtualization enabled in the system BIOS/EFI
* Minimum of 4 GB of memory, recommended 8 GB
* Minimum of 5 GB of disk space, recommended 15 GB

## Install Hyper-V

Hyper-V can be used on Windows 10 and Windows 11 Pro, Enterprise, and Education editions, as well as Windows Server. The installation method differs between Windows client and Windows Server editions.

Hyper-V is not included in Windows 10 or Windows 11 Home, which [would need to be upgraded](https://support.microsoft.com/en-us/windows/upgrade-windows-home-to-windows-pro-ef34d520-e73f-3198-c525-d1a218cc2818) to the Pro edition.

### Install Hyper-V on Windows client

The following steps apply to Windows 10 and Windows 11 editions.

#### Install Hyper-V graphically

1. Right-click on the Windows Start button and select 'Apps and Features'.

1. Select 'Programs and Features' under Related Settings.

1. Select 'Turn Windows Features on or off'.

1. Select 'Hyper-V' and click OK.

1. Restart when prompted.

#### Install Hyper-V using PowerShell

1. Open a PowerShell console as Administrator.

1. Run the following command:
   
   ```
   Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
   ```

1. Restart when prompted.

### Install Hyper-V on Windows Server

On Windows Server editions, Hyper-V is installed as a server role rather than an optional feature. In an elevated PowerShell session, run:

```powershell
Install-WindowsFeature -Name Hyper-V -IncludeManagementTools -Restart
```

For the complete steps — including remote installation and role verification — see Microsoft's guide on [installing the Hyper-V role on Windows Server](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/install-the-hyper-v-role-on-windows-server).

## Install Ubuntu on Hyper-V

There are two main methods for installing Ubuntu on Hyper-V depending on your use case. Read each of the descriptions of the following methods and then determine the best for your situation.

### Using Quick Create

:::{note}
Quick Create is only available on Windows 10 and Windows 11 **client** editions. It is not available on Windows Server. If you are running Windows Server, use the {ref}`New Virtual Machine Wizard <using-the-new-virtual-machine-wizard>` method instead.
:::

The recommended method is to use the curated Ubuntu image from the Hyper-V Quick Create Gallery. This is ideal for desktop development on Ubuntu and for users interested in running a complete Ubuntu desktop environment. The Ubuntu image from the Quick Create Gallery includes pre-configured features, such as clipboard sharing, dynamic resolution display, and shared folders.

1. Enable Hyper-V as described above.

1. Open 'Hyper-V Manager' by either:

   * Selecting the Windows Start button, then
      -> Expanding the 'Windows Administrative Tools' folder 
      -> Selecting 'Hyper-V Manager'

   or

   * Selecting the Windows key, then
      -> Typing 'Hyper-V'
      -> Selecting 'Hyper-V Manager'

   In the future, the Quick Create tool can be accessed directly using the above methods, but it is useful to know where Hyper-V Manager is because it is what you will use to manage your Ubuntu VM.

1. On the 'Actions' pane select 'Quick Create' and the Quick Create tool will open.

1. Select a version of Ubuntu from the versions on the list.

   * The **LTS version** is recommended if you are developing for Ubuntu Server or an enterprise environment.
   * The **interim release** is recommended if you would like to use the latest versions of software in Ubuntu.

1. Select 'Create Virtual Machine' and wait for the VM image to be downloaded.

1. Select 'Connect' to open a connection to your VM.

1. Select 'Start' to run your VM.

1. Complete the final stages of the Ubuntu install, including username selection.

(using-the-new-virtual-machine-wizard)=
### Using the New Virtual Machine Wizard

You can install Ubuntu on Hyper-V using an ISO image and the New Virtual Machine Wizard, which is available on Windows Server. Note that the enhanced features included in Quick Create images (clipboard sharing, dynamic resolution, and shared folders) are not enabled by default with a manual ISO install.

1. Download an Ubuntu ISO from an [official Ubuntu source](https://ubuntu.com/download/server).

1. Install Hyper-V as described above.

1. Open 'Hyper-V Manager'.

1. In the 'Actions' pane, select 'New', then 'Virtual Machine' to open the New Virtual Machine Wizard.

1. Work through the wizard pages:

   * **Name and Location**: Enter a descriptive name (e.g. 'Ubuntu Server 24.04 LTS') and choose a storage location.
   * **Generation**: Select 'Generation 2' for UEFI and Secure Boot support.
   * **Memory**: Assign at least 2048 MB; enable Dynamic Memory if desired.
   * **Networking**: Connect to a virtual switch, or configure networking later.
   * **Virtual Hard Disk**: Create a new virtual hard disk; 25 GB or more is recommended.
   * **Installation Options**: Select 'Install an operating system from a bootable image file' and browse to your ISO.

1. Select 'Finish' and wait for the virtual machine to be created.

1. Before starting the VM, configure Secure Boot: right-click the VM and select 'Settings', then navigate to 'Security'. Under 'Secure Boot', change the template from 'Microsoft Windows' to 'Microsoft UEFI Certificate Authority', then select 'Apply' and 'OK'.

1. Right-click the VM and select 'Connect', then select 'Start' to run your VM.

1. Complete the manual installation of Ubuntu.

### Further reading

For a complete guide on creating virtual machines on Windows Server Hyper-V, see Microsoft's documentation on [creating a virtual machine in Hyper-V](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/create-a-virtual-machine-in-hyper-v).
