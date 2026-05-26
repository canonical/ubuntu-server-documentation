---
myst:
  html_meta:
    description: Set up traffic shaping on Ubuntu using tc and the CAKE qdisc to reduce bufferbloat and prioritize low-latency traffic.
---

(traffic-shaping-tc-cake)=
# Traffic shaping with tc and CAKE

When using an Ubuntu machine as a router, traffic shaping helps prioritize low-latency traffic (such as Voice over IP (VoIP), video calls, and gaming) over bulk transfers. This guide explains how to set up traffic shaping using `tc` (traffic control) with the Common Applications Kept Enhanced (CAKE) queuing discipline.

## What is bufferbloat?

Bufferbloat occurs when network buffers become too full, causing high latency and jitter. This happens because routers and modems queue excess packets rather than dropping them, which delays time-sensitive traffic. CAKE is designed to solve this by implementing fair queuing and active queue management.

## Prerequisites

- An Ubuntu system acting as a router with a {term}`WAN` interface (e.g., `ext0`)
- The `iproute2` package (installed by default)
- `systemd-networkd` for network configuration

## Enable Explicit Congestion Notification (ECN)

ECN allows routers to signal congestion by marking packets rather than dropping them. This improves performance when combined with CAKE.

Create `/etc/sysctl.d/50-trafficshaping.conf` with the following contents:

```
# Enable explicit congestion notification for TCP (covers IPv4 and IPv6)
net.ipv4.tcp_ecn = 1
```

Apply the setting:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo sysctl --system
```

## Create the IFB interface

Traffic shaping with `tc` only works on egress (outbound) traffic. To shape ingress (inbound) traffic, redirect it through an Intermediate Functional Block (IFB) interface where it becomes egress traffic that can be shaped.

Create the IFB interface using `systemd-networkd`. First, create the netdev file at `/etc/systemd/network/20-wanifb.netdev` and add the following:

```ini
[NetDev]
Kind=ifb
Name=wanifb
MTUBytes=1492
```

:::{note}
Adjust `MTUBytes` to match your WAN connection. For {term}`PPPoE` connections, 1492 is typical. For standard Ethernet, use 1500. You can measure the {term}`MTU` to be sure.
:::

Create the network file at `/etc/systemd/network/30-wanifb.network`:

```ini
[Match]
Name=wanifb

[Link]
ActivationPolicy=always-up
```

Reload networkd to create the interface:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo networkctl reload
```

Verify the interface exists:

```{terminal}
:copy:
:user:
:host:
:dir:
ip link show wanifb
```

## Create the traffic shaping script

Create `/usr/local/bin/traffic-shaping` with the following content:

```python
#!/usr/bin/env python3
"""
Traffic shaping using CAKE qdisc.

Shapes both upload (egress) and download (ingress via IFB redirect) traffic
to reduce bufferbloat and improve latency for interactive applications.

Test results at: https://www.waveform.com/tools/bufferbloat
"""

import subprocess
import argparse
import shlex

# Configuration - adjust these values for your connection
CONFIG = {
    "wan_iface": "ext0",        # Physical WAN interface
    "ifb_iface": "wanifb",      # IFB interface for download shaping
    # set to ~90-95% of what your ISP effectively delivers (not just their promise)
    # please measure your bandwidth, and remember it can have time-of-day dependent variations
    "upload_speed": "30mbit",   # you -> WAN
    "download_speed": "80mbit", # WAN -> you
}


def run(cmd, ignore_errors=False):
    """Run a shell command."""
    print(f"  {cmd}")
    subprocess.run(shlex.split(cmd), check=(not ignore_errors))


def clear_all():
    """Remove existing traffic shaping rules."""
    run(f"tc qdisc del dev {CONFIG['wan_iface']} root", ignore_errors=True)
    run(f"tc qdisc del dev {CONFIG['wan_iface']} ingress", ignore_errors=True)
    run(f"tc qdisc del dev {CONFIG['ifb_iface']} root", ignore_errors=True)


def start():
    """Apply traffic shaping rules."""
    print("Clearing existing rules...")
    clear_all()

    # Ensure IFB interface is up
    run(f"ip link set dev {CONFIG['ifb_iface']} up", ignore_errors=True)

    # Shape upload (egress on WAN interface)
    print(f"Setting upload limit to {CONFIG['upload_speed']}...")
    run(f"tc qdisc add dev {CONFIG['wan_iface']} root cake "
        f"bandwidth {CONFIG['upload_speed']} nat")

    # Redirect ingress traffic to IFB interface
    print("Redirecting ingress traffic to IFB interface...")
    run(f"tc qdisc add dev {CONFIG['wan_iface']} handle ffff: ingress")
    run(f"tc filter add dev {CONFIG['wan_iface']} parent ffff: protocol all "
        f"u32 match u32 0 0 action mirred egress redirect dev {CONFIG['ifb_iface']}")

    # Shape download (egress on IFB interface)
    print(f"Setting download limit to {CONFIG['download_speed']}...")
    run(f"tc qdisc add dev {CONFIG['ifb_iface']} root cake "
        f"bandwidth {CONFIG['download_speed']} wash")

    print("Traffic shaping enabled.")


def stop():
    """Remove traffic shaping rules."""
    print("Removing traffic shaping rules...")
    clear_all()
    print("Traffic shaping disabled.")


def status():
    """Show current traffic shaping statistics."""
    print(f"\n=== Upload ({CONFIG['wan_iface']}) ===")
    run(f"tc -s qdisc show dev {CONFIG['wan_iface']}")
    print(f"\n=== Download ({CONFIG['ifb_iface']}) ===")
    run(f"tc -s qdisc show dev {CONFIG['ifb_iface']}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage traffic shaping with CAKE qdisc"
    )
    parser.add_argument(
        "action",
        choices=["start", "stop", "status"],
        help="Action to perform"
    )
    args = parser.parse_args()

    actions = {"start": start, "stop": stop, "status": status}
    actions[args.action]()


if __name__ == "__main__":
    main()
```

