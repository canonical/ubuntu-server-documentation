(openssh-crypto-configuration)=
# OpenSSH crypto configuration

Establishing an SSH connection to a remote service involves multiple stages. Each one of these stages will use some form of encryption, and there are configuration settings that control which cryptographic algorithms can be used at each step.

The default selection of algorithms for each stage should be good enough for the majority of deployment scenarios. Sometimes, however, a compliance rule, or a set of legacy servers, or something else, requires a change in this selection. Perhaps a legacy system or piece of hardware that is still in production is not compatible with the current encryption schemes and requires legacy algorithms to be enabled again. Or a compliance rule that isn't up-to-date with the current crypto standards doesn't allow a more advanced cipher.

```{warning}
Be careful when restricting cryptographic algorithms in SSH, specially on the server side. You can inadvertently lock yourself out of a remote system!
```

## Algorithm configuration general rules

Most of the configuration options that take a list of cryptographic algorithms follow a defined set of rules. The first algorithm in the list (that the **client** offers to the server) that matches an offer from the server, is what will be selected. The rules are as follows:

* The lists are algorithm names separated by commas. For example, `Ciphers aes128-gcm@openssh.com,aes256-gcm@openssh.com` will replace the current set of ciphers with the two named algorithms.

* Instead of specifying the full list, which will replace the existing default one, some manipulations are allowed. If the list starts with:

  * **`+`**
     The specified algorithm(s) will be appended to the end of the default set. For example, `MACs +hmac-sha2-512,hmac-sha2-256` will append *both* Message Authentication Code (MAC) algorithms to the end of the current set.

  * **`-`**
     The specified algorithm(s) will be removed from the default set. For example, `KexAlgorithms -diffie-hellman-group1-sha1,diffie-hellman-group14-sha1` will remove *both* key exchange algorithms from the current set.

  * **`^`**
     The specified ciphers will be placed at the beginning of the default set. For example, `PubkeyAcceptedAlgorithms ^ssh-ed25519,ecdsa-sha2-nistp256` will move *both* signature algorithms to the start of the set.
  
  * Wildcards (**`*`**) are also allowed, but be careful to not inadvertently include or exclude something that wasn't intended.

With rare exceptions, the list of algorithms can be queried by running `ssh -Q <config>`, where `<config>` is the configuration setting name. For example, `ssh -Q ciphers` will show the available list of ciphers.

```{note}
The output of the `ssh -Q <name>` command will not take into consideration the configuration changes that may have been made. It cannot therefore be used to test the crypto configuration changes.
```

## Configuration settings

It's not the goal of this documentation to repeat the excellent upstream documentation (see the References section at the end of this page). Instead, we will show the configuration options, and some examples of how to use them.

Here are the configuration settings that control the cryptographic algorithms selection. Unless otherwise noted, they apply to both the server and the client.

* `Ciphers`
    List of symmetric ciphers. Examples include `aes256-ctr` and `chacha20-poly1305@openssh.com`.

* `MACs`
    List of Message Authentication Code algorithms, used for data integrity protection. The `-etm` versions calculate the MAC after encryption and are considered safer. Examples include `hmac-sha2-256` and `hmac-sha2-512-etm@openssh.com`.

