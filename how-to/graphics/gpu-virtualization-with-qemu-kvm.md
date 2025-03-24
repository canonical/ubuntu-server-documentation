(gpu-virtualization-with-qemu-kvm)=
# GPU virtualisation with QEMU/KVM

## Graphics

Graphics for QEMU/KVM always comes in two pieces: a {term}`frontend` and a backend.

- `frontend`: Controlled via the `-vga` argument, which is provided to the guest. Usually one of `cirrus`, `std`, `qxl`, or `virtio`. The default these days is `qxl` which strikes a good balance between guest compatibility and performance. The guest needs a driver for whichever option is selected -- this is the most common reason to not use the default (e.g., on very old Windows versions).

- `backend`: Controlled via the `-display` argument. This is what the host uses to actually display the graphical content, which can be an application window via `gtk` or a `vnc`.

- In addition, one can enable the `-spice` back end (which can be done in addition to `vnc`). This can be faster and provides more authentication methods than `vnc`.

- If you want no graphical output at all, you can save some memory and CPU cycles by setting `-nographic`.

If you run with `spice` or `vnc` you can use native `vnc` tools or virtualization-focused tools like `virt-viewer`. You can read more about these in the {ref}`libvirt section <libvirt>`.

All these options  are considered basic usage of graphics, but there are also advanced options for more specific use-cases. Those cases usually differ in their [ease-of-use and capability](https://cpaelzer.github.io/blogs/006-mediated-device-to-pass-parts-of-your-gpu-to-a-guest/), such as:

- *Need 3D acceleration*: Use `-vga virtio` with a local display having a {term}`GL` context `-display gtk,gl=on`. This will use [virgil3d](https://virgil3d.github.io/) on the host, and guest drivers are needed (which are common in Linux since [Kernels >= 4.4](https://www.kraxel.org/blog/2016/09/using-virtio-gpu-with-libvirt-and-spice/) but can be hard to come by for other cases). While not as fast as the next two options, the major benefit is that it can be used without additional hardware and without a proper input-output memory management unit (IOMMU) [set up for device passthrough](https://www.kernel.org/doc/Documentation/vfio-mediated-device.txt).

- *Need native performance*: Use PCI passthrough of additional {term}`GPUs` in the system. You'll need an IOMMU set up, and you'll need to unbind the cards from the host before you can pass it through, like so:

  ```bash
  -device vfio-pci,host=05:00.0,bus=1,addr=00.0,multifunction=on,x-vga=on -device vfio-pci,host=05:00.1,bus=1,addr=00.1
  ```

- *Need native performance, but multiple guests per card*: Like with PCI passthrough, but using mediated devices to shard a card on the host into multiple devices, then passing those:

  ```bash
  -display gtk,gl=on -device vfio-pci,sysfsdev=/sys/bus/pci/devices/0000:00:02.0/4dd511f6-ec08-11e8-b839-2f163ddee3b3,display=on,rombar=0
  ```

  You can read more [about vGPU at kraxel](https://www.kraxel.org/blog/2018/04/vgpu-display-support-finally-merged-upstream/) and [Ubuntu GPU mdev evaluation](https://cpaelzer.github.io/blogs/006-mediated-device-to-pass-parts-of-your-gpu-to-a-guest/). The sharding of the cards is driver-specific and therefore will differ per manufacturer -- [Intel](https://github.com/intel/gvt-linux/wiki/GVTg_Setup_Guide), [Nvidia](https://docs.nvidia.com/grid/latest/grid-vgpu-user-guide/index.html), or {term}`AMD`.

The advanced cases in particular can get pretty complex -- it is recommended to use QEMU through {ref}`libvirt section <libvirt>` for those cases. libvirt will take care of all but the host kernel/BIOS tasks of such configurations. Below are the common basic actions needed for faster options (i.e., passthrough and mediated devices passthrough).

The initial step for both options is the same; you want to ensure your system has its IOMMU enabled and the device to pass should be in a group of its own. Enabling the VT-d and IOMMU is usually a BIOS action and thereby manufacturer dependent.

## Preparing the input-output memory management unit (IOMMU)

On the kernel side, there are various [options you can enable/configure](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html?highlight=iommu) for the [IOMMU feature](https://www.kernel.org/doc/html/latest/arch/x86/iommu.html). In recent Ubuntu kernels (>=5.4 => Focal or Bionic-HWE kernels) everything usually works by default, unless your hardware setup makes you need any of those tuning options.

> **Note**:
> The card used in all examples below e.g. when filtering for or assigning PCI IDs, is an NVIDIA V100 on PCI ID 41.00.0
> $ lspci | grep 3D
41:00.0 3D controller: NVIDIA Corporation GV100GL [Tesla V100 PCIe 16GB] (rev a1)

You can check your boot-up kernel messages for IOMMU/{term}`DMAR` messages or even filter it for a particular PCI ID.

To list all:

```bash
dmesg | grep -i -e DMAR -e IOMMU
```

Which produces an output like this:

```text
[    3.509232] iommu: Default domain type: Translated
...
[    4.516995] pci 0000:00:01.0: Adding to iommu group 0
...
[    4.702729] perf/amd_iommu: Detected AMD IOMMU #0 (2 banks, 4 counters/bank).
```

To filter for the installed 3D card:

```bash
dmesg | grep -i -e DMAR -e IOMMU | grep $(lspci | awk '/ 3D / {print $1}' )
```

Which shows the following output:

```text
[    4.598150] pci 0000:41:00.0: Adding to iommu group 66
```

If you have a particular device and want to check for its group you can do that via `sysfs`. If you have multiple cards or want the full list you can traverse the same `sysfs` paths for that.

For example, to find the group for our example card:

```bash
find /sys/kernel/iommu_groups/ -name "*$(lspci | awk '/ 3D / {print $1}')*"
```

Which it tells us is found here:

```text
/sys/kernel/iommu_groups/66/devices/0000:41:00.0
```

We can also check if there are other devices in this group:

```
ll /sys/kernel/iommu_groups/66/devices/
lrwxrwxrwx 1 root root 0 Jan  3 06:57 0000:41:00.0 -> ../../../../devices/pci0000:40/0000:40:03.1/0000:41:00.0/
```

Another useful tool for this stage (although the details are beyond the scope of this article) can be `virsh node*`, especially `virsh nodedev-list --tree` and `virsh nodedev-dumpxml <pcidev>`.

> **Note**:
> Some older or non-server boards tend to group devices in one IOMMU group, which isn't very useful as it means you'll need to pass "all or none of them" to the same guest.

## Preparations for PCI and mediated devices pass-through -- block host drivers

For both, you'll want to ensure the normal driver isn't loaded. In some cases you can do that at runtime via `virsh nodedev-detach <pcidevice>`. `libvirt` will even do that automatically if, on the passthrough configuration, you have set `<hostdev mode='subsystem' type='pci' managed='yes'>`.

This usually works fine for e.g. network cards, but some other devices like GPUs do not like to be unassigned, so there the required step usually is block loading the drivers you do not want to be loaded. In our GPU example the `nouveau` driver would load and that has to be blocked. To do so you can create a `modprobe` blacklist.

```bash
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf          
echo "options nouveau modeset=0" | sudo tee -a /etc/modprobe.d/blacklist-nouveau.conf
sudo update-initramfs -u                                                         
sudo reboot                                                                      
```   

You can check which kernel modules are loaded and available via `lspci -v`:

```bash
lspci -v | grep -A 10 " 3D "
```

Which in our example shows:

```text
41:00.0 3D controller: NVIDIA Corporation GV100GL [Tesla V100 PCIe 16GB] (rev a1)
...
Kernel modules: nvidiafb, nouveau
```

If the configuration did not work instead it would show:

```text
Kernel driver in use: nouveau
```

## Preparations for mediated devices pass-through - driver

For PCI passthrough, the above steps would be all the preparation needed, but for mediated devices one also needs to install and set up the host driver. The example here continues with our NVIDIA V100 which is [supported and available from Nvidia](https://docs.nvidia.com/grid/latest/product-support-matrix/index.html#abstract__ubuntu).

There is also an Nvidia document about the same steps available on [installation and configuration of vGPU on Ubuntu](https://docs.nvidia.com/grid/latest/grid-vgpu-user-guide/index.html#ubuntu-install-configure-vgpu).

Once you have the drivers from Nvidia, like `nvidia-vgpu-ubuntu-470_470.68_amd64.deb`, then install them and check (as above) that that driver is loaded. The one you need to see is `nvidia_vgpu_vfio`:

```bash
lsmod | grep nvidia
```

Which we can see in the output:

```text
nvidia_vgpu_vfio       53248  38
nvidia              35282944  586 nvidia_vgpu_vfio
mdev                   24576  2 vfio_mdev,nvidia_vgpu_vfio
drm                   491520  6 drm_kms_helper,drm_vram_helper,nvidia
```

> **Note**:
> While it works without a vGPU manager, to get the full capabilities you'll need to configure the [vGPU manager (that came with above package)](https://docs.nvidia.com/grid/latest/grid-vgpu-user-guide/index.html#install-vgpu-package-ubuntu) and a license server so that each guest can get a license for the vGPU provided to it. Please see [Nvidia's documentation for the license server](https://docs.nvidia.com/grid/ls/latest/grid-license-server-user-guide/index.html). While not officially supported on Linux (as of Q1 2022), it's worthwhile to note that it runs fine on Ubuntu with `sudo apt install unzip default-jre tomcat9 liblog4j2-java libslf4j-java` using `/var/lib/tomcat9` as the server path in the license server installer.
>
> It's also worth mentioning that the Nvidia license server went [{term}`EOL` on 31 July 2023](https://docs.nvidia.com/grid/news/vgpu-software-license-server-eol-notice/index.html). At that time, it was replaced by the [NVIDIA License System](https://docs.nvidia.com/license-system/latest/nvidia-license-system-quick-start-guide/index.html).

Here is an example of those when running fine:
```text
# general status
$ systemctl status nvidia-vgpu-mgr
     Loaded: loaded (/lib/systemd/system/nvidia-vgpu-mgr.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2021-09-14 07:30:19 UTC; 3min 58s ago
    Process: 1559 ExecStart=/usr/bin/nvidia-vgpu-mgr (code=exited, status=0/SUCCESS)
   Main PID: 1564 (nvidia-vgpu-mgr)
      Tasks: 1 (limit: 309020)
     Memory: 1.1M
     CGroup: /system.slice/nvidia-vgpu-mgr.service
             └─1564 /usr/bin/nvidia-vgpu-mgr

Sep 14 07:30:19 node-watt systemd[1]: Starting NVIDIA vGPU Manager Daemon...
Sep 14 07:30:19 node-watt systemd[1]: Started NVIDIA vGPU Manager Daemon.
Sep 14 07:30:20 node-watt nvidia-vgpu-mgr[1564]: notice: vmiop_env_log: nvidia-vgpu-mgr daemon started

# Entries when a guest gets a vGPU passed
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: (0x0): gpu-pci-id : 0x4100
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: (0x0): vgpu_type : Quadro
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: (0x0): Framebuffer: 0x1dc000000
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: (0x0): Virtual Device Id: 0x1db4:0x1252
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: (0x0): FRL Value: 60 FPS
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: ######## vGPU Manager Information: ########
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: Driver Version: 470.68
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: (0x0): vGPU supported range: (0x70001, 0xb0001)
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: (0x0): Init frame copy engine: syncing...
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: (0x0): vGPU migration enabled
Sep 14 08:29:50 node-watt nvidia-vgpu-mgr[2866]: notice: vmiop_log: display_init inst: 0 successful

# Entries when a guest grabs a license
Sep 15 06:55:50 node-watt nvidia-vgpu-mgr[4260]: notice: vmiop_log: (0x0): vGPU license state: Unlicensed (Unrestricted)
Sep 15 06:55:52 node-watt nvidia-vgpu-mgr[4260]: notice: vmiop_log: (0x0): vGPU license state: Licensed

# In the guest the card is then fully recognized and enabled
$ nvidia-smi -a | grep -A 2 "Licensed Product"
    vGPU Software Licensed Product
        Product Name                      : NVIDIA RTX Virtual Workstation
        License Status                    : Licensed
```

A [mediated device](https://www.kernel.org/doc/html/latest/driver-api/vfio-mediated-device.html) is essentially the partitioning of a hardware device using {term}`firmware <FW>` and host driver features. This brings a lot of flexibility and options; in our example we can split our 16G GPU into 2x8G, 4x4G, 8x2G or 16x1G just as we need it. The following gives an example of how to split it into two 8G cards for a compute profile and pass those to guests.

Please refer to the [NVIDIA documentation](https://docs.nvidia.com/grid/latest/grid-vgpu-user-guide/index.html#ubuntu-install-configure-vgpu) for advanced tunings and different card profiles.

The tool for listing and configuring these mediated devices is `mdevctl`: 

```bash
sudo mdevctl types
```

Which will list the available types:

```text
...
  nvidia-300
    Available instances: 0
    Device API: vfio-pci
    Name: GRID V100-8C
    Description: num_heads=1, frl_config=60, framebuffer=8192M, max_resolution=4096x2160, max_instance=2
```

Knowing the PCI ID (`0000:41:00.0`) and the mediated device type we want (`nvidia-300`) we can now create those mediated devices:

```
$ sudo mdevctl define --parent 0000:41:00.0 --type nvidia-300
bc127e23-aaaa-4d06-a7aa-88db2dd538e0
$ sudo mdevctl define --parent 0000:41:00.0 --type nvidia-300
1360ce4b-2ed2-4f63-abb6-8cdb92100085
$ sudo mdevctl start --parent 0000:41:00.0 --uuid bc127e23-aaaa-4d06-a7aa-88db2dd538e0
$ sudo mdevctl start --parent 0000:41:00.0 --uuid 1360ce4b-2ed2-4f63-abb6-8cdb92100085
```

After that, you can check the UUID of your ready mediated devices:

```
$ sudo mdevctl list -d
bc127e23-aaaa-4d06-a7aa-88db2dd538e0 0000:41:00.0 nvidia-108 manual (active)
1360ce4b-2ed2-4f63-abb6-8cdb92100085 0000:41:00.0 nvidia-108 manual (active)
```

Those UUIDs can then be used to pass the mediated devices to the guest - which from here is rather similar to the pass through of a full PCI device.

## Passing through PCI or mediated devices

After the above setup is ready one can pass through those devices, in `libvirt` for a PCI passthrough that looks like:

```
<hostdev mode='subsystem' type='pci' managed='yes'>
  <source>
    <address domain='0x0000' bus='0x41' slot='0x00' function='0x0'/>
  </source>
</hostdev>
```

And for mediated devices it is quite similar, but using the UUID.

```
<hostdev mode='subsystem' type='mdev' managed='no' model='vfio-pci' display='on'>
  <source>
    <address uuid='634fc146-50a3-4960-ac30-f09e5cedc674'/>
  </source>
</hostdev>
```

Those sections can be [part of the guest definition](https://libvirt.org/formatdomain.html#usb-pci-scsi-devices) itself, to be added on guest startup and freed on guest shutdown. Or they can be in a file and used by for hot-add remove if the hardware device and its drivers support it `virsh attach-device`.

> **Note**:
> This works great on Focal, but `type='none'` as well as `display='off'` weren't available on Bionic. If this level of control is required one would need to consider using the [Ubuntu Cloud Archive](https://wiki.ubuntu.com/OpenStack/CloudArchive) or [Server-Backports](https://launchpad.net/~canonical-server/+archive/ubuntu/server-backports) for a newer stack of the virtualisation components.

And finally, it might be worth noting that while mediated devices are becoming more common and known for vGPU handling, they are a general infrastructure also used (for example) for [s390x vfio-ccw](https://www.kernel.org/doc/html/latest/s390/vfio-ccw.html).
