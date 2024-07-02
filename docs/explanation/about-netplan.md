(about-netplan)=
# About Netplan

Network configuration on Ubuntu is handled through [Netplan](https://netplan.io/), which provides a high-level, distribution-agnostic way to define how the network on your system should be set up via a [YAML configuration file](https://netplan.readthedocs.io/en/stable/netplan-yaml/).

It is just as useful for configuring networking connectivity on a personal Raspberry Pi project as it is for enterprise systems administrators, who may need to configure and deploy complex networking setups in a consistent way across servers.

It is also flexible enough to be used in virtual environments and containerised deployments where network requirements might be more dynamic. Network bridges for VMs and containers can be straightforwardly defined in the YAML configuration file, and changed without needing to restart the entire network.

Netplan integrates with both of the primary Linux network management daemons: NetworkManager and systemd-networkd. For more general information about Netplan and how it works, see the [introduction to Netplan](https://netplan.readthedocs.io/en/stable/structure-id/) in the official Netplan documentation. 

Server admins may want to get started by checking out our guide to [configuring networks](configuring-networks.md).  For more specific networking tasks with Netplan, we recommend checking out the [list of how-to guides](https://netplan.readthedocs.io/en/stable/howto/) in their documentation.
