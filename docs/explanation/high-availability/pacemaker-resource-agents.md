(pacemaker-resource-agents)=
# Pacemaker resource agents


From the ClusterLabs definition:

> Resource agents are the abstraction that allows Pacemaker to manage services it knows nothing about. They contain the logic for what to do when the cluster wishes to start, stop or check the health of a service. This particular set of agents conform to the Open Cluster Framework (OCF) specification.

Currently, the `resource-agents` binary package has been split into two: `resource-agents-base` and `resource-agents-extra`. The `resource-agents-base` binary package contains a set of curated agents which the Ubuntu Server team continuously runs tests on to make sure everything is working as expected. All the other agents previously in the `resource-agents` binary package are now found in the `resource-agents-extra` package.

The `resource-agents-base` binary package contains the following agents in the latest Ubuntu release:

* `IPaddr2`
* `iscsi`
* `iSCSILogicalUnit`
* `iSCSITarget`
* `LVM-activate`
* `systemd`

All of these agents are in `main` and are fully supported.

All other agents are in `resource-agents-extra` and while most of them are supported by upstream, they are not curated by the Ubuntu Server team. The set of resource agents that are not maintained by upstream is listed in `/usr/share/doc/resource-agents-extra/DEPRECATED_AGENTS`, the use of those agents is discouraged.

For the resource agents provided by `resource-agents-base`, we will briefly describe how to use them.

```{note}
There are two well known tools used to manage fence agents, they are `crmsh` and `pcs`. Here we will present examples with both, since `crmsh` is the recommended and supported tool until Ubuntu 22.10 Kinetic Kudu, and `pcs` is the recommended and supported tool from Ubuntu 23.04 Lunar Lobster onwards. For more information on how to migrate from `crmsh` to `pcs` {ref}`refer to this migration guide <migrate-from-crmsh-to-pcs>`.
```

## IPaddr2

From its manual page:

> This Linux-specific resource manages IP alias IP addresses. It can add an IP alias, or remove one. In addition, it can implement Cluster Alias IP functionality if invoked as a clone resource.

One could configure a `IPaddr2` resource with the following command:

```
$ crm configure primitive $RESOURCE_NAME ocf:heartbeat:IPaddr2 \
            ip=$IP_ADDRESS \
            cidr_netmask=$NET_MASK \
            op monitor interval=30s
```

One can do the same using `pcs` via the following command:

```
$ pcs resource create $RESOURCE_NAME ocf:heartbeat:IPaddr2 \
            ip=$IP_ADDRESS \
            cidr_netmask=$NET_MASK \
            op monitor interval=30s
```

This is one way to set up `IPaddr2`, for more information refer {manpage}`to its manual page <ocf_heartbeat_IPaddr2(7)>`.

## iscsi

From its manual page:

> Manages a local iSCSI initiator and its connections to iSCSI targets.

Once the iSCSI target is ready to accept connections from the initiator(s), with all the appropriate permissions, the `iscsi` resource can be configured with the following command:

```
$ crm configure primitive $RESOURCE_NAME ocf:heartbeat:iscsi \
          target=$TARGET \
          portal=$PORTAL
```

One can do the same using `pcs` via the following command:

```
$ pcs resource create $RESOURCE_NAME ocf:heartbeat:iscsi \
          target=$TARGET \
          portal=$PORTAL
```

Where `$TARGET` is the iSCSI Qualified Name (IQN) of the iSCSI target and `$PORTAL` its address, which can be, for instance, formed by the IP address and port number used by the target daemon.

This is one way to set up `iscsi`, for more information refer {manpage}`to its manual page <ocf_heartbeat_iscsi(7)>`.

## iSCSILogicalUnit

From its manual page:

> Manages iSCSI Logical Unit. An iSCSI Logical unit is a subdivision of an SCSI Target, exported via a daemon that speaks the iSCSI protocol.

