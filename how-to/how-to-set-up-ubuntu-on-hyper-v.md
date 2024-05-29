# How to set up Ubuntu on Hyper-V

Hyper-V is a native [type 1 hypervisor](https://en.wikipedia.org/wiki/Hypervisor#Classification) developed by Microsoft for the Windows family of operating systems, similar to Xen or VMWare ESXi. It was first released for Windows Server in 2008, and has been available without additional charge since Windows Server 2012 and Windows 8.

Hyper-V allows Ubuntu to be run in parallel or in isolation on Windows operating systems. There are several use-cases for running Ubuntu on Hyper-V:

* To introduce Ubuntu in a Windows-centric IT environment.
* To have access to a complete Ubuntu desktop environment without dual-booting a PC.
* To use Linux software on Ubuntu that is not yet supported on the[ Windows Subsystem for Linux](https://learn.microsoft.com/windows/wsl/about).

## Hyper-V system requirements

The following are typical [system requirements for Hyper-V](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/system-requirements-for-hyper-v-on-windows):

* A 64-bit processor with Second Level Address Translation (SLAT)
* CPU support for virtualization extensions and virtualization enabled in the system BIOS/EFI
* Minimum of 4 GB of memory, recommended 8 GB
* Minimum of 5 GB of disk space, recommended 15 GB

## Install Hyper-V

Our first step in enabling Ubuntu is to install Hyper-V, which can be used on the Windows 11 Pro, Enterprise, Education and Server operating systems.

Hyper-V is not included in Windows 11 Home, which [would need to be upgraded](https://support.microsoft.com/en-us/windows/upgrade-windows-home-to-windows-pro-ef34d520-e73f-3198-c525-d1a218cc2818) to Windows 11 Pro.

### Install Hyper-V graphically

1. Right click on the Windows Start button and select 'Apps and Features'.

1. Select 'Programs and Features' under Related Settings.

1. Select 'Turn Windows Features on or off'.

1. Select 'Hyper-V' and click OK.

1. Restart when prompted.

### Install Hyper-V using PowerShell

1. Open a PowerShell console as Administrator.

1. Run the following command:
   
   ```
   Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
   ```

1. Restart when prompted.

## Install Ubuntu on Hyper-V

There are two main methods for installing Ubuntu on Hyper-V depending on your use case. Read each of the descriptions of the following methods and then determine the best for your situation.

### Using Quick Create

The recommended method is to use the curated Ubuntu image from the Hyper-V Quick Create Gallery. This is ideal for desktop development on Ubuntu and for users interested in running a complete Ubuntu desktop environment. The Ubuntu image from the Quick Create Gallery includes pre-configured features, such as clipboard sharing, dynamic resolution display, and shared folders.

1. Enable Hyper-V as described above.

1. Open 'Hyper-V Manager' by either:

   * Selecting the Windows Start button, then
      -> Expanding the 'Windows Administrative Tools' folder 
      -> Selecting 'Hyper-V Manager'

   or

   * Selecting the Windows key, then
      -> typing 'Hyper-V'
      -> selecting 'Hyper-V Manager'

   In the future, the Quick Create tool can be accessed directly using the above methods, but it is useful to know where Hyper-V Manager is because it is what you will use to manage your Ubuntu VM.

1. On the 'Actions' pane select 'Quick Create' and the Quick Create tool will open.

1. Select a version of Ubuntu from the versions on the list. A build of the [most recent LTS](https://wiki.ubuntu.com/LTS) version of Ubuntu and the [most recent interim release](https://wiki.ubuntu.com/Releases) are provided.

   * The **LTS version** is recommended if you are developing for Ubuntu Server or an enterprise environment.
   * The **interim release** is recommended if you would like to use the latest versions of software in Ubuntu.

1. Select 'Create Virtual Machine' and wait for the VM image to be downloaded.

1. Select 'Connect' to open a connection to your VM.

1. Select 'Start' to run your VM.

1. Complete the final stages of the Ubuntu install, including username selection.

### Using an Ubuntu CD image

It is possible to install Ubuntu on Hyper-V using a CD image ISO. This is useful if you are running Ubuntu Server and do not need an enhanced desktop experience. Note that the enhanced features of the Quick Create images are not enabled by default when you perform a manual install from an ISO.

1. Download an Ubuntu ISO from an [official Ubuntu source](https://ubuntu.com/download/server).

1. Install Hyper-V as described above.

1. Open 'Hyper-V Manager' by either:

   * Selecting the Windows Start button, then
       -> Expanding the 'Windows Administrative Tools' folder
       -> Selecting 'Hyper-V Manager'

      or
   
   * Selecting the Windows key, then
      -> Typing 'Hyper-V'
      -> Selecting 'Hyper-V Manager'

1. On the 'Actions' pane click 'Quick Create' and the Quick Create tool will open.

1. Select 'Change installation source' and choose the ISO file you downloaded before.

   If you want to give your virtual machine a more descriptive name, select the 'More options' down-arrow and change 'New Virtual Machine' to something more useful, e.g. 'Ubuntu Server 18.04 LTS'.

1. Select 'Create Virtual Machine' and wait for the virtual machine to be created.

1. Select 'Connect' to open a connection to your VM.

1. Select 'File' in the menu bar, then
    -> Choose 'Settings' and select the 'Security' tab
    -> Under Secure Boot choose 'Microsoft UEFI Certificate Authority'
    -> Then select 'Apply' and 'OK' to return to your VM.

1. Select 'Start' to run your VM.

10. Complete the manual installation of Ubuntu.
