---
myst:
  html_meta:
    description: Secure your Ubuntu Server console by disabling Ctrl+Alt+Delete, Magic SysRq reboots and implementing physical access protection measures.
---

(console-security)=
# Console security

It is difficult to defend against the damage that can be caused by someone with physical access to your environment, for example, due to theft of hard drives, power or service disruption, and so on. 

Console security should be addressed as one component of your overall physical security strategy. A locked "screen door" may deter a casual criminal, or at the very least slow down a determined one, so it is still advisable to perform basic precautions with regard to console security.

## Disable Ctrl+Alt+Delete

Anyone with physical access to the keyboard can use the {kbd}`Ctrl` + {kbd}`Alt` + {kbd}`Delete` key combination to reboot the server without having to log on. While someone could also simply unplug the power source, you should still prevent the use of this key combination on a production server. This forces an attacker to take more drastic measures to reboot the server, and will prevent accidental reboots at the same time.

To disable the reboot action taken by pressing the {kbd}`Ctrl` + {kbd}`Alt` + {kbd}`Delete` key combination, run the following two commands:

```bash
sudo systemctl mask ctrl-alt-del.target
sudo systemctl daemon-reload
```

:::{note}
To re-enable this feature, use:

```bash
sudo systemctl unmask ctrl-alt-del.target
```
:::

## Disable Magic SysRq keys

The Linux kernel's [Magic SysRq](https://www.kernel.org/doc/html/latest/admin-guide/sysrq.html)
feature allows keyboard shortcuts to send low-level commands directly to the kernel, bypassing
any running applications and without requiring a login. By default, Ubuntu enables a subset of
these functions, including the ability to immediately reboot ({kbd}`Alt` + {kbd}`SysRq` +
{kbd}`b`) or power off ({kbd}`Alt` + {kbd}`SysRq` + {kbd}`o`) the machine. As with
Ctrl+Alt+Delete, this is worth addressing as part of your physical access hardening.

You can check which functions are currently enabled:

```bash
sysctl kernel.sysrq
```

```text
kernel.sysrq = 176
```

The default value of `176` enables filesystem sync (16), remounting read-only
(32), and reboot/poweroff (128). To disable all SysRq functions, create an override file in
`/etc/sysctl.d/` with a higher sort order than the default sysrq configuration file `10-magic-sysrq.conf`:

```bash
echo "kernel.sysrq = 0" | sudo tee /etc/sysctl.d/99-disable-sysrq.conf
sudo sysctl --system
```

The `99-` prefix ensures this file is processed after `10-magic-sysrq.conf`, and the setting
persists across reboots.

Verify the change has taken effect:

```bash
sysctl kernel.sysrq
```

```text
kernel.sysrq = 0
```

:::{note}
To re-enable the default SysRq functions, remove the override file and reload:

```bash
sudo rm /etc/sysctl.d/99-disable-sysrq.conf
sudo sysctl --system
```
:::