This agent is usually used alongside with `iSCSITarget` to manage the target itself and its Logical Units. The supported implementation of iSCSI targets is using `targetcli-fb`, due to that, make sure to use `lio-t` as the implementation type. Considering one has an iSCSI target in place, the `iSCSILogicalUnit` resource could be configured with the following command:

```
$ crm configure primitive $RESOURCE_NAME ocf:heartbeat:iSCSILogicalUnit \
          implementation=lio-t \
          target_iqn=$IQN_TARGET \
          path=$DEVICE \
          lun=$LUN
```

One can do the same using `pcs` via the following command:

```
$ pcs resource create $RESOURCE_NAME ocf:heartbeat:iSCSILogicalUnit \
          implementation=lio-t \
          target_iqn=$IQN_TARGET \
          path=$DEVICE \
          lun=$LUN
```

Where implementation is set to `lio-t` as mentioned before, `$IQN_TARGET` is the iSCSI Qualified Name (IQN) that this Logical Unit belongs to, `$DEVICE` is the path to the exposed block device, and `$LUN` is the number representing the Logical Unit which will be exposed to initiators.

This is one way to set up `iSCSILogicalUnit`, for more information refer {manpage}`to its manual page <ocf_heartbeat_iSCSILogicalUnit(7)>`.

## iSCSITarget

From its manual page:

> Manages iSCSI targets. An iSCSI target is a collection of SCSI Logical Units (LUs) exported via a daemon that speaks the iSCSI protocol.

This agent is usually used alongside with `iSCSILogicalUnit` to manage the target itself and its Logical Units. The supported implementation of iSCSI targets is using `targetcli-fb`, due to that, make sure to use `lio-t` as the implementation type. With `targetcli-fb` installed on the system, the `iSCSITarget` resource can be configured with the following command:

```
$ crm configure primitive $RESOURCE_NAME ocf:heartbeat:iSCSITarget \
          implementation=lio-t \
          iqn=$IQN_TARGET
```

One can do the same using `pcs` via the following command:

```
$ pcs resource create $RESOURCE_NAME ocf:heartbeat:iSCSITarget \
          implementation=lio-t \
          iqn=$IQN_TARGET
```

Where implementation is set to `lio-t` as mentioned before and `$IQN_TARGET` is the IQN of the target.

This is one way to set up `iSCSITarget`, for more information refer {manpage}`to its manual page <ocf_heartbeat_iSCSITarget(7)>`.

## LVM-activate

From its manual page:

> This agent manages LVM activation/deactivation work for a given volume group.

If the LVM setup is ready to be activated and deactivated by this resource agent (make sure the `system_id_resource` is set to `uname` in `/etc/lvm/lvm.conf`), the `LVM-activate` resource can be configured with the following command:

```bash
$ crm configure primitive $RESOURCE_NAME ocf:heartbeat:LVM-activate \
             vgname=$VOLUME_GROUP \
             vg_access_mode=system_id
```

One can do the same using `pcs` via the following command:

```
$ pcs resource create $RESOURCE_NAME ocf:heartbeat:LVM-activate \
             vgname=$VOLUME_GROUP \
             vg_access_mode=system_id
```

This is one way to set up `LVM-activate`, for more information refer {manpage}`to its manual page <ocf_heartbeat_LVM-activate(7)>`.

## Systemd

There is also a way to manage systemd unit files via a resource agent. One need to have the systemd unit file in place (already loaded by systemd) and configure a resource using the following command:

```
$ crm configure primitive $RESOURCE_NAME systemd:$SERVICE_NAME
```

One can do the same using `pcs` via the following command:

```
$ pcs resource create $RESOURCE_NAME systemd:$SERVICE_NAME
```

The `$SERVICE_NAME` can be any service managed by a systemd unit file, and it needs to be available for the cluster nodes.

## Further reading

* [ClusterLabs website](https://clusterlabs.org/)
* [The OCF resource-agent developer's guide](https://github.com/ClusterLabs/resource-agents/blob/master/doc/dev-guides/ra-dev-guide.asc)
