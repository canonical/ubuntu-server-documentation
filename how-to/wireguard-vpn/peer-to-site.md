(wireguard-vpn-peer-to-site)=
# WireGuard VPN peer-to-site


To help understand the WireGuard concepts, we will show some practical setups that hopefully match many scenarios out there.

This is probably the most common setup for a VPN: connecting a single system to a remote site, and getting access to the remote network "as if you were there".

Where to place the remote WireGuard endpoint in the network will vary a lot depending on the topology. It can be in a firewall box, the router itself, or some random system in the middle of the network.

Here we will cover a simpler case more resembling what a home network could be like:

```{mermaid}
 flowchart LR
  %% ASCII -> Mermaid conversion
  host["host"]
  internet(("public internet"))
  router["router"]

  %% Home network
  subgraph home["home 10.10.10.0/24"]
    pi4["pi4"]
    nas["NAS"]
    dots["..."]
  end

  %% Paths
  host --|ppp0|--> internet
  internet --|ppp0|--> router

  router --- pi4
  router --- nas
  router --- dots

```


This diagram represents a typical simple home network setup. You have a router/modem, usually provided by the ISP (Internet Service Provider), and some internal devices like a Raspberry PI perhaps, a NAS (Network Attached Storage), and some other device.

There are basically two approaches that can be taken here: install WireGuard {ref}`on the router <wireguard-vpn-peer-to-site-on-router>`, or on {ref}`another system in the home network <wireguard-on-an-internal-system>`.

Note that in this scenario the "fixed" side, the home network, normally won't have a WireGuard `Endpoint` configured, as the peer is typically "on the road" and will have a dynamic IP address.

```{toctree}
:titlesonly:

Peer-to-site (on router) <peer-to-site-on-router>
Peer-to-site (inside device) <on-an-internal-system>
```
