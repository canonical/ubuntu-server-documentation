(openssh-server)=

# OpenSSH server

OpenSSH is a powerful collection of tools for remotely controlling networked computers and transferring data between them. Here we'll describe some of the configuration settings possible with the OpenSSH server application and how to change them on your Ubuntu system.

OpenSSH is a freely available version of the Secure Shell (SSH) protocol family of tools. Traditional tools, such as `telnet` or `rcp`, are insecure and transmit the user's password in cleartext when used. OpenSSH provides a server daemon and client tools to facilitate secure, encrypted, remote control and file transfer operations, effectively replacing the legacy tools.

The OpenSSH server component, `sshd`, listens continuously for client connections from any of the client tools. When a connection request occurs, `sshd` sets up the correct connection depending on the type of client tool connecting. For example, if the remote computer is connecting with the SSH client application, the OpenSSH server sets up a remote control session after authentication. If a remote user connects to an OpenSSH server with `scp`, the OpenSSH server daemon initiates a secure copy of files between the server and client after authentication.

OpenSSH can use many authentication methods, including plain password, public key, and Kerberos tickets.

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

To configure the default behavior of the OpenSSH server application, `sshd`, edit the file `/etc/ssh/sshd_config`. For information about the configuration directives used in this file, refer to the online {manpage}`sshd_config(5)` manpage or run `man sshd_config` at a terminal prompt.

There are many directives in the `sshd` configuration file, which control things like communication settings and authentication modes. The following are examples of configuration directives that can be changed by editing the `/etc/ssh/sshd_config` file.

````{tip}
Before editing the configuration file, you should make a copy of the original `/etc/ssh/sshd_config` file and protect it from writing so you will have the original settings as a reference and to reuse as necessary. You can do this with the following commands:

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

## SSH keys

SSH allows authentication between two hosts without the need of a password. SSH key authentication uses a **private key** and a **public key**.

To generate the keys, run the following command:

```bash
ssh-keygen -t rsa
```

This will generate the keys using the **RSA Algorithm**. At the time of this writing, the generated keys will have 3072 bits. You can modify the number of bits by using the `-b` option. For example, to generate keys with 4096 bits, you can use:

```bash
ssh-keygen -t rsa -b 4096
```

During the process you will be prompted for a password. Simply hit <kbd>Enter</kbd> when prompted to create the key.

By default, the public key is saved in the file `~/.ssh/id_rsa.pub`, while `~/.ssh/id_rsa` is the private key. Now copy the `id_rsa.pub` file to the remote host and append it to `~/.ssh/authorized_keys` by running:

```bash
ssh-copy-id username@remotehost
```

Finally, double check the permissions on the `authorized_keys` file -- only the authenticated user should have read and write permissions. If the permissions are not correct then change them by:

```bash
chmod 600 .ssh/authorized_keys
```

You should now be able to SSH to the host without being prompted for a password.

## Import keys from public keyservers

These days many users have already SSH keys registered with services like Launchpad or GitHub. Those can be imported with:

```bash
ssh-import-id <username-on-remote-service>
```

The prefix `lp:` is implied and means fetching from Launchpad. The alternative `gh:` will make the tool fetch from GitHub instead.

## Two factor authentication

You can add an extra layer of security to the default key-based authentication using two factor authentication. You can add two factor authentication {ref}`using U2F/FIDO hardware authentication devices <two-factor-authentication-with-u2f-or-fido>`. Alternatively, in cases U2F/FIDO hardware authentication devices are unavailable or impractical for your use case you can add it {ref}`using HMAC/Time based One Time Passwords (HOTP/TOTP) <two-factor-authentication-with-totp-or-hotp>`.

## Further reading

- [Ubuntu Wiki SSH](https://help.ubuntu.com/community/SSH) page.
- [OpenSSH Website](http://www.openssh.org/)
- [Advanced OpenSSH Wiki Page](https://wiki.ubuntu.com/AdvancedOpenSSH)

```{toctree}
self
2FA with TOTP/HOTP <two-factor-authentication-with-totp-or-hotp.md>
2FA with U2F/FIDO <two-factor-authentication-with-u2f-or-fido.md>
```
