---
myst:
  html_meta:
    description: Secure your Ubuntu Server console by disabling Ctrl+Alt+Delete reboots and implementing physical access protection measures.
---

(console-security)=
# Console security


It is difficult to defend against the damage that can be caused by someone with physical access to your environment, for example, due to theft of hard drives, power or service disruption, and so on. 

Console security should be addressed as one component of your overall physical security strategy. A locked "screen door" may deter a casual criminal, or at the very least slow down a determined one, so it is still advisable to perform basic precautions with regard to console security.

## Disable Ctrl+Alt+Delete

Anyone with physical access to the keyboard can use the <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>Delete</kbd> key combination to reboot the server without having to log on. While someone could also simply unplug the power source, you should still prevent the use of this key combination on a production server. This forces an attacker to take more drastic measures to reboot the server, and will prevent accidental reboots at the same time.

To disable the reboot action taken by pressing the <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>Delete</kbd> key combination, run the following two commands:

```bash
sudo systemctl mask ctrl-alt-del.target
sudo systemctl daemon-reload
```
