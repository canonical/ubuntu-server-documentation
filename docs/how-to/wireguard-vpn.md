---
myst:
  html_meta:
    description: Set up WireGuard VPN on Ubuntu Server for peer-to-site and site-to-site connections with security tips and troubleshooting.
---

(how-to-wireguard-vpn)=
# WireGuard VPN

WireGuard is a straightforward, modern, cross-platform VPN implementation. It is usually used to either connect a single system to a remote site ("peer-to-site") or to connect two distinct networks over the internet ("site-to-site").

```{toctree}
:titlesonly:

Peer-to-site <wireguard-vpn/peer-to-site>
Site-to-site <wireguard-vpn/site-to-site>
```

WireGuard can also be set up to route all traffic through the VPN. 

```{toctree}
:titlesonly:

Default gateway <wireguard-vpn/vpn-as-the-default-gateway>
```

There are also some common tasks and tips that will help you adjust your configuration to your needs.

```{toctree}
:titlesonly:

Common tasks <wireguard-vpn/common-tasks>
Security tips <wireguard-vpn/security-tips>
Troubleshooting <wireguard-vpn/troubleshooting>
```

## See also

* Explanation: {ref}`introduction-to-wireguard-vpn`
