# WireGuard VPN peer-to-site (on router)


In this diagram, we are depicting a home network with some devices and a router where we can install WireGuard.

```
                       public internet              ┌─── wg0 10.10.11.1/24
10.10.11.2/24                                       │        VPN network
        home0│            xxxxxx       ppp0 ┌───────┴┐
           ┌─┴──┐         xx   xxxxx  ──────┤ router │
           │    ├─wlan0  xx       xx        └───┬────┘    home network, .home domain
           │    │       xx        x             │.1       10.10.10.0/24
           │    │        xxx    xxx             └───┬─────────┬─────────┐
           └────┘          xxxxxx                   │         │         │
Laptop in                                         ┌─┴─┐     ┌─┴─┐     ┌─┴─┐
Coffee shop                                       │   │     │   │     │   │
                                                  │pi4│     │NAS│     │...│
                                                  │   │     │   │     │   │
                                                  └───┘     └───┘     └───┘
```

Of course, this setup is only possible if you can install software on the router. Most of the time, when it's provided by your ISP, you can't. But some ISPs allow their device to be put into a bridge mode, in which case you can use your own device (a computer, a Raspberry PI, or something else) as the routing device.

Since the router is the default gateway of the network already, this means you can create a whole new network for your VPN users. You also won't have to create any (D)NAT rules since the router is directly reachable from the Internet.

Let's define some addresses, networks, and terms used in this guide:

- **laptop in coffee shop**: just your normal user at a coffee shop, using the provided Wi-Fi access to connect to their home network. This will be one of our **peers** in the VPN setup.
- **`home0`**: this will be the WireGuard interface on the laptop. It's called `home0` to convey that it is used to connect to the **home** network.
- **router**: the existing router at the home network. It has a public interface `ppp0` that has a routable but dynamic IPv4 address (not CGNAT), and an internal interface at `10.10.10.1/24` which is the default gateway for the home network.
- **home network**: the existing home network (`10.10.10.0/24` in this example), with existing devices that the user wishes to access remotely over the WireGuard VPN.
- **`10.10.11.0/24`**: the WireGuard VPN network. This is a whole new network that was created just for the VPN users.
- **`wg0`** on the **router**: this is the WireGuard interface that we will bring up on the router, at the `10.10.11.1/24` address. It is the gateway for the `10.10.11.0/24` VPN network.

With this topology, if, say, the NAS wants to send traffic to `10.10.11.2/24`, it will send it to the default gateway (since the NAS has no specific route to `10.10.11.0/24`), and the gateway will know how to send it to `10.10.11.2/24` because it has the `wg0` interface on that network.

## Configuration

First, we need to create keys for the peers of this setup. We need one pair of keys for the laptop, and another for the home router:

```bash
$ umask 077
$ wg genkey > laptop-private.key
$ wg pubkey < laptop-private.key > laptop-public.key
$ wg genkey > router-private.key
$ wg pubkey < router-private.key > router-public.key
```

Let's create the router `wg0` interface configuration file. The file will be `/etc/wireguard/wg0.conf` and have these contents:

```text
[Interface]
PrivateKey = <contents-of-router-private.key>
ListenPort = 51000
Address = 10.10.11.1/24

[Peer]
PublicKey = <contents-of-laptop-public.key>
AllowedIPs = 10.10.11.2
```

There is no `Endpoint` configured for the laptop peer, because we don't know what IP address it will have beforehand, nor will that IP address be always the same. This laptop could be connecting from a coffee shop's free Wi-Fi, an airport lounge, or a friend's house.

Not having an endpoint here also means that the home network side will never be able to *initiate*  the VPN connection. It will sit and wait, and can only *respond* to VPN handshake requests, at which time it will learn the endpoint from the peer and use that until it changes (i.e. when the peer reconnects from a different site) or it times out.

> **Important**:
> This configuration file contains a secret: **PrivateKey**.
> Make sure to adjust its permissions accordingly, as follows:
> ```
> sudo chmod 0600 /etc/wireguard/wg0.conf
> sudo chown root: /etc/wireguard/wg0.conf
> ```

When activated, this will bring up a `wg0` interface with the address `10.10.11.1/24`, listening on port `51000/udp`, and add a route for the `10.10.11.0/24` network using that interface.

The `[Peer]` section is identifying a peer via its public key, and listing who can connect from that peer. This `AllowedIPs` setting has two meanings:

- When sending packets, the `AllowedIPs` list serves as a routing table, indicating that this peer's public key should be used to encrypt the traffic.
- When receiving packets, `AllowedIPs` behaves like an access control list. After decryption, the traffic is only allowed if it matches the list.

Finally, the `ListenPort` parameter specifies the **UDP** port on which WireGuard will listen for traffic. This port will have to be allowed in the firewall rules of the router. There is neither a default nor a standard port for WireGuard, so you can pick any value you prefer.

Now let's create a similar configuration on the other peer, the laptop. Here the interface is called `home0`, so the configuration file is `/etc/wireguard/home0.conf`:

```
[Interface]
PrivateKey = <contents-of-laptop-private.key>
ListenPort = 51000
Address = 10.10.11.2/24

[Peer]
PublicKey = <contents-of-router-public.key>
Endpoint = <home-ppp0-IP-or-hostname>:51000
AllowedIPs = 10.10.11.0/24,10.10.10.0/24
```

