(about-logical-volume-management-lvm)=
# About LVM

[Logical Volume Management](https://en.wikipedia.org/wiki/Logical_volume_management), or LVM, provides a method of allocating and managing space on mass-storage devices that is more advanced and flexible than the traditional method of partitioning storage volumes.

To find out how to set up LVM in Ubuntu, [refer to this guide](../how-to/how-to-manage-logical-volumes.md), which will also show you how to resize and move partitions, and how to create snapshots.

## Key concepts

There are 3 concepts that LVM manages:

* **Physical volumes**: correspond to disks. They represent the lowest abstraction level of LVM, and are used to create a volume group.
* **Volume groups**: are collections of physical volumes. They are pools of disk space that logical volumes can be allocated from.
* **Logical volumes**: correspond to partitions – they usually hold a filesystem. Unlike partitions though, they can span multiple disks (because of the way volume groups are organised) and do not have to be physically contiguous.

## Resizing partitions

LVM can expand a partition while it is mounted, if the filesystem used on it also supports that. When expanding a partition, LVM can use free space anywhere in the volume group, even on another disk.

When resizing LVM partitions, and especially when shrinking them, it is important to take the same precautions you would as if you were dealing with regular partitions. Namely, always make a backup of your data before actually executing the commands. Although LVM will try hard to determine whether a partition can be expanded or shrunk before actually performing the operation, there is always the possibility of data loss.

## Moving Partitions

Moving regular partitions is usually only necessary because of the requirement that partitions be physically contiguous, so you probably will not need to do this with LVM. If you do, LVM can move a partition while it is in use, and will not corrupt your data if it is interrupted. In the event that your system crashes or loses power during the move, you can simply restart it after rebooting and it will finish normally. Another reason you might want to move an LVM partition is to replace an old disk with a new, larger one. You can migrate the system to the new disk while using it, and then remove the old one later.

## Snapshots

LVM allows you to freeze an existing logical volume in time, at any moment, even while the system is running. You can continue to use the original volume normally, but the snapshot volume appears to be an image of the original, frozen in time at the moment you created it. You can use this to get a consistent filesystem image to back up, without shutting down the system. You can also use it to save the state of the system, so that you can later return to that state if needed. You can also mount the snapshot volume and make changes to it, without affecting the original.