* `GSSAPIKexAlgorithms`
    This option is not available in OpenSSH upstream, and is [provided via a patch](https://git.launchpad.net/ubuntu/+source/openssh/tree/debian/patches/gssapi.patch?h=applied/ubuntu/jammy-devel) that Ubuntu and many other Linux Distributions carry. It lists the key exchange (kex) algorithms that are offered for {term}`Generic Security Services Application Program Interface (GSSAPI) <GSSAPI>` key exchange, and only applies to connections using GSSAPI. Examples include `gss-gex-sha1-` and `gss-group14-sha256-`.

* `KexAlgorithms`
    List of available key exchange (kex) algorithms. Examples include `curve25519-sha256` and `sntrup761x25519-sha512@openssh.com`.

* `HostKeyAlgorithms`
    This is a **server-only** configuration option. It lists the available host key signature algorithms that the server offers. Examples include `ssh-ed25519-cert-v01@openssh.com` and `ecdsa-sha2-nistp521-cert-v01@openssh.com`.

* `PubkeyAcceptedAlgorithms`
    List of signature algorithms that will be accepted for public key authentication. Examples include `ssh-ed25519-cert-v01@openssh.com` and `rsa-sha2-512-cert-v01@openssh.com`.

* `CASignatureAlgorithms`
    List of algorithms that certificate authorities (CAs) are allowed to use to sign certificates. Certificates signed using any other algorithm will not be accepted for public key or host-based authentication. Examples include `ssh-ed25519` and `ecdsa-sha2-nistp384`.

To check what effect a configuration change has on the server, it's helpful to use the `-T` parameter and `grep` the output for the configuration key you want to inspect. For example, to check the current value of the `Ciphers` configuration setting after having set `Ciphers ^3des-cbc` in `sshd_config`:

```bash
$ sudo sshd -T | grep ciphers

ciphers 3des-cbc,chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com
```

The output will include changes made to the configuration key. There is no need to restart the service.
    
## OpenSSH examples

Here are some examples of how the cryptographic algorithms can be selected in OpenSSH.

### Which cipher was used?

One way to examine which algorithm was selected is to add the `-v` parameter to the `ssh` client.

For example, assuming password-less public key authentication is being used (so no password prompt), we can use this command to initiate the connection and exit right away:

```bash
$ ssh -v <server> exit 2>&1 | grep "cipher:"

debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
```

In the above case, the `chacha20` cipher was automatically selected. We can influence this decision and only offer one algorithm:

```bash
$ ssh -v -c aes128-ctr <server> exit 2>&1 | grep "cipher:"

debug1: kex: server->client cipher: aes128-ctr MAC: umac-64-etm@openssh.com compression: none
debug1: kex: client->server cipher: aes128-ctr MAC: umac-64-etm@openssh.com compression: none
```

For the other stages in the `ssh` connection, like key exchange, or public key authentication, other expressions for the `grep` command have to be used. In general, it will all be visible in the full `-v` output.

### Remove AES 128 from server

Let's configure an OpenSSH server to only offer the {term}`AES` 256-bit variant of symmetric ciphers for an `ssh` connection.

First, let's see what the default is:

```bash
$ sudo sshd -T | grep ciphers

ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com
```

Now let's make our change. On the server, we can edit `/etc/ssh/sshd_config` and add this line:

```text
Ciphers -aes128*
```

And then check what is left:

```bash
$ sudo sshd -T | grep ciphers

ciphers chacha20-poly1305@openssh.com,aes192-ctr,aes256-ctr,aes256-gcm@openssh.com
```

To activate the change, `ssh` has to be restarted:

```bash
$ sudo systemctl restart ssh.service
```

After we restart the service, clients will no longer be able to use AES 128 to connect to it:

```bash
$ ssh -c aes128-ctr <server>

Unable to negotiate with 10.0.102.49 port 22: no matching cipher found. Their offer: chacha20-poly1305@openssh.com,aes192-ctr,aes256-ctr,aes256-gcm@openssh.com
```

### Prioritize AES 256 on the client

If we just want to prioritize a particular cipher, we can use the "`^`" character to move it to the front of the list, without disabling any other cipher:

```bash
$ ssh -c ^aes256-ctr -v <server> exit 2>&1 | grep "cipher:"

debug1: kex: server->client cipher: aes256-ctr MAC: umac-64-etm@openssh.com compression: none
debug1: kex: client->server cipher: aes256-ctr MAC: umac-64-etm@openssh.com compression: none
```

In this way, if the server we are connecting to does not support AES 256, the negotiation will pick up the next one from the list. If we do that on the server via `Ciphers -aes256*`, this is what the same client, with the same command line, now reports:

```bash
$ ssh -c ^aes256-ctr -v <server> exit 2>&1 | grep "cipher:"

debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
```

## References

* [OpenSSH upstream documentation index](https://www.openssh.org/manual.html)
* Ubuntu {manpage}`sshd_config(5)` manual page
* Ubuntu {manpage}`ssh_config(5)` manual page
