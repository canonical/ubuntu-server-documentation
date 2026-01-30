(wireguard-on-an-internal-system)=
# WireGuard on an internal system (peer-to-site)

Sometimes it's not possible to install WireGuard {ref}`on the home router itself <wireguard-vpn-peer-to-site-on-router>`. Perhaps it's a closed system to which you do not have access, or there is no easy build for that architecture, or any of the other possible reasons.

However, you do have a spare system inside your network that you could use. Here we are going to show one way to make this work. There are others, but we believe this to be the least "involved" as it only requires a couple of (very common) changes in the router itself: NAT port forwarding, and {term}`DHCP` range editing.

To recap, our home network has the `10.10.10.0/24` address, and we want to connect to it from a remote location and be "inserted" into that network as if we were there:

```{mermaid}
flowchart LR
    subgraph home["home network, .home domain — 10.10.10.0/24"]
        router["router"]
        pi4["pi4"]
        nas["NAS"]
        extra["Y"]
        dots["..."]
    end
    router --- pi4 & nas & extra & dots
    host["home0<br>10.10.10.11/24"] -- |ppp0| --> internet(("public internet"))
    internet -- |ppp0| --> router
    host -. "wg0<br>10.10.10.10/32" .- pi4
    note["Reserved for VPN users:<br>10.10.10.10–49"] --- router
```

## Router changes

Since, in this scenario, we don't have a new network dedicated to our VPN users, we need to "carve out" a section of the home network and reserve it for the VPN.

The easiest way to reserve IPs for the VPN is to change the router configuration (assuming it's responsible for DHCP in this network) and tell its DHCP server to only hand out addresses from a specific range, leaving a "hole" for our VPN users.

For example, in the case of the `10.10.10.0/24` network, the DHCP server on the router might already be configured to hand out IP addresses from `10.10.10.2` to `10.10.10.254`. We can carve out a "hole" for our VPN users by reducing the DHCP range, as in this table:

|||
|---|---|
| Network | `10.10.10.0/24` |
| Usable addresses | `10.10.10.2` -- `10.10.10.254` (`.1` is the router) |
| DHCP range | `10.10.10.50` -- `10.10.10.254` |
| VPN range | `10.10.10.10` -- `10.10.10.49` |
|||

Or via any other layout that is better suited for your case. In this way, the router will never hand out a DHCP address that conflicts with one that we selected for a VPN user.

The second change we need to do in the router is to **port forward** the WireGuard traffic to the internal system that will be the endpoint. In the diagram above, we selected the `10.10.10.10` system to be the internal WireGuard endpoint, and we will run it on the `51000/udp` port. Therefore, you need to configure the router to forward all `51000/udp` traffic to `10.10.10.10` on the same `51000/udp` port.

Finally, we also need to allow hosts on the internet to send traffic to the router on the `51000/udp` port we selected for WireGuard. This is done in the firewall rules of the device. Sometimes, performing the port forwarding as described earlier also configures the firewall to allow that traffic, but it's better to check.

Now we are ready to configure the internal endpoint.

## Configure the internal WireGuard endpoint

Install the `wireguard` package:

```bash
$ sudo apt install wireguard
```

Generate the keys for this host:

```bash
$ umask 077
$ wg genkey > internal-private.key
$ wg pubkey < internal-private.key > internal-public.key
```

And create the `/etc/wireguard/wg0.conf` file with these contents:

```
[Interface]
Address = 10.10.10.10/32
ListenPort = 51000
PrivateKey = <contents of internal-private.key>

[Peer]
# laptop
PublicKey = <contents of laptop-public.key>
AllowedIPs = 10.10.10.11/32 # any available IP in the VPN range
```

```{note}
Just like in the {ref}`peer-to-site <wireguard-vpn-peer-to-site-on-router>` scenario with WireGuard on the router, there is no `Endpoint` configuration here for the laptop peer, because we don't know where it will be connecting from beforehand.
```

The final step is to configure this internal system as a router for the VPN users. For that, we need to enable a couple of settings:

- **`ip_forward`**: to enable forwarding (aka, routing) of traffic between interfaces.
- **`proxy_arp`**: to reply to Address Resolution Protocol (ARP) requests on behalf of the VPN systems, as if they were locally present on the network segment.

To do that, and make it persist across reboots, create the file `/etc/sysctl.d/70-wireguard-routing.conf` file with this content:

```
net.ipv4.ip_forward = 1
net.ipv4.conf.all.proxy_arp = 1
```

Then run this command to apply those settings:

```bash
$ sudo sysctl -p /etc/sysctl.d/70-wireguard-routing.conf -w
```

Now the WireGuard interface can be brought up:

```bash
$ sudo wg-quick up wg0
```

## Configuring the peer

The peer configuration will be very similar to what was done before. What changes will be the address, since now it won't be on an exclusive network for the VPN, but will have an address carved out of the home network block.

Let's call this new configuration file `/etc/wireguard/home0.conf`:

```
[Interface]
ListenPort = 51000
Address = 10.10.10.11/24
PrivateKey = <contents of the private key for this system>

[Peer]
PublicKey = <contents of internal-public.key>
Endpoint = <home-ppp0-IP-or-hostname>:51000
AllowedIPs = 10.10.10.0/24
```

And bring up this WireGuard interface:

```bash
$ sudo wg-quick up home0
```

```{note}
There is no need to add an index number to the end of the interface name. That is a convention, but not strictly a requirement.
```

## Testing

With the WireGuard interfaces up on both peers, traffic should flow seamlessly in the `10.10.10.0/24` network between remote and local systems.

More specifically, it's best to test the non-trivial cases, that is, traffic between the remote peer and a host other than the one with the WireGuard interface on the home network.
