(common-multipath-tasks-and-procedures)=
# Common multipath tasks and procedures

This section shows examples of common configuration procedures and tasks. Before moving on with this section it's a good idea to read or be familiar with the topics in these pages:

1. [Introduction to device mapper multipathing](introduction-to-device-mapper-multipathing.md)
2. [Configuration options and overview](configuring-device-mapper-multipathing.md)
3. [Configuration examples](multipath-configuration-examples.md)

For consistency, we will refer to device mapper multipathing as **multipath**.

## Resizing online multipath devices

To resize online multipath devices, first find all the paths to the logical unit number (LUN) that is to be resized by running the following command:

```bash
$ sudo multipath -ll

mpathb (360014056eee8ec6e1164fcb959086482) dm-0 LIO-ORG,lun01
size=1.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 7:0:0:1 sde 8:64 active ready running
`-+- policy='service-time 0' prio=50 status=enabled
  `- 8:0:0:1 sdf 8:80 active ready running
mpatha (36001405e3c2841430ee4bf3871b1998b) dm-1 LIO-ORG,lun02
size=1.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 7:0:0:2 sdc 8:32 active ready running
`-+- policy='service-time 0' prio=50 status=enabled
  `- 8:0:0:2 sdd 8:48 active ready running
```

Now, reconfigure `mpathb` (with `wwid = 360014056eee8ec6e1164fcb959086482`) to have 2 GB instead of just 1 GB and check if it has changed:

```bash
$ echo 1 | sudo tee /sys/block/sde/device/rescan

1

$ echo 1 | sudo tee /sys/block/sdf/device/rescan

1

$ sudo multipath -ll

mpathb (360014056eee8ec6e1164fcb959086482) dm-0 LIO-ORG,lun01
size=1.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 7:0:0:1 sde 8:64 active ready running
`-+- policy='service-time 0' prio=50 status=enabled
  `- 8:0:0:1 sdf 8:80 active ready running
mpatha (36001405e3c2841430ee4bf3871b1998b) dm-1 LIO-ORG,lun02
size=1.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 7:0:0:2 sdc 8:32 active ready running
`-+- policy='service-time 0' prio=50 status=enabled
  `- 8:0:0:2 sdd 8:48 active ready running
```

Not yet! We still need to re-scan the multipath map:

```bash
$ sudo multipathd resize map mpathb

ok
```

And then we are good:

```bash
$ sudo multipath -ll

mpathb (360014056eee8ec6e1164fcb959086482) dm-0 LIO-ORG,lun01
size=2.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 7:0:0:1 sde 8:64 active ready running
.`-+- policy='service-time 0' prio=50 status=enabled
  `- 8:0:0:1 sdf 8:80 active ready running
mpatha (36001405e3c2841430ee4bf3871b1998b) dm-1 LIO-ORG,lun02
size=1.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 7:0:0:2 sdc 8:32 active ready running
`-+- policy='service-time 0' prio=50 status=enabled
  `- 8:0:0:2 sdd 8:48 active ready running
```

Make sure to run `resize2fs /dev/mapper/mpathb` to resize the filesystem.

## Move root file system from a single path device to a multipath device

This is greatly simplified by the use of UUIDs to identify devices with an intrinsic label. To do this, install `multipath-tools-boot` and reboot your system. This will rebuild the initial RAM disk and afford multipath the opportunity to build its paths before the root filesystem is mounted by UUID.

> **Note**:
> Whenever `multipath.conf` is updated, initrd should be updated as well by running:  
> `update-initramfs -u -k all`   
> The reason for this is that `multipath.conf` is copied to the RAM disk, and is integral to determining the available devices to map via its `denylist` and `devices` sections. 

## The multipathd daemon

If you have trouble implementing a multipath configuration, you should ensure the multipath daemon is running as described in [the example configuration page](multipath-configuration-examples.md). The `multipathd` daemon must be running in order to use multipath devices. 

## Multipath command output

When you create, modify, or list a multipath device, you get a printout of the current device setup. The format is as follows for each multipath device:

```text
action_if_any: alias (wwid_if_different_from_alias) dm_device_name_if_known vendor,product
   size=size features='features' hwhandler='hardware_handler' wp=write_permission_if_known
```