> **Important**:
> As before, this configuration file contains a secret: **PrivateKey**.
> You need to adjust its permissions accordingly, as follows:
> ```
> sudo chmod 0600 /etc/wireguard/home0.conf
> sudo chown root: /etc/wireguard/home0.conf
> ```

We have given this laptop the `10.10.11.2/24` address. It could have been any valid address in the `10.10.11.0/24` network, as long as it doesn't collide with an existing one, and is allowed in the router's peer's `AllowedIPs` list.

> **Note**:
> You may have noticed by now that address allocation is manual, and not via something like DHCP. Keep tabs on it!

In the `[Peer]` stanza for the laptop we have:

- The usual **`PublicKey`** item, which identifies the peer. Traffic to this peer will be encrypted using this public key.
- **`Endpoint`**: this tells WireGuard where to actually send the encrypted traffic to. Since in our scenario the laptop will be initiating connections, it has to know the public IP address of the home router. If your ISP gave you a fixed IP address, great! You have nothing else to do. If, however, you have a dynamic IP address (one that changes every time you establish a new connection), then you will have to set up some sort of dynamic DNS service. There are many such services available for free on the Internet, but setting one up is out of scope for this guide.
- In **`AllowedIPs`** we list our destinations. The VPN network `10.10.11.0/24` is listed so that we can ping `wg0` on the home router as well as other devices on the same VPN, and the actual home network, which is `10.10.10.0/24`. 

If we had used `0.0.0.0/0` alone in `AllowedIPs`, then the VPN would become our default gateway, and all traffic would be sent to this peer. See [Default Gateway](using-the-vpn-as-the-default-gateway.md) for details on that type of setup.

## Testing

With these configuration files in place, it's time to bring the WireGuard interfaces up.

On the home router, run:

```bash
$ sudo wg-quick up wg0
[#] ip link add wg0 type wireguard
[#] wg setconf wg0 /dev/fd/63
[#] ip -4 address add 10.10.11.1/24 dev wg0
[#] ip link set mtu 1378 up dev wg0
```

Verify you have a `wg0` interface with an address of `10.10.11.1/24`:

```bash
$ ip a show dev wg0
9: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1378 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 10.10.11.1/24 scope global wg0
       valid_lft forever preferred_lft forever
```

Verify you have a `wg0` interface up with an address of `10.10.11.1/24`:

```bash
$ ip a show dev wg0
9: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1378 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 10.10.11.1/24 scope global wg0
       valid_lft forever preferred_lft forever
```

And a route to the `10.10.1.0/24` network via the `wg0` interface:

```bash
$ ip route | grep wg0
10.10.11.0/24 dev wg0 proto kernel scope link src 10.10.11.1
```

And `wg show` should show some status information, but no connected peer yet:

```bash
$ sudo wg show
interface: wg0
  public key: <router public key>
  private key: (hidden)
  listening port: 51000

peer: <laptop public key>
  allowed ips: 10.10.11.2/32
```

In particular, verify that the listed public keys match what you created (and expected!).

Before we start the interface on the other peer, it helps to leave the above `show` command running continuously, so we can see when there are changes:

```bash
$ sudo watch wg show
```

Now start the interface on the laptop:

```bash
$ sudo wg-quick up home0
[#] ip link add home0 type wireguard
[#] wg setconf home0 /dev/fd/63
[#] ip -4 address add 10.10.11.2/24 dev home0
[#] ip link set mtu 1420 up dev home0
[#] ip -4 route add 10.10.10.0/24 dev home0
```

Similarly, verify the interface's IP and added routes:

```bash
$ ip a show dev home0
24: home0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 10.10.11.2/24 scope global home0
       valid_lft forever preferred_lft forever

$ ip route | grep home0
10.10.10.0/24 dev home0 scope link
10.10.11.0/24 dev home0 proto kernel scope link src 10.10.11.2
```

Up to this point, the `wg show` output on the home router probably didn't change. That's because we haven't sent any traffic to the home network, which didn't trigger the VPN yet. By default, WireGuard is very "quiet" on the network.

If we trigger some traffic, however, the VPN will "wake up". Let's ping the internal address of the home router a few times:

```bash
$ ping -c 3 10.10.10.1
PING 10.10.10.1 (10.10.10.1) 56(84) bytes of data.
64 bytes from 10.10.10.1: icmp_seq=1 ttl=64 time=603 ms
64 bytes from 10.10.10.1: icmp_seq=2 ttl=64 time=300 ms
64 bytes from 10.10.10.1: icmp_seq=3 ttl=64 time=304 ms
```

Note how the first ping was slower. That's because the VPN was "waking up" and being established. Afterwards, with the tunnel already established, the latency reduced.

At the same time, the `wg show` output on the home router will have changed to something like this:

```bash
$ sudo wg show
interface: wg0
  public key: <router public key>
  private key: (hidden)
  listening port: 51000

peer: <laptop public key>
  endpoint: <laptop public IP>:51000
  allowed ips: 10.10.11.2/32
  latest handshake: 1 minute, 8 seconds ago
  transfer: 564 B received, 476 B sent
```
