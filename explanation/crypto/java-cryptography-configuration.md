(java-cryptography-configuration)=
# Java cryptography configuration

The Java cryptographic settings are large and complex, with many layers and policies. Here we will focus on one aspect of it, which is how to apply some basic filters to the set of cryptographic algorithms available to applications. The references section at the end contains links to more information.

There are many versions of Java available in Ubuntu. It's best to install the "default" one, which is represented by the `default-jre` (for the Runtime Environment) or `default-jdk` (for the Development Kit). And their non-{term}`GUI` counterparts `default-jre-headless` and `default-jdk-headless`, respectively.

To install the default Java Runtime on Ubuntu Server, run the following command:

```bash
sudo apt install default-jre-headless
```

## Config file

The Java installation in Ubuntu ships a system-wide configuration tree under `/etc/java-<VERSION>-openjdk`. In Ubuntu Jammy 22.04 LTS, the default Java version is 11, so this directory will be `/etc/java-11/openjdk`. In that directory, the file that defines Java security settings, including cryptographic algorithms, is `/etc/java-11-openjdk/security/java.security`.

This is a very large file, with many options and comments. Its structure is simple, with configuration keys and their values. For crypto algorithms, we will be looking into the following settings:

* `jdk.certpah.disabledAlgorithms`: Restrictions on algorithms and key lengths used in certificate path processing.
* `jdk.tls.disabledAlgorithms`: Restrictions on algorithms and key lengths used in SSL/TLS connections.

