(troubleshooting-wireguard-vpn)=
# Troubleshooting WireGuard VPN

The following general checklist should help as a first set of steps to try when you run into problems with WireGuard.

- **Verify public and private keys**: When dealing with multiple peers, it's easy to mix these up, especially because the contents of these keys are just random data. There is nothing identifying them, and public and private keys are basically the same (format-wise).

- **Verify `AllowedIPs` list on all peers**.

- **Check with `ip route` and `ip addr show dev <wg-interface>`** if the routes and IPs are set as you expect.

- Double check that you have **`/proc/sys/net/ipv4/ip_forward` set to `1`** where needed.

- When injecting the VPN users into an existing network, without routing, make sure **`/proc/sys/net/ipv4/conf/all/proxy_arp` is set to `1`**.

- Make sure the above `/proc` entries are in **`/etc/sysctl.conf` or a file in `/etc/sysctl.d`** so that they persist reboots.

## The watch wg command

It can be helpful to leave a terminal open with the `watch wg` command. Here is a sample output showing a system with two peers configured, where only one has established the VPN so far:

```bash
Every 2.0s: wg                j-wg: Fri Aug 26 17:44:37 2022

interface: wg0
  public key: +T3T3HTMeyrEDvim8FBxbYjbz+/POeOtG3Rlvl9kJmM=
  private key: (hidden)
  listening port: 51000

peer: 2cJdFcNzXv4YUGyDTahtOfrbsrFsCByatPnNzKTs0Qo=
  endpoint: 10.172.196.106:51000 
  allowed ips: 10.10.11.2/32
  latest handshake: 3 hours, 27 minutes, 35 seconds ago
  transfer: 3.06 KiB received, 2.80 KiB sent

peer: ZliZ1hlarZqvfxPMyME2ECtXDk611NB7uzLAD4McpgI=
  allowed ips: 10.10.11.3/32
```

## Kernel debug messages

WireGuard is also silent when it comes to logging. Being (essentially) a kernel module, we need to explicitly enable verbose logging of its module. This is done with the following command:

```bash
$ echo "module wireguard +p" | sudo tee /sys/kernel/debug/dynamic_debug/control
```

This will write WireGuard logging messages to the kernel log, which can be watched live with:

```bash
$ sudo dmesg -wT
```

To disable logging, run this:

```bash
$ echo "module wireguard -p" | sudo tee /sys/kernel/debug/dynamic_debug/control
```

## Destination address required

If you ping an IP and get back an error like this:

```bash
$ ping 10.10.11.2
PING 10.10.11.2 (10.10.11.2) 56(84) bytes of data.
From 10.10.11.1 icmp_seq=1 Destination Host Unreachable
ping: sendmsg: Destination address required
```

This is happening because the WireGuard interface selected for this destination doesn't know the endpoint for it. In other words, it doesn't know where to send the encrypted traffic.

One common scenario for this is on a peer where there is no `Endpoint` configuration, which is perfectly valid, and the host is trying to send traffic to that peer. Let's take the coffee shop scenario we described earlier as an example.

The laptop is connected to the VPN and exchanging traffic as usual. Then it stops for a bit (the person went to get one more cup). Traffic ceases (WireGuard is silent, remember). If the WireGuard on the home router is now restarted, when it comes back up, it won't know how to reach the laptop, because it was never contacted by it before. This means that at this time, if the home router tries to send traffic to the laptop in the coffee shop, it will get the above error.

Now the laptop user comes back, and generates some traffic to the home network (remember: the laptop has the home network's `Endpoint` value). The VPN "wakes up", data is exchanged, handshakes are completed, and now the home router knows the `Endpoint` associated with the laptop, and can again initiate new traffic to it without issues.

Another possibility is that one of the peers is behind a NAT, and there wasn't enough traffic for the stateful firewall to consider the "connection" alive, and it dropped the NAT mapping it had. In this case, the peer might benefit from the `PersistentKeepalive` configuration, which makes WireGuard send a *keepalive* probe every so many seconds.

## Required key not available

This error:

```bash
$ ping 10.10.11.1 
PING 10.10.11.1 (10.10.11.1) 56(84) bytes of data.
From 10.10.11.2 icmp_seq=1 Destination Host Unreachable
ping: sendmsg: Required key not available
```

Can happen when you have a route directing traffic to the WireGuard interface, but that interface does not have the target address listed in its `AllowedIPs` configuration.

If you have enabled kernel debugging for WireGuard, you will also see a message like this one in the [`dmesg`](https://documentation.ubuntu.com/server/reference/glossary/#term-dmesg) output:

```
wireguard: home0: No peer has allowed IPs matching 10.10.11.1
```
