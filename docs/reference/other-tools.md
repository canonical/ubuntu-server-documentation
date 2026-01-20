---
myst:
  html_meta:
    description: "Reference documentation for additional Ubuntu Server tools including sudo-rs, tmux, and system utilities."
---

(reference-other-tools)=
# Other tools

Terminal Multiplexers can be a useful tool for system administrators who need to execute multiple sessions in one terminal or SSH connection.
They also tolerate detaching or disconnection from remote sessions.

* {ref}`Terminal Multiplexers <terminal-multiplexers>`

`pam_motd` is a PAM module that allows customized "Message Of The Day" (MOTD) messages to be shown.

* {ref}`pam_motd <pam-motd>`

`sudo-rs` is a safety-oriented and memory-safe implementation of `sudo` written in Rust.

* {ref}`sudo-rs <sudo-rs>`

```{toctree}
:hidden:

terminal-multiplexers <other-tools/terminal-multiplexers>
pam_motd <other-tools/pam-motd>
sudo-rs <other-tools/sudo-rs>
```
