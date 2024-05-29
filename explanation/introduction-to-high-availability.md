# Introduction to High Availability


A definition of High Availability Clusters [from Wikipedia:](https://en.wikipedia.org/wiki/High-availability_cluster)

## High Availability Clusters

> **High-availability clusters**  (also known as  **HA clusters**  ,  **failover clusters**  or  **Metroclusters Active/Active** ) are groups of [computers](https://en.wikipedia.org/wiki/Computer) that support [server](https://en.wikipedia.org/wiki/Server_(computing)) [applications](https://en.wikipedia.org/wiki/Application_software) that can be reliably utilised with [a minimum amount of down-time](https://en.wikipedia.org/wiki/High_availability).<P>They operate by using [high availability software](https://en.wikipedia.org/wiki/High_availability_software) to harness [redundant](https://en.wikipedia.org/wiki/Redundancy_(engineering)) computers in groups or [clusters](https://en.wikipedia.org/wiki/Computer_cluster) that provide continued service when system components fail. <P>Without clustering, if a server running a particular application crashes, the application will be unavailable until the crashed server is fixed. HA clustering remedies this situation by detecting hardware/software faults, and immediately restarting the application on another system without requiring administrative intervention, a process known as [failover](https://en.wikipedia.org/wiki/Failover). <P>As part of this process, clustering software may configure the node before starting the application on it. For example, appropriate file systems may need to be imported and mounted, network hardware may have to be configured, and some supporting applications may need to be running as well.
>
>HA clusters are often used for critical [databases](https://en.wikipedia.org/wiki/Database_management_system), file sharing on a network, business applications, and customer services such as [electronic commerce](https://en.wikipedia.org/wiki/Electronic_commerce) [websites](https://en.wikipedia.org/wiki/Websites).

## High Availability cluster heartbeat

>HA cluster implementations attempt to build redundancy into a cluster to eliminate single points of failure, including multiple network connections and data storage which is redundantly connected via [storage area networks](https://en.wikipedia.org/wiki/Storage_area_network).
>
>HA clusters usually use a [heartbeat](https://en.wikipedia.org/wiki/Heartbeat_(computing)) private network connection which is used to monitor the health and status of each node in the cluster. One subtle but serious condition all clustering software must be able to handle is [split-brain](https://en.wikipedia.org/wiki/Split-brain_(computing)), which occurs when all of the private links go down simultaneously, but the cluster nodes are still running. <P>If that happens, each node in the cluster may mistakenly decide that every other node has gone down and attempt to start services that other nodes are still running. Having duplicate instances of services may cause data corruption on the shared storage.

## High Availability Cluster Quorum

> HA clusters often also use [quorum](https://en.wikipedia.org/wiki/Quorum_(distributed_computing)) witness storage (local or cloud) to avoid this scenario. A witness device cannot be shared between two halves of a split cluster, so in the event that all cluster members cannot communicate with each other (e.g., failed heartbeat), if a member cannot access the witness, it cannot become active.

### Example

![2-node HA cluster|578x674,75%](https://assets.ubuntu.com/v1/14896401-HA_intro.png)

## Fencing

Fencing protects your data from being corrupted, and your application from becoming unavailable, due to unintended concurrent access by rogue nodes.

Just because a node is unresponsive doesn’t mean it has stopped accessing your data. The only way to be 100% sure that your data is safe, is to use fencing to ensure that the node is truly offline before allowing the data to be accessed from another node.

Fencing also has a role to play in the event that a clustered service cannot be stopped. In this case, the cluster uses fencing to force the whole node offline, thereby making it safe to start the service
elsewhere. The most popular example of fencing is cutting a host’s power.

Key Benefits:

- Active counter-measure taken by a functioning host to isolate a misbehaving (usually dead) host from shared data.

- **MOST CRITICAL** part of a cluster utilising SAN or other shared storage technology (*Ubuntu HA Clusters can only be supported if the fencing mechanism is configured*).

- Required by OCFS2, GFS2, cLVMd (before Ubuntu 20.04), lvmlockd (from 20.04 and beyond).

## Linux High Availability Projects

There are many upstream high availability related projects that are included in Ubuntu Linux. This section will describe the most important ones.

The following packages are present in latest Ubuntu LTS release:

### Ubuntu HA Core Packages

Packages in this list are supported just like any other package available in  **[main] repository**  would be.

| Package | URL |
|-|-|
| `libqb` | [Ubuntu](https://launchpad.net/ubuntu/+source/libqb) \| [Upstream](http://clusterlabs.github.io/libqb/)
| `kronosnet` | [Ubuntu](https://launchpad.net/ubuntu/+source/kronosnet) \| [Upstream](https://kronosnet.org/)
| `corosync` | [Ubuntu](https://launchpad.net/ubuntu/+source/corosync) \| [Upstream](http://corosync.github.io/corosync/)
| `pacemaker` | [Ubuntu](https://launchpad.net/ubuntu/+source/pacemaker) \| [Upstream](https://www.clusterlabs.org/pacemaker/)
| `resource-agents` |[Ubuntu](https://launchpad.net/ubuntu/+source/resource-agents) \| [Upstream](https://github.com/ClusterLabs/resource-agents)
| `fence-agents` |[Ubuntu](https://launchpad.net/ubuntu/+source/fence-agents) \| [Upstream](https://github.com/ClusterLabs/fence-agents)
| `crmsh` |[Ubuntu](https://launchpad.net/ubuntu/+source/crmsh) \| [Upstream](https://github.com/ClusterLabs/crmsh)
| `pcs*` |[Ubuntu](https://launchpad.net/ubuntu/+source/pcs) \| [Upstream](https://github.com/ClusterLabs/pcs/)
| `cluster-glue` |[Ubuntu](https://launchpad.net/ubuntu/+source/cluster-glue) \| [Upstream](https://github.com/ClusterLabs/cluster-glue)
| `drbd-utils` |[Ubuntu](https://launchpad.net/ubuntu/+source/drbd-utils) \| [Upstream](https://linbit.com/drbd/)
| `dlm` |[Ubuntu](https://launchpad.net/ubuntu/+source/dlm) \| [Upstream](https://pagure.io/dlm)
| `gfs2-utils` |[Ubuntu](https://launchpad.net/ubuntu/+source/gfs2-utils) \| [Upstream](https://pagure.io/gfs2-utils)
| `keepalived` |[Ubuntu](https://launchpad.net/ubuntu/+source/keepalived) \| [Upstream](https://www.keepalived.org/)


- **`libqb`** - Library which provides a set of high performance client-server reusable features. It offers high performance logging, tracing, IPC and poll. Its initial features were spun off the `Corosync` cluster communication suite to make them accessible for other projects.

- **`Kronosnet`** - `Kronosnet`, often referred to as `knet`, is a network abstraction layer designed for High Availability. `Corosync` uses `Kronosnet` to provide multiple networks for its interconnect (replacing the old [Totem Redundant Ring Protocol](https://discourse.ubuntu.com/t/corosync-and-redundant-rings/11627)) and add support for some more features like interconnect network hot-plug.

- **`Corosync`** - or *Cluster Membership Layer*, provides reliable messaging, membership and quorum information about the cluster. Currently, Pacemaker supports `Corosync` as this layer.


- **Pacemaker** - or *Cluster Resource Manager*, provides the brain that processes and reacts to events that occur in the cluster. Events might be: nodes joining or leaving the cluster, resource events caused by failures, maintenance, or scheduled activities. To achieve the desired availability, Pacemaker may start and stop resources and fence nodes.

- **Resource Agents** - Scripts or operating system components that start, stop or monitor resources, given a set of resource parameters. These provide a uniform interface between pacemaker and the managed services.

- **Fence Agents** - Scripts that execute node fencing actions, given a target and fence device parameters.

- **crmsh** - Advanced command-line interface for High-Availability cluster management in GNU/Linux.

- **pcs** - Pacemaker command line interface and GUI. It permits users to easily view, modify and create pacemaker based clusters. `pcs` also provides `pcsd`, which operates as a GUI and remote server for `pcs`. Together `pcs` and `pcsd` form the recommended configuration tool for use with pacemaker. *NOTE: It was added to the [main] repository in Ubuntu Lunar Lobster (23.10)*.

- **cluster-glue** - Reusable cluster components for Linux HA. This package contains node fencing plugins, an error reporting utility, and other reusable cluster components from the Linux HA project.

- **DRBD** - Distributed Replicated Block Device, **DRBD**  is a [distributed replicated storage system](https://en.wikipedia.org/wiki/Distributed_Replicated_Block_Device) for the Linuxplatform. It is implemented as a kernel driver, several userspace management applications, and some shell scripts. DRBD is traditionally used in high availability (HA) clusters.

- **DLM** - A distributed lock manager (DLM) runs in every machine in a cluster, with an identical copy of a cluster-wide lock database. In this way   DLM provides software applications which are distributed across a cluster on multiple machines with a means to synchronize their accesses to shared resources. 

- **gfs2-utils** - Global File System 2 - filesystem tools. The Global File System allows a cluster of machines to concurrently access shared storage hardware like SANs or iSCSI and network block devices.

- **Keepalived** - Keepalived provides simple and robust facilities for loadbalancing and high-availability to Linux system and Linux based infrastructures. Loadbalancing framework relies on well-known and widely used [Linux Virtual Server (IPVS)](http://www.linux-vs.org/) kernel module providing Layer4 loadbalancing. Keepalived implements a set of checkers to dynamically and adaptively maintain and manage loadbalanced server pool according their health. On the other hand high-availability is achieved by [VRRP](https://datatracker.ietf.org/wg/vrrp/documents/) protocol.

### Ubuntu HA Community Packages

Packages in this list are supported just like any other package available in  **[universe] repository**  would be.

| Package | URL |
|-|-|
| pcs* | [Ubuntu](https://launchpad.net/ubuntu/+source/libqb) \| [Upstream](https://github.com/ClusterLabs/pcs)
| csync2| [Ubuntu](https://launchpad.net/ubuntu/+source/csync2) \| [Upstream](https://github.com/LINBIT/csync2)
| corosync-qdevice| [Ubuntu](https://launchpad.net/ubuntu/+source/corosync-qdevice) \| [Upstream](https://github.com/corosync/corosync-qdevice)
| fence-virt| [Ubuntu](https://launchpad.net/ubuntu/+source/fence-virt) \| [Upstream](https://github.com/ClusterLabs/fence-virt)
| sbd| [Ubuntu](https://launchpad.net/ubuntu/+source/sbd) \| [Upstream](https://github.com/ClusterLabs/sbd)
| booth| [Ubuntu](https://launchpad.net/ubuntu/+source/booth) \| [Upstream](https://github.com/ClusterLabs/booth)

- **Corosync-Qdevice** - Its primary use is for even-node clusters, operates at corosync (quorum) layer. Corosync-Qdevice is an independent arbiter for solving split-brain situations. (qdevice-net supports multiple algorithms).

- **SBD** - A Fencing Block Device can be particularly useful in environments where traditional fencing mechanisms are not possible. SBD integrates with Pacemaker, a watchdog device and shared storage to arrange for nodes to reliably self-terminate when  fencing is required.

> Note: **pcs** was added to the [main] repository in Ubuntu Lunar Lobster (23.04).

### Ubuntu HA Deprecated Packages

Packages in this list are  **only supported by the upstream community** . All bugs opened against these agents will be forwarded to upstream IF makes sense (affected version is close to upstream).

| Package|URL|
|-|-|
|ocfs2-tools|[Ubuntu](https://launchpad.net/ubuntu/+source/ocfs2-tools) \| [Upstream](https://github.com/markfasheh/ocfs2-tools)

### Ubuntu HA Related Packages

Packages in this list aren't necessarily **HA** related packages, but they have a very important role in High Availability Clusters and are supported like any other package provide by the **[main]** repository.

| Package | URL |
|-|-|
| multipath-tools | [Ubuntu](https://launchpad.net/ubuntu/+source/multipath-tools) \| [Upstream](https://github.com/opensvc/multipath-tools)
| open-iscsi | [Ubuntu](https://launchpad.net/ubuntu/+source/open-iscsi) \| [Upstream](https://github.com/open-iscsi/open-iscsi)
| sg3-utils | [Ubuntu](https://launchpad.net/ubuntu/+source/sg3-utils) \| [Upstream](http://sg.danny.cz/sg/sg3_utils.html)
| tgt OR targetcli-fb* | [Ubuntu](https://launchpad.net/ubuntu/+source/tgt) \| [Upstream](https://github.com/fujita/tgt)
| lvm2 | [Ubuntu](https://launchpad.net/ubuntu/+source/lvm2) \| [Upstream](https://sourceware.org/lvm2/)

* **LVM2** in a Shared-Storage Cluster Scenario:
<BR>**CLVM** - supported before **Ubuntu 20.04**
A distributed lock manager (DLM) is used to broker concurrent LVM metadata accesses. Whenever a cluster node needs to modify the LVM metadata, it must secure permission from its local  `clvmd` , which is in constant contact with other  `clvmd`  daemons in the cluster and can communicate a desire to get a lock on a particular set of objects.
<br>**[lvmlockd](http://manpages.ubuntu.com/manpages/man8/lvmlockd.8.html)** - supported after **Ubuntu 20.04**
As of 2017, a stable LVM component that is designed to replace  `clvmd`  by making the locking of LVM objects transparent to the rest of LVM, without relying on a distributed lock manager.<BR>
The lvmlockd benefits over clvm are:<BR><BR>
  - lvmlockd supports two cluster locking plugins: DLM and SANLOCK. SANLOCK plugin can supports up to ~2000 nodes that benefits LVM usage in big virtualization / storage cluster, while DLM plugin fits HA cluster.
  - lvmlockd has better design than clvmd. clvmd is command-line level based locking system, which means the whole LVM software will get hang if any LVM command gets dead-locking issue.
  - lvmlockd can work with lvmetad.

> Note: `targetcli-fb (Linux LIO)` will likely replace `tgt` in future Ubuntu versions.

## Upstream Documentation

The server guide does not have the intent to document every existing option for all the HA related software described in this page, but to document recommended scenarios for Ubuntu HA Clusters. You will find more complete documentation upstream at:

- ClusterLabs
  - [Clusters From Scratch](https://clusterlabs.org/pacemaker/doc/en-US/Pacemaker/2.0/html-single/Clusters_from_Scratch/index.html)
  - [Managing Pacemaker Clusters](https://clusterlabs.org/pacemaker/doc/deprecated/en-US/Pacemaker/2.0/html/Clusters_from_Scratch/index.html)
  - [Pacemaker Configuration Explained](https://clusterlabs.org/pacemaker/doc/deprecated/en-US/Pacemaker/2.0/html/Pacemaker_Explained/index.html)
  - [Pacemaker Remote - Scaling HA Clusters](https://clusterlabs.org/pacemaker/doc/deprecated/en-US/Pacemaker/2.0/html/Pacemaker_Remote/index.html)
- Other
  - [Ubuntu Bionic HA in Shared Disk Environments (Azure)](https://discourse.ubuntu.com/t/ubuntu-high-availability-corosync-pacemaker-shared-disk-environments/14874)

> A very special thanks, and all the credits, to [ClusterLabs Project](https://clusterlabs.org/) for all that detailed documentation.
