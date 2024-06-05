(kerberos-encryption-types)=
# Kerberos encryption types

Encryption is at the heart of Kerberos, and it supports multiple cryptographic algorithms. The default choices are good enough for most deployments, but specific situations might need to tweak these settings.

This document will explain the basic configuration parameters of Kerberos that control the selection of encryption algorithms used in a Kerberos deployment.

## Server-side configuration

There are two main server-side configuration parameters that control the encryption types used on the server for its database and its collection or principals. Both exist in `/etc/krb5kdc/kdc.conf` inside the `[realms]` section and are as follows:

 * `master_key_type`
    Specifies the key type of the master key. This is used to encrypt the database, and the default is `aes256-cts-hmac-sha1-96`.

* `supported_enctypes`
    Specifies the default key/salt combinations of principals for this realm. The default is `aes256-cts-hmac-sha1-96:normal aes128-cts-hmac-sha1-96:normal`, and the encryption types should be listed in order of preference.

Possible values for the encryption algorithms are listed in the [MIT documentation on encryption types](https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/kdc_conf.html#encryption-types), and the salt types can be seen [in the MIT keysalt lists](https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/kdc_conf.html#keysalt-lists).

Here is an example showing the default values (other settings removed for brevity):
```text
[realms]
    EXAMPLE.INTERNAL = {
        (...)
        master_key_type = aes256-cts
        supported_enctypes = aes256-cts-hmac-sha1-96:normal aes128-cts-hmac-sha1-96:normal
        (...)
}
```

The master key is created once per realm, when the realm is bootstrapped. That is usually done with the `krb5_newrealm` tool (see [how to install a Kerberos server](how-to-install-a-kerberos-server.md) for details). You can check the master key type with either of these commands on the KDC server:

```bash
$ sudo kadmin.local
kadmin.local:  getprinc K/M
Principal: K/M@EXAMPLE.INTERNAL
(...)
Number of keys: 1
Key: vno 1, aes256-cts-hmac-sha1-96
(...)

$ sudo klist -ke /etc/krb5kdc/stash
Keytab name: FILE:/etc/krb5kdc/stash
KVNO Principal