The list of restrictions has its own format which allows for constructs that disable whole families of algorithms, key sizes, usage, and more. The [`java.security` configuration file](https://git.launchpad.net/ubuntu/+source/openjdk-lts/tree/src/java.base/share/conf/security/java.security?h=applied/ubuntu/jammy-devel#n520) has comments explaining this syntax with some examples.

Changes to these security settings can be made directly in the `/etc/java-11-openjdk/security/java.security` file, or in an alternate file that can be specified to a Java application by setting the `java.security.properties` value. For example, if your java application is called `myapp.java`, you can invoke it as shown below to specify an additional security properties file:

```bash
java -Djava.security.properties=file://$HOME/java.security
```

When using just one equals sign ("`=`") as above, the settings from the specified file are appended to the existing ones. If, however, we use two equals signs:

```bash
java -Djava.security.properties==file://$HOME/java.security
```

Then the settings from `$HOME/java.security` completely override the ones from the main file at `/etc/java-11-openjdk/security/java.security`.

To disable the ability to specify an additional properties file in the command line, set the key `security.overridePropertiesFile` to `false` in `/etc/java-11-openjdk/security/java.security`.

## Practical examples

Let’s see some practical examples of how we can use the configuration file to tweak the default cryptographic settings of a Java application.

The examples will use the Java `keytool` utility for the client part, and a simple OpenSSL test server on localhost for the server part. Since OpenSSL has its own separate configuration, it won't be affected by the changes we make to the Java security settings.

### Test setup

To use the test OpenSSL server, we will have to generate a certificate and key for it to use, and then import that into the Java Certificate Authority (CA) database so it can be trusted.

First, generate a keypair for OpenSSL:

```bash
openssl req -new -x509 -days 30 -nodes -subj "/CN=localhost" -out localhost.pem -keyout localhost.key
```

Now let's import this new certificate into the system-wide CA database. Execute the following commands:

```bash
sudo cp localhost.pem /usr/local/share/ca-certificates/localhost-test.crt
sudo update-ca-certificates
```

For our testing purposes, this is how we will launch our OpenSSL test server:

```bash
openssl s_server -accept 4443 -cert localhost.pem -key localhost.key | grep ^CIPHER
```

This will show the cipher that was selected for each connection, as it occurs.

The client part of our setup will be using the `keytool` utility that comes with Java, but any Java application that is capable of using SSL/TLS should suffice. We will be running the client as below:

```bash
keytool -J-Djava.security.properties=file://$HOME/java.security -printcert -sslserver localhost:4443 > /dev/null;echo $?
```

These are the parameters:

* `-J-Djava.security.properties=...`
   This is used to point at the configuration file snippet that has our changes. It is NOT NEEDED if you are modifying `/etc/java-11-openjdk/security/java.security` instead.

* `-printcert -sslserver localhost:4443`
   Connect to a server on localhost (`-sslserver` is a parameter to `-printcert`, so we need the latter even though we are not interested in the certificate).

The rest is just to ignore all non-error output, and show us the exit status (`0` for success, anything else for an error).

```{note}
`keytool` is not really intended as a tool to test SSL/TLS connections, but being part of the Java packaging makes it convenient and it's enough for our purposes.
```

Let's see some examples now.

### Only use TLSv1.3

Create `$HOME/java.security` with the following content:

```text
jdk.tls.disabledAlgorithms=TLSv1, TLSv1.1, TLSv1.2, SSLv3, SSLv2
```

Notice that TLSv1.3 is absent.

When you then run the `keytool` utility:

```bash
$ keytool -J-Djava.security.properties=file://$HOME/java.security -printcert -sslserver localhost:4443 > /dev/null;echo $?

0
```

The server should log:

```bash
$ openssl s_server -accept 4443 -key localhost.key -cert localhost.pem   | grep ^CIPHER

CIPHER is TLS_AES_256_GCM_SHA384
```

That is a TLSv1.3 cipher. To really test that TLSv1.3 is the only protocol available, we can force some failures:

Force the client to try to use TLSv1.2:

```bash
$ keytool \
  -J-Djava.security.properties=file://$HOME/java.security \
  -J-Djdk.tls.client.protocols=TLSv1.2 \
  -printcert -sslserver localhost:4443

keytool error: java.lang.Exception: No certificate from the SSL server
```

Restart the server with the `no_tls1_3` option, disabling TLSv1.3, and run the client again as originally (without the extra TLSv1.2 option we added above):

**Server**:

```bash
$ openssl s_server -accept 4443 -key localhost.key -cert localhost.pem -no_tls1_3

Using default temp DH parameters
ACCEPT
ERROR
40676E75B37F0000:error:0A000102:SSL routines:tls_early_post_process_client_hello:unsupported protocol:../ssl/statem/statem_srvr.c:1657:
shutting down SSL
CONNECTION CLOSED
```

**Client**:

```bash
$ keytool -J-Djava.security.properties=file://$HOME/java.security -printcert -sslserver localhost:4443

keytool error: java.lang.Exception: No certificate from the SSL server
```

To get a little bit more verbosity in the `keytool` output, you can add the `-v` option. Then, inside the traceback that we get back, we can see an error message about an SSL protocol version:

```bash
$ keytool -J-Djava.security.properties=file://$HOME/java.security -printcert -sslserver localhost:4443  -v

keytool error: java.lang.Exception: No certificate from the SSL server
java.lang.Exception: No certificate from the SSL server
        at java.base/sun.security.tools.keytool.Main.doPrintCert(Main.java:2981)
        at java.base/sun.security.tools.keytool.Main.doCommands(Main.java:1292)
        at java.base/sun.security.tools.keytool.Main.run(Main.java:421)
        at java.base/sun.security.tools.keytool.Main.main(Main.java:414)
Caused by: javax.net.ssl.SSLHandshakeException: Received fatal alert: protocol_version
...
```

### Prevent a specific cipher

The [Java Security Standard Algorithm Names](https://docs.oracle.com/en/java/javase/11/docs/specs/security/standard-names.html) page lists the names of all the cryptographic algorithms recognised by Java. If you want to prevent a specific algorithm from being used, you can list it in the `java.security` file.

In the previous example where we allowed only TLSv1.3 we saw that the negotiated algorithm was `TLS_AES_256_GCM_SHA384`. But what happens if we block it?

Add `TLS_AES_256_GCM_SHA384` to `jdk.tls.disabledAlgorithms` in `$HOME/java.security` like this:

```text
jdk.tls.disabledAlgorithms=TLSv1, TLSv1.1, TLSv1.2, SSLv3, SSLv2, TLS_AES_256_GCM_SHA384
```

If we run our client now:

```bash
$ keytool -J-Djava.security.properties=file://$HOME/java.security -printcert -sslserver localhost:4443 > /dev/null; echo $?

0
```

The server will show the new selected cipher:

```bash
$ openssl s_server -accept 4443 -key localhost.key -cert localhost.pem | grep ^CIPHER

CIPHER is TLS_AES_128_GCM_SHA256
```

## Blocking cipher "elements"

With TLSv1.3 ciphers, we must list the exact cipher name. With TLSv1.2 ciphers, however, there is a bit more flexibility and we can list just an "element".

For example, let's check out a case where we only allow TLSv1.2 for simplicity by once again modifying `$HOME/java.security`:

```text
jdk.tls.disabledAlgorithms=TLSv1, TLSv1.1, TLSv1.3, SSLv2, SSLv3
```

When we run the client:

```bash
$ keytool -J-Djava.security.properties=file://$HOME/java.security -printcert -sslserver localhost:4443  > /dev/null; echo $?

0
```

The server reports:

```bash
$ openssl s_server -accept 4443 -key localhost.key -cert localhost.pem | grep ^CIPHER

CIPHER is ECDHE-RSA-AES256-GCM-SHA384
```

We can block just the AES256 component by using:

```text
jdk.tls.disabledAlgorithms=TLSv1, TLSv1.1, TLSv1.3, SSLv2, SSLv3, AES_256_GCM
```

And now the server reports:

```bash
$ openssl s_server -accept 4443 -key localhost.key -cert localhost.pem | grep ^CIPHER

CIPHER is ECDHE-RSA-CHACHA20-POLY1305
```

## References

  * Additional information on [Java's Cryptographic Algorithms settings](https://www.java.com/en/configure_crypto.html)
  * Java Security [Standard Algorithm Names](https://docs.oracle.com/en/java/javase/12/docs/specs/security/standard-names.html)
  * [Keytool upstream documentation](https://docs.oracle.com/en/java/javase/11/tools/keytool.html)
  * [`java.security` file with comments](https://git.launchpad.net/ubuntu/+source/openjdk-lts/tree/src/java.base/share/conf/security/java.security?h=applied/ubuntu/jammy-devel#n520) -- links to the section which explains the crypto algorithm restrictions)