Make the script executable:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo chmod +x /usr/local/bin/traffic-shaping
```

Edit the `CONFIG` section to match your setup:

- **`wan_iface`**: Your WAN interface name (e.g., `eth0`, `enp1s0`, `ppp0`) - or rename your interface to `ext0` using {manpage}`systemd.link(5)`
- **`ifb_iface`**: The IFB interface name (must match the netdev file)
- **`upload_speed`**: Set to 90-95% of your actual upload speed
- **`download_speed`**: Set to 90-95% of your actual download speed

:::{note}
Setting speeds slightly below your actual bandwidth leaves headroom for the shaper to work effectively. If you set the limit too high, bufferbloat can still occur in upstream devices.
:::

## Create a systemd service

Create `/etc/systemd/system/traffic-shaping.service`:

```ini
[Unit]
Description=Traffic shaping with CAKE
After=network-online.target
Wants=network-online.target
# Bind to the WAN and IFB interfaces
BindsTo=sys-subsystem-net-devices-ext0.device
After=sys-subsystem-net-devices-ext0.device
BindsTo=sys-subsystem-net-devices-wanifb.device
After=sys-subsystem-net-devices-wanifb.device

[Service]
Type=oneshot
ExecStart=/usr/local/bin/traffic-shaping start
ExecStop=/usr/local/bin/traffic-shaping stop
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

:::{note}
Replace `ext0` in the `BindsTo` and `After` lines with your actual WAN interface name - or rename your external interface to `ext0`. The interface name becomes part of the systemd device unit path.
:::

Enable and start the service:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo systemctl daemon-reload
sudo systemctl enable --now traffic-shaping.service
```

## Verify the configuration

Check that the service is running:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo systemctl status traffic-shaping.service
```

View the traffic shaping statistics:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo /usr/local/bin/traffic-shaping status
```

The output shows packet counts, bytes transferred, and drop statistics for both upload and download queues.

## Test for bufferbloat

Use an online bufferbloat test to verify the configuration:

1. Visit the [Waveform Bufferbloat Test](https://www.waveform.com/tools/bufferbloat)
1. Run the test and observe the latency during upload and download
1. A grade of A or B indicates good bufferbloat control

Without traffic shaping, latency typically spikes to hundreds of milliseconds during speed tests. With CAKE properly configured, latency should remain low (under 30ms increase) even under load.

## CAKE options explained

The script uses these CAKE options:

- **`bandwidth`**: The target bandwidth limit
- **`nat`**: Enables {term}`NAT` lookup to identify flows correctly when the router performs NAT (used for upload)
- **`wash`**: Clears {term}`DSCP` markings that may have been set incorrectly by other devices (used for download)

Additional options you may find useful:

- **`diffserv4`**: Enables four-tier priority based on {term}`DSCP` markings
- **`dual-srchost`** / **`dual-dsthost`**: Fairer bandwidth sharing between hosts
- **`docsis`**: Optimizations for cable modem connections

See the {manpage}`tc-cake(8)` manual page for the full list of options.

## Troubleshooting

If traffic shaping is not working as expected:

1. **Verify interfaces exist**:
   ```{terminal}
   :copy:
   :user:
   :host:
   :dir:
   ip link show ext0
   ip link show wanifb
   ```

1. **Check for errors in the service**:
   ```{terminal}
   :copy:
   :user:
   :host:
   :dir:
   sudo journalctl -eu traffic-shaping.service
   ```

1. **Verify CAKE module is loaded**:
   ```{terminal}
   :copy:
   :user:
   :host:
   :dir:
   lsmod | grep cake
   ```

1. **Test manually**:
   ```{terminal}
   :copy:
   :user:
   :host:
   :dir:
   sudo /usr/local/bin/traffic-shaping stop
   sudo /usr/local/bin/traffic-shaping start
   ```

## Further reading

- [Bufferbloat project](https://www.bufferbloat.net/)
- {manpage}`tc(8)` — traffic control command
- {manpage}`tc-cake(8)` — CAKE qdisc documentation
