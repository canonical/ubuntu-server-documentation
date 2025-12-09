---
myst:
  html_meta:
    description: "Learn about Pacemaker fence agents for managing node fencing in high-availability clusters on Ubuntu Server."
---

(pacemaker-fence-agents)=
# Pacemaker fence agents


From the ClusterLabs definition:

> A **fence agent** (or **fencing agent**) is a **stonith**-class resource agent.
>
> The fence agent standard provides commands (such as `off` and `reboot`) that the cluster can use to fence nodes. As with other resource agent classes, this allows a layer of abstraction so that Pacemaker doesn’t need any knowledge about specific fencing technologies — that knowledge is isolated in the agent.

Currently, the `fence-agents` binary package has been split into two: `fence-agents-base` and `fence-agents-extra`. The `fence-agents-base` binary package contains a set of curated agents which the Ubuntu Server team continuously runs tests on to make sure everything is working as expected. All the other agents previously in the `fence-agents` binary package are now moved to the `fence-agents-extra`.

The `fence-agents-base` binary package contains the following agents in the latest Ubuntu release:

* `fence_ipmilan`
  * `fence_idrac`
  * `fence_ilo3`
  * `fence_ilo4`
  * `fence_ilo5`
  * `fence_imm`
  * `fence_ipmilanplus`
* `fence_mpath`
* `fence_sbd`
* `fence_scsi`
* `fence_virsh`

All of these agents are in `main` and are fully supported. All other agents, in `fence-agents-extra`, are supported by upstream but are not curated by the Ubuntu Server team.

For the fence agents provided by `fence-agents-base`, we will briefly describe how to use them.

```{note}
There are two well known tools used to manage fence agents, they are `crmsh` and `pcs`. Here we present examples with both, since `crmsh` is the recommended and supported tool until Ubuntu 22.10 Kinetic Kudu, and `pcs` is the recommended and supported tool from Ubuntu 23.04 Lunar Lobster onwards. For more information on how to migrate from `crmsh` to `pcs` {ref}`refer to our migration guide <migrate-from-crmsh-to-pcs>`.
```

## `fence_ipmilan`

The content of this section is also applicable to the following fence agents: `fence_idrac`, `fence_ilo3`, `fence_ilo4`, `fence_ilo5`, `fence_imm`, and `fence_ipmilanplus`. All of them are symlinks to `fence_ipmilan`.

From its manual page:

> `fence_ipmilan` is an I/O Fencing agent which can be used with machines controlled by IPMI. This agent calls support software `ipmitool`. WARNING! This fence agent might report success before the node is powered off. You should use `-m/method onoff` if your fence device works correctly with that option.

In a system which supports IPMI and with `ipmitool` installed, a `fence_ipmilan` resource can be configured with the following command:

```
$ crm configure primitive $RESOURCE_NAME stonith:fence_ipmilan \
            ip=$IP \
            ipport=$PORT \
            username=$USER \
            password=$PASSWD \
            lanplus=1 \
            action=$ACTION
```

One can do the same using `pcs` via the following command:

```
$ pcs stonith create $RESOURCE_NAME fence_ipmilan \
            ip=$IP \
            ipport=$PORT \
            username=$USER \
            password=$PASSWD \
            lanplus=1 \
            action=$ACTION
```

Where `$IP` is the IP address or {term}`hostname` of fencing device, `$PORT` is the TCP/UDP port to use for connection, `$USER` is the login name and `$PASSWD` its password, and `$ACTION` is the fencing actions which by default is `reboot`.

This is one way to set up `fence_ipmilan`, for more information refer {manpage}`to its manual page <fence_ipmilan(8)>`.

## `fence_mpath`

From its manual page:

>`fence_mpath` is an I/O fencing agent that uses SCSI-3 persistent reservations to control access multipath devices. Underlying devices must support SCSI-3 persistent reservations (SPC-3 or greater) as well as the "preempt-and-abort" subcommand. The `fence_mpath` agent works by having a unique key for each node that has to be set in `/etc/multipath.conf`. Once registered, a single node will become the reservation holder by creating a "write exclusive, registrants only" reservation on the device(s). The result is that only registered nodes may write to the device(s). When a node failure occurs, the `fence_mpath` agent will remove the key belonging to the failed node from the device(s). The failed node will no longer be able to write to the device(s). A manual reboot is required.

One can configure a `fence_mpath` resource with the following command:

```
$ crm configure primitive $RESOURCE_NAME stonith:fence_mpath \
            pcmk_host_map="$NODE1:$NODE1_RES_KEY;$NODE2:$NODE2_RES_KEY;$NODE3:$NODE3_RES_KEY" \
            pcmk_host_argument=key \
            pcmk_monitor_action=metadata \
            pcmk_reboot_action=off \
            devices=$MPATH_DEVICE \
            meta provides=unfencing
```

