# Smart card authentication with SSH


One of the authentication methods supported by the SSH protocol is public key authentication. A public key is copied to the SSH server where it is stored and marked as authorized. The owner of the corresponding private key in the smart card can then SSH login to the server.

We will use `opensc-pkcs11` on the client to access the smart card drivers, and we will copy the public key from the smart card to the SSH server to make the authentication work.

The following instructions apply to Ubuntu 18.04 later.

## Server configuration
The SSH server and client must be configured to permit smart card authentication.

### Configure the SSH server
The SSH server needs to allow public key authentication set in its configuration file and it needs the user’s public key.

Ensure the server has the PubkeyAuthentication option set to ‘yes’ in its `/etc/ssh/sshd_config` file. In a default `/etc/ssh/sshd_config` in Ubuntu, the
PubkeyAuthentication option is commented out. However, the default is ‘yes’. To ensure the setting, edit the `sshd_config` file and set accordingly.

```
PubkeyAuthentication yes
```

### Restart the SSH server

```
sudo systemctl restart sshd
```

### Set the public key on the server

Extract the user’s public key from the smart card on the SSH client. Use sshkeygen to read the public key from the smart card and into a format consumable
for SSH.

```
ssh-keygen -D /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so > smartcard.pub
```

Copy this key to the SSH server.

```bash
ssh-copy-id -f -i smartcard.pub ubuntu@server-2
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: “smartcard.pub”
ubuntu@server-2’s password:
Number of key(s) added: 1
Now try logging into the machine, with: “ssh ‘ubuntu@server-2’”
and check to make sure that only the key(s) you wanted were added.
```

## Client configuration

The SSH client needs to identify its PKCS#11 provider.  To do that set the PKCS11Provider option in the `~/.ssh/config `file of each user desiring to use SSH smart card login.

```
PKCS11Provider /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so
```

Use this method to enforce SSH smart card login on a per user basis.

After this step you can SSH into the server using the smart card for authentication.
