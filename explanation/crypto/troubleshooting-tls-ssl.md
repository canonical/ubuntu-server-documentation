(troubleshooting-tls-ssl)=
# Troubleshooting TLS/SSL

Debugging TLS/SSL connections and protocols can be daunting due to their complexity. Here are some troubleshooting tips.

## Separate the client and server

Whenever testing TLS/SSL connections over the network, it's best to really separate the client and the server. Remember that the crypto library configuration file is read by the library, not just by a server or a client. It's read by both. Therefore having separate systems acting as clients and servers, with their own configuration files, makes things simpler to analyse.

## Tools

Here are some tools to help troubleshooting a TLS/SSL configuration.

### OpenSSL server and client apps

The OpenSSL server and client tools are very handy to quickly bring up a server with a selection of ciphers and protocols and test it with a client. Being part of OpenSSL, these tools will also initialise the library defaults directly from the OpenSSL config file, so they are very useful to test your configuration changes.

To bring up an OpenSSL server, a certificate with a private key is needed. There are many ways to generate a pair, and here is a quick one:

```bash
$ openssl req -new -x509 -nodes -days 30 -out myserver.pem -keyout myserver.key
```

Answer the questions as you prefer, but the one that needs special attention is the `commonName` (`CN`) one, which should match the hostname of this server. Then bring up the OpenSSL server with this command:

```bash
$ openssl s_server -cert myserver.pem -key myserver.key
```

That will bring up a TLS/SSL server on port 4433. Extra options that can be useful:

* `-port N`: Set a port number. Remember that ports below 1024 require root privileges, so use `sudo` if that's the case.
* `-www`: Will send back a summary of the connection information, like ciphers used, protocols, etc.
* `-tls1_2`, `-tls1_3`, `-no_tls1_3`, `-no_tls1_2`: Enable only the mentioned protocol version, or, with the `no_` prefix variant, disable it.
* `-cipher <string>`: Use the specified cipher string for TLS1.2 and lower.
* `-ciphersuite <string>`: Use the specified string for TLS1.3 ciphers.

The client connection tool can be used like this when connecting to `server`:

```bash
$ echo | openssl s_client -connect server:port 2>&1 | grep ^New
```

That will generally show the TLS version used, and the selected cipher:

```bash
$ echo | openssl s_client -connect j-server.lxd:443 2>&1  | grep ^New
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
```

The ciphers and protocols can also be selected with the same command line options as the server:

```bash
$ echo | openssl s_client -connect j-server.lxd:443 -no_tls1_3 2>&1  | grep ^New
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384

$ echo | openssl s_client -connect j-server.lxd:443 -no_tls1_3 2>&1 -cipher DEFAULT:-AES256 | grep ^New
New, TLSv1.2, Cipher is ECDHE-RSA-CHACHA20-POLY1305
```

### The `sslscan` tool

The `sslscan` tool comes from a package with the same name, and it will scan a server and list the supported algorithms and protocols. It's super useful for determining if your configuration has really disabled or enabled a particular cipher or TLS version.

To use the tool, point it at the server you want to scan:

```bash
$ sslscan j-server.lxd
```

And you will get a report of the ciphers and algorithms supported by that server. [Consult its manpage](https://manpages.ubuntu.com/manpages/man1/sslscan.1.html) for more details.

## References

* [OpenSSL s_server](https://manpages.ubuntu.com/manpages/kinetic/en/man1/openssl-s_server.1ssl.html)
* [OpenSSL s_client](https://manpages.ubuntu.com/manpages/kinetic/en/man1/openssl-s_client.1ssl.html)
* [`sslscan`](https://manpages.ubuntu.com/manpages/man1/sslscan.1.html)
* [`https://badssl.com`](https://badssl.com/): excellent website that can be used to test a client against a multitude of certificates, algorithms, key sizes, protocol versions, and more.