For each path group:
```text
  -+- policy='scheduling_policy' prio=prio_if_known
  status=path_group_status_if_known
```

For each path:
```text
   `- host:channel:id:lun devnode major:minor dm_status_if_known path_status
  online_status
```

For example, the output of a multipath command might appear as follows:

```text
mpathb (360014056eee8ec6e1164fcb959086482) dm-0 LIO-ORG,lun01
size=2.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 7:0:0:1 sde 8:64 active ready running
`-+- policy='service-time 0' prio=50 status=enabled
  `- 8:0:0:1 sdf 8:80 active ready running
```

If the path is up and ready for I/O, the status of the path is `ready` or `ghost`. If the path is down, the status is `faulty` or `shaky`. The path status is updated periodically by the `multipathd` daemon based on the **polling interval** defined in the `/etc/multipath.conf`  file.

The `dm_status` is similar to the `path` status, but from the kernel’s point of view. The `dm_status` has two states: **`failed`**, which is analogous to `faulty`, and **`active`**, which covers all other path states. Occasionally, the `path` state and the `dm` state of a device will temporary not agree.

The possible values for `online_status` are **`running`** and **`offline`**. A status of `offline` means that the SCSI device has been disabled.

## Multipath queries with the multipath command

You can use the `-l` and `-ll` options of the `multipath` command to display the current multipath configuration. 

- **`-l`** : Displays multipath topology gathered from information in `sysfs` and the device mapper 
- **`-ll`** : Displays the information the `-l` displays in addition to all other available components of the system

When displaying the multipath configuration, there are three verbosity levels you can specify with the `-v` option of the `multipath` command:
- **`-v0`** : Yields no output
- **`-v1`** : Outputs only the created or updated multipath names, which you can then feed to other tools such as `kpartx`
- **`-v2`** : Prints all detected paths, multipaths, and device maps

> **Note**:
> The default verbosity level of multipath is 2 and can be globally modified by defining the verbosity attribute in the `defaults` section of `multipath.conf`

The following example shows the output of a `sudo multipath -l` command:

```text
mpathb (360014056eee8ec6e1164fcb959086482) dm-0 LIO-ORG,lun01
size=2.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=0 status=active
| `- 7:0:0:1 sde 8:64 active undef running
`-+- policy='service-time 0' prio=0 status=enabled
  `- 8:0:0:1 sdf 8:80 active undef running
mpatha (36001405e3c2841430ee4bf3871b1998b) dm-1 LIO-ORG,lun02
size=1.0G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=0 status=active
| `- 7:0:0:2 sdc 8:32 active undef running
`-+- policy='service-time 0' prio=0 status=enabled
  `- 8:0:0:2 sdd 8:48 active undef running
```

## Determining device mapper entries with dmsetup

You can use the `dmsetup` command to find out which device mapper entries match the multipathed devices. The following command displays all the device mapper devices and their major and minor numbers. The minor numbers determine the name of the **dm** device. For example, a minor number of 1 corresponds to the `multipathd` device `/dev/dm-1`.

```bash
$ sudo dmsetup ls
mpathb  (253:0)
mpatha  (253:1)

$ ls -lahd /dev/dm*
brw-rw---- 1 root disk 253, 0 Apr 27 14:49 /dev/dm-0
brw-rw---- 1 root disk 253, 1 Apr 27 14:47 /dev/dm-1
```

## Troubleshooting with the multipathd interactive console

The `multipathd -k` command is an interactive interface to the `multipathd` daemon. Running this command brings up an interactive multipath console where you can enter `help` to get a list of available commands, you can enter an interactive command, or you can enter <kbd>Ctrl</kbd>+<kbd>D</kbd> to quit.

The `multipathd` interactive console can be used to troubleshoot problems with your system. For example, the following command sequence displays the multipath configuration, including the defaults, before exiting the console. 

```bash
$ sudo multipathd -k
  > show config
  > CTRL-D
```

The following command sequence ensures that multipath has picked up any changes to the `multipath.conf`:

```bash
$ sudo multipathd -k
> reconfigure
> CTRL-D
```

Use the following command sequence to ensure that the path checker is working properly:

```bash
$ sudo multipathd -k
> show paths
> CTRL-D
```

Commands can also be streamed into `multipathd` using STDIN like so:

```bash
$ echo 'show config' | sudo multipathd -k
```