One can do the same using `pcs` via the following command:

```
$ pcs stonith create $RESOURCE_NAME fence_mpath \
            pcmk_host_map="$NODE1:$NODE1_RES_KEY;$NODE2:$NODE2_RES_KEY;$NODE3:$NODE3_RES_KEY" \
            pcmk_host_argument=key \
            pcmk_monitor_action=metadata \
            pcmk_reboot_action=off \
            devices=$MPATH_DEVICE \
            meta provides=unfencing
```

The `$NODE1_RES_KEY` is the reservation key used by this node 1 (same for the others node with access to the multipath device), please make sure you have `reservation_key <key>` in the `default` section inside `/etc/multipath.conf` and the multipathed service was reloaded after it.

This is one way to set up `fence_mpath`, for more information please check its manual page.

## `fence_sbd`

From its manual page:

> `fence_sbd` is I/O Fencing agent which can be used in environments where SBD can be used (shared storage).

With STONITH Block Device (SBD) configured on a system, the `fence_sbd` resource can be configured with the following command:

```
$ crm configure primitive $RESOURCE_NAME stonith:fence_sbd devices=$DEVICE
```

One can do the same using `pcs` via the following command:

```
$ pcs stonith create $RESOURCE_NAME fence_sbd devices=$DEVICE
```

This is one way to set up `fence_sbd`, for more information refer {manpage}`to its manual page <fence_sbd(8)>`.

## `fence_scsi`

From its manual page:

>`fence_scsi` is an I/O fencing agent that uses SCSI-3 persistent reservations to control access to shared storage devices. These devices must support SCSI-3 persistent reservations (SPC-3 or greater) as well as the "preempt-and-abort" subcommand. The `fence_scsi` agent works by having each node in the cluster register a unique key with the SCSI device(s). Reservation key is generated from "node id" (default) or from "node name hash" (RECOMMENDED) by adjusting "key_value" option. Using hash is recommended to prevent issues when removing nodes from cluster without full cluster restart. Once registered, a single node will become the reservation holder by creating a "write exclusive, registrants only" reservation on the device(s). The result is that only registered nodes may write to the device(s). When a node failure occurs, the `fence_scsi` agent will remove the key belonging to the failed node from the device(s). The failed node will no longer be able to write to the device(s). A manual reboot is required.

A `fence_scsi` resource can be configured with the following command:

```
$ crm configure primitive $RESOURCE_NAME stonith:fence_scsi \
            pcmk_host_list="$NODE1 $NODE2 $NODE3" \
            devices=$SCSI_DEVICE \
            meta provides=unfencing
```

One can do the same using `pcs` via the following command:

```
$ pcs stonith create $RESOURCE_NAME fence_scsi \
            pcmk_host_list="$NODE1 $NODE2 $NODE3" \
            devices=$SCSI_DEVICE \
            meta provides=unfencing
```

The `pcmk_host_list` parameter contains a list of cluster nodes that can access the managed SCSI device.

This is one way to set up `fence_scsi`, for more information refer {manpage}`to its manual page <fence_scsi(8)>`.

## `fence_virsh`

From its manual page:

>`fence_virsh` is an I/O Fencing agent which can be used with the virtual machines managed by libvirt. It logs via SSH to a dom0 and there run `virsh` command, which does all work. By default, `virsh` needs root account to do properly work. So you must allow SSH login in your `sshd_config`.

A `fence_virsh` resource can be configured with the following command:

```
$ crm configure primitive $RESOURCE_NAME stonith:fence_virsh \
            ip=$HOST_IP_ADDRESS \
            login=$HOST_USER \
            identity_file=$SSH_KEY \
            plug=$NODE \
            ssh=true \
            use_sudo=true
```

One can do the same using `pcs` via the following command:

```
$ pcs stonith create $RESOURCE_NAME fence_virsh \
            ip=$HOST_IP_ADDRESS \
            login=$HOST_USER \
            identity_file=$SSH_KEY \
            plug=$NODE \
            ssh=true \
            use_sudo=true
```

This is one way to set up `fence_virsh`, for more information refer {manpage}`to its manual page <fence_virsh(8)>`.

In order to avoid running the resource in the same node that should be fenced, we need to add a location restriction:

```
$ crm configure location fence-$NODE-location $RESOURCE_NAME -inf: $NODE
```

Using `pcs`:

```
$ pcs constraint location $RESOURCE_NAME avoids $NODE
```

## Further reading

* [ClusterLabs website](https://clusterlabs.org/)
* [Fence agents API documentation](https://github.com/ClusterLabs/fence-agents/blob/master/doc/FenceAgentAPI.md)
