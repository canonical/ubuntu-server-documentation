(introduction-to-wireguard-vpn)=
# Introduction to WireGuard VPN

WireGuard is a simple, fast and modern VPN implementation. It is widely deployed and can be used cross-platform.

VPNs have traditionally been hard to understand, configure and deploy. WireGuard removed most of that complexity by focusing on its single task, and leaving out things like key distribution and pushed configurations. You get a network interface which encrypts and verifies the traffic, and the remaining tasks like setting up addresses, routing, etc, are left to the usual system tools like [ip-route(8)](https://manpages.ubuntu.com/manpages/man8/ip-route.8.html) and [ip-address(8)](https://manpages.ubuntu.com/manpages/man8/ip-address.8.html).

Setting up the cryptographic keys is very much similar to configuring SSH for key based authentication: each side of the connection has its own private and public key, and the peers' public key, and this is enough to start encrypting and verifying the exchanged traffic.

For more details on how WireGuard works, and information on its availability on other platforms, please see the references section.

## WireGuard concepts

It helps to think of WireGuard primarily as a network interface, like any other. It will have the usual attributes, like IP address, CIDR, and there will be some routing associated with it. But it also has WireGuard-specific attributes, which handle the VPN part of things.

All of this can be configured via different tools. WireGuard itself ships its own tools in the user-space package `wireguard-tools`: [`wg`](https://manpages.ubuntu.com/manpages/man8/wg.8.html) and [`wg-quick`](https://manpages.ubuntu.com/manpages/man8/wg-quick.8.html). But these are not strictly needed: any user space with the right privileges and kernel calls can configure a WireGuard interface. For example, `systemd-networkd` and `network-manager` can do it on their own, without the WireGuard user-space utilities.

Important attributes of a WireGuard interface are:

- **Private key**: together with the corresponding public key, they are used to authenticate and encrypt data. This is generated with the `wg genkey` command.
- **Listen port**: the UDP port that WireGuard will be listening to for incoming traffic.
- List of **peers**, each one with:
  - **Public key**: the public counterpart of the private key. Generated from the private key of that peer, using the `wg pubkey` command.
  - **Endpoint**: where to send the encrypted traffic to. This is optional, but at least one of the corresponding peers must have it to bootstrap the connection.
  - **Allowed IPs**: list of inner tunnel destination networks or addresses for this peer when sending traffic, or, when receiving traffic, which source networks or addresses are allowed to send traffic to us.

> **Note**:
> Cryptography is not simple. When we say that, for example, a private key is used to decrypt or sign traffic, and a public key is used to encrypt or verify the authenticity of traffic, this is a simplification and is hiding a lot of important details. WireGuard has a detailed explanation of its protocols and cryptography handling [on its website](https://www.wireguard.com/protocol/).

These parameters can be set with the low-level [`wg`](https://manpages.ubuntu.com/manpages/man8/wg.8.html) tool, directly via the command line or with a configuration file. This tool, however, doesn't handle the non-WireGuard settings of the interface. It won't assign an IP address to it, for example, nor set up routing. For this reason, it's more common to use [`wg-quick`](https://manpages.ubuntu.com/manpages/man8/wg-quick.8.html).

`wg-quick` will handle the lifecycle of the WireGuard interface. It can bring it up or down, set up routing, execute arbitrary commands before or after the interface is up, and more. It augments the configuration file that `wg` can use, with its own extra settings, which is important to keep in mind when feeding that file to `wg`, as it will contain settings `wg` knows nothing about.

The `wg-quick` configuration file can have an arbitrary name, and can even be placed anywhere on the system, but the best practice is to:

- Place the file in `/etc/wireguard`.
- Name it after the interface it controls.

For example, a file called `/etc/wireguard/wg0.conf` will have the needed configuration settings for a WireGuard network interface called `wg0`. By following this practice, you get the benefit of being able to call `wg-quick` with just the interface name:

```bash
$ sudo wg-quick up wg0
```

That will bring the `wg0` interface up, give it an IP address, set up routing, and configure the WireGuard-specific parameters for it to work. This interface is usually called `wg0`, but can have any valid network interface name, like `office` (it doesn't need an index number after the name), `home1`, etc. It can help to give it a meaningful name if you plan to connect to multiple peers.

Let's go over an example of such a configuration file:

```
[Interface]
PrivateKey = eJdSgoS7BZ/uWkuSREN+vhCJPPr3M3UlB3v1Su/amWk=
ListenPort = 51000
Address = 10.10.11.10/24

[Peer]
# office
PublicKey = xeWmdxiLjgebpcItF1ouRo0ntrgFekquRJZQO+vsQVs=
Endpoint = wg.example.com:51000 # fake endpoint, just an example
AllowedIPs = 10.10.11.0/24, 10.10.10.0/24
```

In the `[Interface]` section:

- **`Address`**: this is the IP address, and CIDR, that the WireGuard interface will be set up with.
- **`ListenPort`**: the UDP port WireGuard will use for traffic (listening and sending).
- **`PrivateKey`**: the secret key used to decrypt traffic destined for this interface.

The **peers** list, each one in its own `[Peer]` section (example above has just one), comes next:

- **`PublicKey`**: the key that will be used to encrypt traffic to this peer.
- **`Endpoint`**: where to send encrypted traffic to.
- **`AllowedIPs`**: when sending traffic, this is the list of target addresses that identify this peer. When receiving traffic, it's the list of addresses that are allowed to be the source of the traffic.

To generate the keypairs for each peer, the `wg` command is used:

```bash
$ umask 077
$ wg genkey > wg0.key
$ wg pubkey < wg0.key > wg0.pub
```

And then the contents of `wg0.key` and `wg0.pub` can be used in the configuration file.

This is what it looks like when this interface is brought up by `wg-quick`:

```bash
$ sudo wg-quick up wg0
[#] ip link add wg0 type wireguard
[#] wg setconf wg0 /dev/fd/63
[#] ip -4 address add 10.10.11.10/24 dev wg0
[#] ip link set mtu 1420 up dev wg0
[#] ip -4 route add 10.10.10.0/24 dev wg0
```

This is what `wg-quick`:

- Created the WireGuard `wg0` interface.
- Configured it with the data from the configuration file.
- Added the IP/CIDR from the `Address` field to the `wg0` interface.
- Calculated a proper MTU (which can be overridden in the config if needed).
- Added a route for `AllowedIPs`.

Note that in this example `AllowedIPs` is a list of two CIDR network blocks, but `wg-quick` only added a route for `10.10.10.0/24` and skipped `10.10.11.0/24`. That's because the `Address` was already specified as a `/24` one. Had we specified the address as `10.10.11.10/32` instead, then `wg-quick` would have added a route for `10.10.11.0/24` explicitly.

To better understand how `AllowedIPs` work, let's go through a quick example.

Let's say this system wants to send traffic to `10.10.10.201/24`. There is a route for it which says to use the `wg0` interface for that:

```bash
$ ip route get 10.10.10.201
10.10.10.201 dev wg0 src 10.10.11.10 uid 1000
    cache
```

Since `wg0` is a WireGuard interface, it will consult its configuration to see if any peer has that target address in the `AllowedIPs` list. Turns out one peer has it, in which case the traffic will:

  a) Be authenticated as us, and encrypted for that peer.
  b) Sent away via the configured `Endpoint`.

Now let's picture the reverse. This system received traffic on the `ListenPort` UDP port. If it can be decrypted, and verified as having come from one of the listed peers using its respective public key, and if the source IP matches the corresponding `AllowedIPs` list, then the traffic is accepted.

What if there is no `Endpoint`? Well, to bootstrap the VPN, at least one of the peers must have an `Endpoint`, or else it won't know where to send the traffic to, and you will get an error saying "Destination address required" (see the [troubleshooting section](../how-to/troubleshooting-wireguard-vpn.md) for details).

But once the peers know each other, the one that didn't have an `Endpoint` setting in the interface will remember where the traffic came from, and use that address as the current endpoint. This has a very nice side effect of automatically tracking the so called "road warrior" peer, which keeps changing its IP. This is very common with laptops that keep being suspended and awakened in a new network, and then try to establish the VPN again from that new address.

### Peers

You will notice that the term "peers" is used preferably to "server" or "client". Other terms used in some VPN documentation are "left" and "right", which is already starting to convey that the difference between a "server" and a "client" is a bit blurry. It only matters, if at all, at the start of the traffic exchange: who sends the first packet of data?

In that sense, "servers" expect to sit idle and wait for connections to be initiated to them, and "clients" are the initiators. For example, a laptop in a public cafe initiating a connection to the company VPN peer. The laptop needs to know the address of that peer, because it's initiating the exchange. But the "server" doesn't need to know the IP of the laptop beforehand.

On a site-to-site VPN, however, when two separate networks are connected through the tunnel, who is the server and who is the client? Both! So it's best to call them "peers" instead.

## Putting it all together

Key takeaways from this introduction:

- Each peer participating in the WireGuard VPN has a private key and a public key.
- `AllowedIPs` is used as a routing key when sending traffic, and as an ACL when receiving traffic.
- To establish a VPN with a remote peer, you need its public key. Likewise, the remote peer will need your public key.
- At least one of the peers needs an `Endpoint` configured in order to be able to initiate the VPN.

To help better understand these (and other) concepts, we will create some WireGuard VPNs in the next sections, illustrating some common setups.

### Peer-to-site

* [About peer-to-site](../how-to/wireguard-vpn-peer-to-site.md)
* [Set up peer-to-site "on router"](../how-to/wireguard-vpn-peer-to-site-on-router.md)
* [Set up peer-to-site on an internal device](../how-to/wireguard-on-an-internal-system.md)

### Site-to-site

* [Set up site-to-site](../how-to/wireguard-vpn-site-to-site.md)

### Default gateway

* [Using the VPN as the default gateway](../how-to/using-the-vpn-as-the-default-gateway.md)

### Other common tasks, hints and tips
* [Common tasks](../how-to/common-tasks-in-wireguard-vpn.md)
* [Security tips](../how-to/security-tips-for-wireguard-vpn.md)
* [Troubleshooting](../how-to/troubleshooting-wireguard-vpn.md)

> **Note**:
> Throughout this guide, we will sometimes mention a VPN "connection". This is technically false, as WireGuard uses UDP and there is no persistent connection. The term is used just to facilitate understanding, and means that the peers in the examples know each other and have completed a handshake already.

## Further reading

- See the [WireGuard website](https://www.wireguard.com) for more detailed information.
- The [WireGuard Quickstart](https://www.wireguard.com/quickstart/) has a good introduction and demo.
- [wg(8)](https://manpages.ubuntu.com/manpages/jammy/man8/wg.8.html) and [wg-quick(8)](https://manpages.ubuntu.com/manpages/jammy/man8/wg-quick.8.html) manual pages.
- [Detailed explanation](https://www.wireguard.com/protocol/) of the algorithms used by WireGuard.
