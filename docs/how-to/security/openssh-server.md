---
myst:
  html_meta:
    description: Install and configure OpenSSH server on Ubuntu for secure remote access, encrypted file transfers, and authentication methods.
---

(openssh-server)=

# OpenSSH server

OpenSSH is a powerful collection of tools for remotely controlling networked computers and transferring data between them. Here we'll describe some of the configuration settings possible with the OpenSSH server application and how to change them on your Ubuntu system.

OpenSSH is a freely available version of the Secure Shell (SSH) protocol family of tools. Traditional tools, such as `telnet` or `rcp`, are insecure and transmit the user's password in cleartext when used. OpenSSH provides a server daemon and client tools to facilitate secure, encrypted, remote control and file transfer operations, effectively replacing the legacy tools.

The OpenSSH server component, `sshd`, listens continuously for client connections from any of the client tools. When a connection request occurs, `sshd` sets up the correct connection depending on the type of client tool connecting. For example, if the remote computer is connecting with the SSH client application, the OpenSSH server sets up a remote control session after authentication. If a remote user connects to an OpenSSH server with `scp`, the OpenSSH server daemon initiates a secure copy of files between the server and client after authentication.

OpenSSH can use many authentication methods, including plain password, public key cryptography, and Kerberos tickets.

## Install OpenSSH

To install the OpenSSH client applications on your Ubuntu system, use this command at a terminal prompt:

```bash
sudo apt install openssh-client
```

To install the OpenSSH server application, and related support files, use this command at a terminal prompt:

```bash
sudo apt install openssh-server
```

## Configure OpenSSH

To configure the default behavior of the OpenSSH server application, `sshd`, edit the file `/etc/ssh/sshd_config`. For information about the configuration directives used in this file, refer to the online {manpage}`sshd_config(5)` manual page or run `man sshd_config` at a terminal prompt.

There are many directives in the `sshd` configuration file, which control things like communication settings and authentication modes. The following are examples of configuration directives that can be changed by editing the `/etc/ssh/sshd_config` file.

````{tip}
You can use {ref}`etckeeper <install-etckeeper>` to track changes in your `/etc/` with `git`.

Alternatively, before editing the configuration file, you should make a copy of the original `/etc/ssh/sshd_config` file and protect it from writing so you will have the original settings as a reference and to reuse as necessary. You can do this with the following commands:

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original
sudo chmod a-w /etc/ssh/sshd_config.original
```
````

Since losing an SSH server might mean losing your way to reach a server, check the configuration after changing it and before restarting the server:

```bash
sudo sshd -t -f /etc/ssh/sshd_config
```

### Example configuration directive

Let's take a look at an example of a configuration directive change. To make your OpenSSH server display the contents of the `/etc/issue.net` file as a pre-login banner, you can add or modify this line in the `/etc/ssh/sshd_config` file:

```text
Banner /etc/issue.net
```

After making changes to the `/etc/ssh/sshd_config` file, save the file. Then, restart the `sshd` server application to effect the changes using the following command:

```bash
sudo systemctl restart ssh.service
```

```{warning}
Many other configuration directives for `sshd` are available to change the server application's behavior to fit your needs. Be advised, however, if your only method of access to a server is SSH, and you make a mistake when configuring `sshd` via the `/etc/ssh/sshd_config` file, you may find you are locked out of the server upon restarting it. Additionally, if an incorrect configuration directive is supplied, the `sshd` server may refuse to start, so be particularly careful when editing this file on a remote server.
```

(openssh-server-ssh-keys)=

## SSH keys

SSH allows authentication between two hosts without the need of a password, using cryptographic keys instead.
{term}`SSH-key` authentication uses a **private key** and a **public key**.

We recommend the [**ed25519 Elliptic Curve algorithm**](https://ed25519.cr.yp.to/) (`-t ed25519`) due to shorter key size and lower computational requirements.
Alternatively, you can create a key using the **RSA Algorithm** (`-t rsa -b 4096`, for 4096 bit key size) instead.

To generate a key pair, run the following command:

```bash
ssh-keygen -t ed25519
```

During creation, you will be prompted for a key passphrase, which you would enter to use that key (every time, or instead using an {manpage}`ssh-agent(1)`.

By default, the public key is saved in the file `~/.ssh/id_<algorithm>.pub`, while `~/.ssh/id_<algorithm>` is the private key.
To allow login for a user via key, append the content of `id_ed25519.pub` (`id_rsa.pub` for RSA) to `target_machine:~/.ssh/authorized_keys` by running:

```bash
ssh-copy-id username@target_machine
```

Finally, double check the permissions on the `authorized_keys` file -- only the authenticated user must have write permissions.
If the permissions are not correct then change them by:

```bash
chmod go-w .ssh/authorized_keys
```

You should now be able to SSH to the `target_machine` without being prompted for a password.

To troubleshoot this, have a look at the `target_machine`'s live logs of `ssh.service`:

```bash
sudo journalctl -fu ssh.service
```

Since you can have multiple {term}`SSH-key`s, you can configure which to use for which target machine in `~/.ssh/config` (see {manpage}`ssh_config(5)`).



## Connection multiplexing

To reduce connection setup times, multiple SSH sessions to the same `target_machine` can reuse the same {term}`TCP` connection.

Configuration to activate multiplexing in `~/.ssh/config`:
```text
ControlMaster auto
ControlPath %d/.ssh/ssh_mux_%u@%l_%r@%h:%p
```

Optionally, if you want the session to still be re-usable `1` second after disconnecting, set:
```text
ControlPersist 1
```


## Import keys from public keyservers

These days many users have already SSH keys registered with services like Launchpad or GitHub. Those can be imported with:

```bash
ssh-import-id <username-on-remote-service>
```

The prefix `lp:` is implied and means fetching from Launchpad. The alternative `gh:` will make the tool fetch from GitHub instead.

## Two factor authentication

You can add an extra layer of security to the default key-based authentication using two factor authentication. You can add two factor authentication {ref}`using U2F/FIDO hardware authentication devices <two-factor-authentication-with-u2f-or-fido>`. Alternatively, in cases U2F/FIDO hardware authentication devices are unavailable or impractical for your use case you can add it {ref}`using HMAC/Time based One Time Passwords (HOTP/TOTP) <two-factor-authentication-with-totp-or-hotp>`.

## Handling unstable connections

When working on remote systems via SSH, unstable network connections or accidental disconnects can interrupt your work and terminate running processes. Terminal multiplexers provide a solution to this problem by allowing sessions to persist even after disconnection.

Using a {ref}`terminal multiplexer <terminal-multiplexers>` like `tmux` or `screen`, you can start a session on the remote machine that continues running independently of your SSH connection. If your connection drops, you can reconnect and reattach to your existing session, resuming your work exactly where you left off without losing any running processes or command output.

## Further reading

- [Ubuntu Wiki SSH](https://help.ubuntu.com/community/SSH) page.
- [OpenSSH Website](http://www.openssh.org/)
- [Advanced OpenSSH Wiki Page](https://wiki.ubuntu.com/AdvancedOpenSSH)

```{toctree}
self
2FA with TOTP/HOTP <two-factor-authentication-with-totp-or-hotp.md>
2FA with U2F/FIDO <two-factor-authentication-with-u2f-or-fido.md>
```
