(gnutls)=
# GnuTLS

When initialized, the {term}`GnuTLS` library tries to read its system-wide configuration file `/etc/gnutls/config`. This file is present in Ubuntu Noble 24.04 LTS and later, but previous releases did not ship it. In that case, if you want to make configuration changes, it has to be created manually.

This config file can be used to disable (or mark as insecure) algorithms and
protocols in a system-wide manner, overriding the library defaults. Note that,
intentionally, any algorithms or protocols that were disabled or marked as insecure cannot then be re-enabled or marked as secure.

There are many configuration options available for GnuTLS, and we strongly
recommend that you carefully read the upstream documentation listed in the
References section at the end of this page if creating this file or making changes to it.

## Structure of the config file

The GnuTLS configuration file is structured as an INI-style text file. There
are three sections, and each section contains `key = values` lines. For
example:

```text
[global]
override-mode = blocklist

[priorities]
SYSTEM = NORMAL:-MD5

[overrides]
tls-disabled-mac = sha1
```

## The `global` section

The `[global]` section sets the override mode used in the `[overrides]` section:

* `override-mode = blocklist`: the algorithms listed in `[overrides]` are disabled
* `override-mode = allowlist`: the algorithms listed in `[overrides]` are enabled.

Note that in the `allowlist` mode, all algorithms that should be enabled must be listed in `[overrides]`, as the library starts with marking all existing algorithms as disabled/insecure. In practice, this means that using `allowlist` tends to make the list in `[overrides]` quite large. Additionally, GnuTLS automatically constructs a `SYSTEM` keyword (that can be used in `[priorities]`) with all the allowed algorithms and ciphers specified in `[overrides]`.

When using `allowlist`, all options in `[overrides]` will be of the `enabled` form. For example:

```text
[global]
override-mode = allowlist

[overrides]
secure-hash = sha256
enabled-curve = secp256r1
secure-sig = ecdsa-secp256r1-sha256
enabled-version = tls1.3
tls-enabled-cipher = aes-128-gcm
tls-enabled-mac = aead
tls-enabled-group = secp256r1
```

And when using `blocklist`, all `[override]` options have the opposite meaning (i.e. `disabled`):

```text
[global]
override-mode = blocklist

[overrides]
tls-disabled-cipher = aes-128-cbc
tls-disabled-cipher = aes-256-cbc
tls-disabled-mac = sha1
tls-disabled-group = group-ffdhe8192
```

