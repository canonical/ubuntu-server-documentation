(nvidia-drivers-installation)=
# NVIDIA drivers installation

This page shows how to install the NVIDIA drivers from the command line, using either the `ubuntu-drivers` tool (recommended), or APT.

## NVIDIA drivers releases

We package two types of NVIDIA drivers:

1. **Unified Driver Architecture (UDA)** drivers - which are recommended for the generic desktop use, and which you can also find [on the NVIDIA website](https://www.nvidia.com/en-us/drivers/unix/).

1. **Enterprise Ready Drivers** ({term}`ERD`) - which are recommended on servers and for computing tasks. Their packages can be recognised by the `-server` suffix. You can read more about these drivers [in the NVIDIA documentation](https://docs.nvidia.com/datacenter/tesla/index.html).

Additionally, we package the **NVIDIA Fabric Manager** and the **NVIDIA Switch Configuration and Query (NSCQ) Library**, which you will only need if you have NVswitch hardware. The Fabric Manager and NSCQ library are only available with the ERDs or `-server` driver versions.

## Check driver versions

To check the version of your currently running driver:

```bash
cat /proc/driver/nvidia/version
```

## The recommended way (ubuntu-drivers tool)

The `ubuntu-drivers` tool relies on the same logic as the "Additional Drivers" graphical tool, and allows more flexibility on desktops and on servers.

The `ubuntu-drivers` tool is recommended if your computer uses Secure Boot, since it always tries to install signed drivers which are known to work with Secure Boot.

### Check the available drivers for your hardware

For desktop:

```bash
sudo ubuntu-drivers list
```

or, for servers:

```bash
sudo ubuntu-drivers list --gpgpu
```

You should see a list such as the following:

```text
nvidia-driver-470
nvidia-driver-470-server
nvidia-driver-535
nvidia-driver-535-open
nvidia-driver-535-server
nvidia-driver-535-server-open
nvidia-driver-550
nvidia-driver-550-open
nvidia-driver-550-server
nvidia-driver-550-server-open
```

### Installing the drivers for generic use (e.g. desktop and gaming)

You can either rely on automatic detection, which will install the driver that is considered the best match for your hardware:

```bash
sudo ubuntu-drivers install
```

Or you can tell the `ubuntu-drivers` tool which driver you would like installed. If this is the case, you will have to use the driver version (such as `535`) that you saw when you used the `ubuntu-drivers list` command.

Let's assume we want to install the `535` driver:

```bash
sudo ubuntu-drivers install nvidia:535
```

### Installing the drivers on servers and/or for computing purposes

You can either rely on automatic detection, which will install the driver that is considered the best match for your hardware:

```bash
sudo ubuntu-drivers install --gpgpu
```

Or you can tell the `ubuntu-drivers` tool which driver you would like installed. If this is the case, you will have to use the driver version (such as `535`) and the `-server` suffix that you saw when you used the `ubuntu-drivers list --gpgpu` command.

Let's assume we want to install the `535-server` driver (listed as `nvidia-driver-535-server`):

```bash
sudo ubuntu-drivers install --gpgpu nvidia:535-server
```

You will also want to install the following additional components:

```bash
sudo apt install nvidia-utils-535-server
```

#### Optional step

If your system comes with NVswitch hardware, then you will want to install Fabric Manager and the NVSwitch Configuration and Query library. You can do so by running the following:
```bash
sudo apt install nvidia-fabricmanager-535 libnvidia-nscq-535
```

> **Note**:
> While `nvidia-fabricmanager` and `libnvidia-nscq` do not have the same `-server` label in their name, they are really meant to match the `-server` drivers in the Ubuntu archive. For example, `nvidia-fabricmanager-535` will match the `nvidia-driver-535-server` package version (not the `nvidia-driver-535 package`).

<h2 id="heading--manual-driver-installation-using-apt">
Manual driver installation (using APT)
</h2>

Installing the NVIDIA driver manually means installing the correct kernel modules first, then installing the metapackage for the driver series.

### Installing the kernel modules

If your system uses Secure Boot (as most x86 modern systems do), your kernel will require the kernel modules to be signed. There are two (mutually exclusive) ways to achieve this.

#### Installing the pre-compiled NVIDIA modules for your kernel

Install the metapackage for your kernel flavour (e.g. `generic`, `lowlatency`, etc) which is specific to the driver branch (e.g. `535`) that you want to install, and whether you want the compute vs. general display driver (e.g. `-server` or not):

```bash
sudo apt install linux-modules-nvidia-${DRIVER_BRANCH}${SERVER}-${LINUX_FLAVOUR}
```

(e.g. `linux-modules-nvidia-535-generic`)

Check that the modules for your specific kernel/ABI were installed by the metapackage:

```bash
sudo apt-cache policy linux-modules-nvidia-${DRIVER_BRANCH}${SERVER}-$(uname -r)
```

(e.g. `sudo apt-cache policy linux-modules-nvidia-535-$(uname -r)`)

If the modules were not installed for your current running kernel, upgrade to the latest kernel or install them by specifying the running kernel version:

```bash
sudo apt install linux-modules-nvidia-${DRIVER_BRANCH}${SERVER}-$(uname -r)
```

(e.g. `sudo apt install linux-modules-nvidia-535-$(uname -r)`)

#### Building your own kernel modules using the NVIDIA DKMS package

Install the relevant NVIDIA {term}`DKMS` package and `linux-headers` to build the kernel modules, and enroll your own key to sign the modules.

Install the `linux-headers` metapackage for your kernel flavour (e.g. `generic`, `lowlatency`, etc):

```bash
sudo apt install linux-headers-${LINUX_FLAVOUR}
```

Check that the headers for your specific kernel were installed by the metapackage:

```bash
sudo apt-cache policy linux-headers-$(uname -r)
```

If the headers for your current running kernel were not installed, install them by specifying the running kernel version:

```bash
sudo apt install linux-headers-$(uname -r)
```

Finally, install the NVIDIA DKMS package for your desired driver series (this may automatically guide you through creating and enrolling a new key for Secure Boot):

```bash
sudo apt install nvidia-dkms-${DRIVER_BRANCH}${SERVER}
```

### Installing the user-space drivers and the driver libraries

After installing the correct kernel modules (see the relevant section of this document), install the correct driver metapackage:

```bash
sudo apt install nvidia-driver-${DRIVER_BRANCH}${SERVER}
```

#### (Optional) Installing Fabric Manager and the NSCQ library

If your system comes with NVswitch hardware, then you will want to install Fabric Manager and the NVSwitch Configuration and Query library. You can do so by running the following:

```bash
sudo apt install nvidia-fabricmanager-${DRIVER_BRANCH} libnvidia-nscq-${DRIVER_BRANCH}
```

> **Note**:
> While `nvidia-fabricmanager` and `libnvidia-nscq` do not have the same `-server` label in their name, they are really meant to match the `-server` drivers in the Ubuntu archive. For example, `nvidia-fabricmanager-535` will match the `nvidia-driver-535-server` package version (not the `nvidia-driver-535` package).

## Switching between pre-compiled and DKMS modules

1. Uninstalling the NVIDIA drivers (below)

2. <a href="#heading--manual-driver-installation-using-apt"> Manual driver installation using APT </a>

### Uninstalling the NVIDIA drivers

Remove any NVIDIA packages from your system:

```bash
sudo apt --purge remove '*nvidia*${DRIVER_BRANCH}*'
```

Remove any additional packages that may have been installed as a dependency (e.g. the `i386` libraries on amd64 systems) and which were not caught by the previous command:

```bash
sudo apt autoremove
```

## Transitional packages to new driver branches

When NVIDIA stops support on a driver branch, then Canonical will transition you to the next supported driver branch automatically if you try to install that driver branch.

See NVIDIA's [current support matrix](https://docs.nvidia.com/datacenter/tesla/drivers/index.html#branches) in their documentation.
