(introduction-to-multipath)=
# Introduction to device mapper multipathing ("multipath")

Device mapper multipathing (which will be called **multipath** in this document) allows you to create a virtual device that aggregrates multiple input/output (I/O) paths between server nodes and storage arrays. These I/O paths are physical storage area network (SAN) connections that can include separate cables, switches, and controllers.

## How a multipath device works in practice

If you are not using multipath, your system treats every path from a server node to a storage controller as a separate device, even when the I/O path connects the same server node to the same storage controller. Multipath allows you to organise the I/O paths logically, by creating a single device on top of the underlying paths.

## What identifier does a multipath device use?

Every multipath device has a World Wide Identifier (WWID), which is guaranteed to be globally unique and unchanging. By default, the name of a multipath device is set to its WWID. However, you can force multipath to give each multipath device a name that is a **node-unique alias** of the form `mpathn` by setting the `user_friendly_names` option in `multipath.conf`.

## What does multipath provide?

When you use multipath, it can provide:

- **Redundancy**
  Multipath provides {term}`failover` in an active/passive configuration. In an active/passive configuration, only half the paths are used at any time for I/O. If any element of an I/O path (the cable, switch, or controller) fails, multipath switches to an alternate path.

- **Improved performance**
  Multipath can be configured in active/active mode, where I/O is spread over the paths in a round-robin fashion. In some configurations, multipath can detect loading on the I/O paths and dynamically re-balance the load.

## Configuring multipath for a storage system

Before you decide to use multipath, check your storage vendor's installation guide for the multipath configuration variables that are recommended for your storage model. The default multipath configuration will probably work but will likely need adjustments based on your storage setup.

## Multipath components

| Component | Description |
| `dm_multipath` kernel module | Reroutes I/O and supports **failover** for paths and path groups. |
| `multipath command` | Lists and configures multipath devices. While this command is normally started up with `/etc/rc.sysinit`, it can also be started up by a `udev` program whenever a block device is added, or it can be run by the `initramfs` file system. |
| `multipathd` daemon | Monitors paths; as paths fail and come back, it may initiate path group switches. Provides for interactive changes to multipath devices. This daemon must be restarted for any changes to the `/etc/multipath.conf` file to take effect. |
| `kpartx` command | Creates device-mapper devices for the partitions on a device. It is necessary to use this command for DOS-based partitions with multipath. The `kpartx` is provided in its own package, but the `multipath-tools` package depends on it.  |

## Multipath setup overview

The multipath setup process is usually simple because it has compiled-in default settings that are suitable for common multipath configurations. The basic procedure for configuring your system with multipath is:

1.  Install the `multipath-tools` and `multipath-tools-boot` packages.

2.  Create an empty config file called `/etc/multipath.conf`.

3.  Edit the `multipath.conf` file to modify default values and save the updated file.

4.  Start the multipath daemon.

5.  Update initial RAM disk.

For detailed setup instructions for multipath configuration see {ref}`DM-Multipath configuration <configuring-multipath>` and {ref}`DM-Multipath setup <multipath-configuration-examples>`.

## Example of a multipath device in use

For example, a node with two host bus adapters (HBAs) attached to a storage controller, with two ports, via a single un-zoned {term}`FC` switch sees four devices:  `/dev/sda`, `/dev/sdb`, `/dev/sdc`, and `/dev/sdd`. If you use multipath with this node, a single multipath device is created with a unique WWID that reroutes I/O to those four underlying devices according to the multipath configuration.

When the `user_friendly_names` configuration option is set to 'yes', the name of the multipath device is set to `mpathn`. When new devices are brought under the control of multipath, the new devices may be seen in two different places under the `/dev` directory: `/dev/mapper/mpathn` and `/dev/dm-n`.

- The devices in `/dev/mapper` are created early in the boot process. **Use these devices to access the multipathed devices.**

- Any devices of the form `/dev/dm-n` are for **internal use only** and should never be used directly.

You can also set the name of a multipath device to a name of your choosing by using the `alias` option in the `multipaths` section of the multipath configuration file.

```{seealso}
For information on the multipath configuration defaults, including the `user_friendly_names` and `alias` configuration options, see {ref}`DM-Multipath configuration <configuring-multipath>`.
```

## Consistent multipath device names in a cluster

When the `user_friendly_names` configuration option is set to 'yes', the name of the multipath device is unique to a node, but it is not guaranteed to be the same on all nodes using the multipath device. Similarly, if you set the `alias` option for a device in the `multipaths` section of `/etc/multipath.conf`, the name is not automatically consistent across all nodes in the cluster.

This should not cause any difficulties if you {ref}`use LVM <manage-logical-volumes>` to create logical devices from the multipath device, but if you require that your multipath device names be consistent in every node it is recommended that you leave the `user_friendly_names` option set to 'no' and that you **do not** configure aliases for the devices.

If you configure an alias for a device that you would like to be consistent across the nodes in the cluster, you should ensure that the `/etc/multipath.conf` file is the same for each node in the cluster by following the same procedure:

1. Configure the aliases for the multipath devices in the in the `multipath.conf` file on one machine.

2. Disable all of your multipath devices on your other machines by running the following commands as root:

   ```bash
   systemctl stop multipath-tools.service
   multipath -F
   ```

3. Copy the `/etc/multipath.conf` file from the first machine to all other machines in the cluster.

4. Re-enable the `multipathd` daemon on all the other machines in the cluster by running the following command as root:

   ```bash
   systemctl start multipath-tools.service
   ```

Whenever you add a new device you will need to repeat this process.

## Multipath device attributes

In addition to the `user_friendly_names` and `alias` options, a multipath device has numerous attributes. You can modify these attributes for a specific multipath device by creating an entry for that device in the `multipaths` section of `/etc/multipath.conf`.

For information on the `multipaths` section of the multipath configuration file, see {ref}`DM-Multipath configuration <configuring-multipath>`.

## Multipath devices in logical volumes

After creating multipath devices, you can use the multipath device names just as you would use a physical device name when you are creating an LVM physical volume.

For example, if `/dev/mapper/mpatha` is the name of a multipath device, the following command (run as root) will mark `/dev/mapper/mpatha` as a physical volume:

```bash
pvcreate /dev/mapper/mpatha
```

You can use the resulting LVM physical device when you create an LVM volume group just as you would use any other LVM physical device.

```{note}
If you try to create an LVM physical volume on a whole device on which you have configured partitions, the `pvcreate` command will fail.
```

Once you create an LVM logical volume that has active/passive multipath arrays as the underlying physical devices, you must add filters in the `lvm.conf` file to exclude the disks that underlie the multipath devices. This is because if the array automatically changes the active path to the passive path when it receives I/O, multipath will failover and {term}`fallbacks` whenever LVM scans the passive path if these devices are not filtered.

If an active/passive array requires a command to activate the passive path, LVM will print a warning message. To filter all SCSI devices in the LVM configuration file (`lvm.conf`), include the following filter in the devices section of the file:

```text
filter = [ "r/block/", "r/disk/", "r/sd.*/", "a/.*/" ]
```

After updating `/etc/lvm.conf`, it's necessary to update the `initrd` so that this file will be copied there, where the filter matters the most -- during boot. Perform:

```bash
update-initramfs -u -k all
```

```{note}
Every time either `/etc/lvm.conf` or `/etc/multipath.conf` is updated, the `initrd` should be rebuilt to reflect these changes. This is imperative when {term}`denylists <denylist>` and filters are necessary to maintain a stable storage configuration.
```