For other examples and a complete list of the valid keys in the `[overrides]` section, please refer to [disabling algorithms and protocols](https://www.gnutls.org/manual/html_node/Disabling-algorithms-and-protocols.html).

## Priority strings

The `[priorities]` section is used to construct **priority strings**. These strings are a way to specify the TLS session's handshake algorithms and options in a compact, easy-to-use, format. Note that priority strings are not guaranteed to imply the same set of algorithms and protocols between different GnuTLS versions.

The default priority string is selected at package build time by the vendor, and in the case of Ubuntu Jammy it's [defined in `debian/rules`](https://git.launchpad.net/ubuntu/+source/gnutls28/tree/debian/rules?h=ubuntu/jammy-devel#n38) as:

```text
NORMAL:-VERS-ALL:+VERS-TLS1.3:+VERS-TLS1.2:+VERS-DTLS1.2:%PROFILE_MEDIUM
```

A priority string can start with a single initial keyword, and then add or remove algorithms or special keywords. The `NORMAL` priority string is [defined in this table](https://gnutls.org/manual/html_node/Priority-Strings.html#tab_003aprio_002dkeywords) in the upstream documentation reference, which also includes many other useful keywords that can be used.

To see the resulting list of ciphers and algorithms from a priority string, one can use the `gnutls-cli` command-line tool. For example, to list all the ciphers and algorithms allowed with the priority string `SECURE256`:

```bash
$ gnutls-cli --list --priority SECURE256
Cipher suites for SECURE256
TLS_AES_256_GCM_SHA384                                  0x13, 0x02      TLS1.3
TLS_CHACHA20_POLY1305_SHA256                            0x13, 0x03      TLS1.3
TLS_ECDHE_ECDSA_AES_256_GCM_SHA384                      0xc0, 0x2c      TLS1.2
TLS_ECDHE_ECDSA_CHACHA20_POLY1305                       0xcc, 0xa9      TLS1.2
TLS_ECDHE_ECDSA_AES_256_CCM                             0xc0, 0xad      TLS1.2
TLS_ECDHE_RSA_AES_256_GCM_SHA384                        0xc0, 0x30      TLS1.2
TLS_ECDHE_RSA_CHACHA20_POLY1305                         0xcc, 0xa8      TLS1.2
TLS_RSA_AES_256_GCM_SHA384                              0x00, 0x9d      TLS1.2
TLS_RSA_AES_256_CCM                                     0xc0, 0x9d      TLS1.2
TLS_DHE_RSA_AES_256_GCM_SHA384                          0x00, 0x9f      TLS1.2
TLS_DHE_RSA_CHACHA20_POLY1305                           0xcc, 0xaa      TLS1.2
TLS_DHE_RSA_AES_256_CCM                                 0xc0, 0x9f      TLS1.2

Protocols: VERS-TLS1.3, VERS-TLS1.2, VERS-TLS1.1, VERS-TLS1.0, VERS-DTLS1.2, VERS-DTLS1.0
Ciphers: AES-256-GCM, CHACHA20-POLY1305, AES-256-CBC, AES-256-CCM
MACs: AEAD
Key Exchange Algorithms: ECDHE-ECDSA, ECDHE-RSA, RSA, DHE-RSA
Groups: GROUP-SECP384R1, GROUP-SECP521R1, GROUP-FFDHE8192
PK-signatures: SIGN-RSA-SHA384, SIGN-RSA-PSS-SHA384, SIGN-RSA-PSS-RSAE-SHA384, SIGN-ECDSA-SHA384, SIGN-ECDSA-SECP384R1-SHA384, SIGN-EdDSA-Ed448, SIGN-RSA-SHA512, SIGN-RSA-PSS-SHA512, SIGN-RSA-PSS-RSAE-SHA512, SIGN-ECDSA-SHA512, SIGN-ECDSA-SECP521R1-SHA512
```

You can manipulate the resulting set by manipulating the priority string. For example, to remove `CHACHA20-POLY1305` from the `SECURE256` set:

```bash
$ gnutls-cli --list --priority SECURE256:-CHACHA20-POLY1305
Cipher suites for SECURE256:-CHACHA20-POLY1305
TLS_AES_256_GCM_SHA384                                  0x13, 0x02      TLS1.3
TLS_ECDHE_ECDSA_AES_256_GCM_SHA384                      0xc0, 0x2c      TLS1.2
TLS_ECDHE_ECDSA_AES_256_CCM                             0xc0, 0xad      TLS1.2
TLS_ECDHE_RSA_AES_256_GCM_SHA384                        0xc0, 0x30      TLS1.2
TLS_RSA_AES_256_GCM_SHA384                              0x00, 0x9d      TLS1.2
TLS_RSA_AES_256_CCM                                     0xc0, 0x9d      TLS1.2
TLS_DHE_RSA_AES_256_GCM_SHA384                          0x00, 0x9f      TLS1.2
TLS_DHE_RSA_AES_256_CCM                                 0xc0, 0x9f      TLS1.2

Protocols: VERS-TLS1.3, VERS-TLS1.2, VERS-TLS1.1, VERS-TLS1.0, VERS-DTLS1.2, VERS-DTLS1.0
Ciphers: AES-256-GCM, AES-256-CBC, AES-256-CCM
MACs: AEAD
Key Exchange Algorithms: ECDHE-ECDSA, ECDHE-RSA, RSA, DHE-RSA
Groups: GROUP-SECP384R1, GROUP-SECP521R1, GROUP-FFDHE8192
PK-signatures: SIGN-RSA-SHA384, SIGN-RSA-PSS-SHA384, SIGN-RSA-PSS-RSAE-SHA384, SIGN-ECDSA-SHA384, SIGN-ECDSA-SECP384R1-SHA384, SIGN-EdDSA-Ed448, SIGN-RSA-SHA512, SIGN-RSA-PSS-SHA512, SIGN-RSA-PSS-RSAE-SHA512, SIGN-ECDSA-SHA512, SIGN-ECDSA-SECP521R1-SHA512
```

And you can give this a new name by adding the following to the `[priorities]` section:

```text
[priorities]
MYSET = SECURE256:-CHACHA20-POLY1305
```

Which allows the `MYSET` priority string to be used like this:

```bash
$ gnutls-cli --list --priority @MYSET
```

## Verification profile (overrides)

When verifying a certificate, or TLS session parameters, GnuTLS uses a set of profiles associated with the session to determine whether the parameters seen in the session are acceptable. These profiles are normally set using the `%PROFILE` priority string, but it is also possible to set a low bar that applications cannot override. This is done with the `min-verification-profile` setting in the `[overrides]` section.

For example:

```text
[overrides]
# do not allow applications use the LOW or VERY-WEAK profiles.
min-verification-profile = legacy
```

The list of values that can be used, and their meaning, is shown in the [key sizes and security parameters](https://gnutls.org/manual/html_node/Selecting-cryptographic-key-sizes.html#tab_003akey_002dsizes) table in the upstream documentation.

## Practical examples

Let's see some practical examples of how we can use the configuration file to tweak the default cryptographic settings of an application linked with GnuTLS.

Contrary to OpenSSL, GnuTLS does not allow a cipher that was once removed to be allowed again. So if you have a setting in the GnuTLS config file that prohibits `CHACHA20`, an application using GnuTLS will not be able to allow it.

### Only use TLSv1.3

One way to do it is to set a new default priority string that removes all TLS versions and then adds back just TLS 1.3:

```INI
[global]
override-mode = blocklist

[overrides]
default-priority-string = NORMAL:-VERS-TLS-ALL:+VERS-TLS1.3
```

With our test server providing everything but TLSv1.3:

```bash
$ sudo openssl s_server -cert j-server.pem -key j-server.key -port 443 -no_tls1_3  -www
```

Connections will fail:

```bash
$ gnutls-cli j-server.lxd
Processed 125 CA certificate(s).
Resolving 'j-server.lxd:443'...
Connecting to '10.0.100.87:443'...
*** Fatal error: A TLS fatal alert has been received.
*** Received alert [70]: Error in protocol version
```

An application linked with GnuTLS will also fail:

```bash
$ lftp -c "cat https://j-server.lxd/status"
cat: /status: Fatal error: gnutls_handshake: A TLS fatal alert has been received.
```

But an application can override these settings, because it's only the priority string that is being manipulated in the GnuTLS config:

```bash
$ lftp -c "set ssl:priority NORMAL:+VERS-TLS-ALL; cat https://j-server.lxd/status" | grep ^New
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384
```

Another way to limit the TLS versions is via specific protocol version configuration keys:

```INI
[global]
override-mode = blocklist

[overrides]
disabled-version = tls1.1
disabled-version = tls1.2
disabled-version = tls1.0
```

Note that setting the same key multiple times will append the new value to the previous value(s).

In this scenario, the application cannot override the config anymore:

```bash
$ lftp -c "set ssl:priority NORMAL:+VERS-TLS-ALL; cat https://j-server.lxd/status" | grep ^New
cat: /status: Fatal error: gnutls_handshake: A TLS fatal alert has been received.
```

### Use only AES256 with TLSv1.3

TLSv1.3 has a small list of ciphers, but it includes {term}`AES`128. Let's remove it:

```INI
[global]
override-mode = blocklist

[overrides]
disabled-version = tls1.1
disabled-version = tls1.2
disabled-version = tls1.0
tls-disabled-cipher = AES-128-GCM
```

If we now connect to a server that was brought up with this config:

```bash
$ sudo openssl s_server -cert j-server.pem -key j-server.key -port 443 -ciphersuites TLS_AES_128_GCM_SHA256 -www
```

Our GnuTLS client will fail:

```bash
$ gnutls-cli j-server.lxd
Processed 126 CA certificate(s).
Resolving 'j-server.lxd:443'...
Connecting to '10.0.100.87:443'...
*** Fatal error: A TLS fatal alert has been received.
*** Received alert [40]: Handshake failed
```

And given GnuTLS' behavior regarding re-enabling a cipher that was once removed, we cannot allow AES128 from the command line either:

```bash
$ gnutls-cli --priority="NORMAL:+AES-128-GCM"  j-server.lxd
Processed 126 CA certificate(s).
Resolving 'j-server.lxd:443'...
Connecting to '10.0.100.87:443'...
*** Fatal error: A TLS fatal alert has been received.
*** Received alert [40]: Handshake failed
```

## References

* [System-wide configuration](https://www.gnutls.org/manual/html_node/System_002dwide-configuration-of-the-library.html)

* [Priority strings](https://gnutls.org/manual/html_node/Priority-Strings.html)

* [`min-verification-profile` values](https://gnutls.org/manual/html_node/Selecting-cryptographic-key-sizes.html#tab_003akey_002dsizes)

* [Disabling algorithms and protocols](https://www.gnutls.org/manual/html_node/Disabling-algorithms-and-protocols.html)

* [Invoking the `gnutls-cli` command line tool](https://gnutls.org/manual/html_node/gnutls_002dcli-Invocation.html)
