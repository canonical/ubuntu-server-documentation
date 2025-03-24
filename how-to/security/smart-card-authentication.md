(smart-card-authentication)=
# Smart card authentication


One of the most popular uses for smart cards is to control access to computer systems. The owner must physically *have* the smart card, and they must know the PIN to unlock it. This provides a higher degree of security than single-factor authentication (such as just using a password). In this page, we describe how to enable smart card authentication on Ubuntu.

> **Note**:
> This guide is meant for Ubuntu Server 20.04 and newer. If you want to configure a desktop installation refer to the [desktop guide](https://ubuntu.com/tutorials/how-to-use-smart-card-authentication-in-ubuntu-desktop#1-overview).

## Software requirements

The following packages must be installed to obtain a smart card configuration on Ubuntu:
 
* **`pcscd`**: contains the drivers needed to communicate with the CCID smart card readers
* **`opensc-pkcs11`**: (optional, depending on your smartcard hardware) contains the smart card drivers, such as Personal Identify Verification (PIV) or Common Access Card (CAC)
* **`sssd`**: the authentication daemon that manages smart card access and certificate verification

To install these packages, run the following command in your terminal:

```bash
sudo apt install opensc-pkcs11 pcscd sssd libpam-sss
```

## Hardware requirements

Any PIV or CAC smart card with the corresponding reader should be sufficient. USB smart cards like Yubikey embed the reader, and work like regular PIV cards.

Each smart card is expected to contain an X.509 certificate and the corresponding private key to be used for authentication.

## Smart card PKCS#11 modules

While `opensc-pkcs11` supports a wide number of smart cards, some of them may require specific PKCS#11 modules, and you must refer to your vendor to install the proper one. From Ubuntu 20.04 onwards, all modules supported by [`p11-kit`](https://p11-glue.github.io/p11-glue/p11-kit.html) can be used. 

If custom PKCS#11 modules are used, you need to ensure that `p11-kit` is [properly configured](https://p11-glue.github.io/p11-glue/p11-kit/manual/config.html).

In any case, `p11-kit` can be used to see all the configured modules that can be used for authentication:

```bash
$ p11-kit list-modules

p11-kit-trust: p11-kit-trust.so
    library-description: PKCS#11 Kit Trust Module
    library-manufacturer: PKCS#11 Kit
    library-version: 0.23
    token: System Trust
        manufacturer: PKCS#11 Kit
        model: p11-kit-trust
        serial-number: 1
        hardware-version: 0.23
        flags:
               write-protected
               token-initialized
opensc-pkcs11: opensc-pkcs11.so
    library-description: OpenSC smartcard framework
    library-manufacturer: OpenSC Project
    library-version: 0.20
    token: MARCO TREVISAN (PIN CNS0)
        manufacturer: IC: STMicroelectronics; mask:...
        model: PKCS#15 emulated
        serial-number: 6090010669298009
        flags:
               login-required
               user-pin-initialized
               token-initialized
               user-pin-locked
```

## X.509 smart card certificates

The authentication is based on X.509 certificate validation and a smart card can provide one or more certificates that can be used for this purpose.

Before continuing, you may need to export or reference the certificate ID that must be used and associated to each user; such operations can be performed in one of the following three ways:

### Using p11tool

This is a more generic implementation that just uses the PKCS#11 protocol so it should work with all modules:

```bash
sudo apt install gnutls-bin
p11tool --list-tokens
```

Alternatively, URLs can be listed via:

```bash
p11tool --list-token-urls
```

For example:

```text
Token 1:
	URL: pkcs11:model=PKCS%2315%20emulated;manufacturer=IC%3A%20Infineon%3B%20mask%3A%20IDEMIA%20%28O...;serial=6090033068507002;token=MARCO%20TREVISAN%20%28PIN%20CNS1%29
	Label: MARCO TREVISAN (PIN CNS1)
	Type: Hardware token
	Flags: Requires login
	Manufacturer: IC: Infineon; mask: IDEMIA (O...
	Model: PKCS#15 emulated
	Serial: 6090033068507002
	Module: opensc-pkcs11.so
```

The command above will show all the available smart cards in the system and their associated PKCS#11 URI. Copy the URI token of the selected card in the following command, which prints all certificates that can be used for authentication and their associated token URIs.

```bash
p11tool --list-all-certs 'pkcs11:token=[TOKEN-ID]'
```

So in the above example:

```text
$ p11tool --list-all-certs 'pkcs11:token=MARCO%20TREVISAN%20%28PIN%20CNS1%29'
Object 0:
	URL: pkcs11:model=PKCS%2315%20emulated;manufacturer=IC%3A%20Infineon%3B%20mask%3A%20IDEMIA%20%28O...;serial=6090033068507002;token=MARCO%20TREVISAN%20%28PIN%20CNS1%29;id=%02;object=CNS1;type=cert
	Type: X.509 Certificate (RSA-2048)
	Expires: ven 17 dic 2027, 00:00:00
	Label: CNS1
	ID: 02
```

Now, once the URI of the certificate that will be used for authentication is known, let's extract the **Common Name** from the certificate. In the example we are assuming that our certificate URI is `pkcs11:id=%02;type=cert`.

It can be exported as text Privacy Enhanced Mail (PEM) format using:

```bash
$ p11tool --export 'pkcs11:id=%02;type=cert'
```

### Using opensc

```bash
$ sudo apt install opensc
```

Certificates can be via:

```bash
$ pkcs15-tool --list-certificates
```

And exported using

```bash
$ pkcs15-tool --read-certificate [CERTIFICATE_ID]
```

So, for example:

```bash
$ pkcs15-tool --list-certificates 
Using reader with a card: Alcor Micro AU9560 00 00
X.509 Certificate [CNS1]
	Object Flags   : [0x00]
	Authority      : no
	Path           : 3f00140090012002
	ID             : 02
	Encoded serial : 02 10 0357B1EC0EB725BA67BD2D838DDF93D5
$ pkcs15-tool --read-certificate 2
Using reader with a card: Alcor Micro AU9560 00 00
-----BEGIN CERTIFICATE-----
MIIHXDCCBUSgAwIBAgIQA1ex7A6.....
```

### Troubleshooting

The card certificate verification can be simulated using openssl:

```bash
$ sudo apt install openssl

# Save the certificate, using one of the method stated above
$ pkcs15-tool --read-certificate 2 > card-cert.pem
$ p11tool --export 'pkcs11:id=%02;type=cert' > card-cert.pem

# See the certificate contents with
$ openssl x509 -text -noout -in card-cert.pem

# Verify it is valid for the given CA, where 'Ca-Auth-CERT.pem'
# contains all the certificates chain
$ openssl verify -verbose -CAfile CA-Auth-CERT.pem card-cert.pem

# If only the parent CA Certificate is available, can use -partial_chain:
$ openssl verify -verbose -partial_chain -CAfile intermediate_CA_cert.pem
```


## PAM configuration

To enable smart card authentication we should rely on a module that allows PAM supported systems to use X.509 certificates to authenticate logins. The module relies on a PKCS#11 library, such as `opensc-pkcs11` to access the smart card for the credentials it will need. 

When a PAM smart card module is enabled, the login process is as follows:
 1. Enter login
 2. Enter PIN
 3. Validate the X.509 certificate
 4. Map the certificate to a user
 5. Verify the login and match

To enable that process we have to configure the PAM module, add the relevant certificate authorities, add the PAM module to PAM configuration and set the mapping of certificate names to logins.


## Setup guide

This configuration uses SSSD as authentication mechanism, and the example shown here is showing a possible usage for local users, but more complex setups using external remote identity managers such as {term}`FreeIPA`, LDAP, Kerberos or others can be used.

Refer to [SSSD documentation](https://sssd.io/docs/introduction.html) to learn more about this.

### Enable SSSD PAM service

Pam service must be enabled in SSSD configuration, it can be done by ensuring that `/etc/sssd/sssd.conf` contains:

```ini
[sssd]
services = pam

[pam]
pam_cert_auth = True
```

Further `[pam]` configuration options can be changed accroding to [`man sssd.conf`](https://manpages.ubuntu.com/manpages/jammy/en/man5/sssd.conf.5.html#services%20sections).

### Configure SSSD Certificate Authorities database

The card certificate must be allowed by a Certificate Authority, these should be part of `/etc/sssd/pki/sssd_auth_ca_db.pem` (or any other location configured in `[pam]` config section of `sssd.conf` as `pam_cert_db_path`).

As per SSSD using openssl, we need to add the whole certificates chain to the SSSD CA certificates path (if not changed via `sssd.certificate_verification` ), so adding the certificates to the `pam_cert_db_path` is enough:

```bash
sudo cat Ca-Auth-CERT*.pem >> /etc/sssd/pki/sssd_auth_ca_db.pem
```

Certification Revocation List can be also defined in `sssd.conf`, providing a CRL file path in PEM format

```ini
[sssd]
crl_file = /etc/sssd/pki/sssd_auth_crl.pem
soft_crl = /etc/sssd/pki/sssd_auth_soft_crl.pem
```

In case that a full certificate authority chain is not available, openssl won't verify the card certificate, and so sssd should be instructed about.

This is not suggested, but it can be done changing `/etc/sssd/sssd.conf` so that it contains:

```ini
[sssd]
certificate_verification = partial_chain
```

#### Troubleshooting

Card certificate verification can be simulated using SSSD tools directly, by using the command SSSD's `p11_child`:

```bash
# In ubuntu 20.04
$ sudo /usr/libexec/sssd/p11_child --pre -d 10 --debug-fd=2 --nssdb=/etc/sssd/pki/sssd_auth_ca_db.pem

# In ubuntu 22.04 and later versions
$ sudo /usr/libexec/sssd/p11_child --pre -d 10 --debug-fd=2 --ca_db=/etc/sssd/pki/sssd_auth_ca_db.pem
```

If certificate verification succeeds, the tool should output the card certificate name, its ID and the certificate itself in base64 format (other than debug data):

```text
(Mon Sep 11 16:33:32:129558 2023) [p11_child[1965]] [do_card] (0x4000): Found certificate has key id [02].
MARCO TREVISAN (PIN CNS1)
/usr/lib/x86_64-linux-gnu/pkcs11/opensc-pkcs11.so
02
CNS1
MIIHXDCCBUSgAwIBAgIQA1ex7....
```

For checking if the smartcard works, without doing any verification check (and so for debugging purposes the option) `--verify=no_ocsp` can also be used, while `--verify=partial_chain` can be used to do partial CA verification.

### Map certificates to user names

The sss PAM module allows certificates to be used for login, though our Linux system needs to know the username associated to a certificate. SSSD provides a variety of cert mappers to do this. Each cert mapper uses specific  information from the certificate to map to a user on the system. The  different cert mappers may even be stacked. In other words, if the first defined mapper fails to map to a user on the system, the next one will be tried, and so on until a user is found.

For the purposes of this guide, we will use a simple local user mapping as reference.

Mapping for more complex configurations can be done following the official [SSSD documentation](https://sssd.io/design-pages/matching_and_mapping_certificates.html) depending on [providers](https://sssd.io/design-pages/certmaps_for_LDAP_AD_file.html). For up-to-date information on certificate mapping, please also consult the [sss-certmap](https://manpages.ubuntu.com/manpages/jammy/en/man5/sss-certmap.5.html) manpage.

#### Local users mapping

When using only local users, sssd can be easily configured to define an `implicit_domain` that maps all the local users.

Certificate mapping for local users can be easily done using the certificate Subject check, in our example:

```bash
openssl x509 -noout -subject -in card-cert.pem | sed "s/, /,/g;s/ = /=/g"
subject=C=IT,O=Actalis S.p.A.,OU=REGIONE TOSCANA,SN=TREVISAN,GN=MARCO,CN=TRVMRC[...data-removed...]/6090033068507002.UyMnHxfF3gkAeBYHhxa6V1Edazs=
```

So we can use for the user `foo`:

```ini
[sssd]
enable_files_domain = True
services = pam

[certmap/implicit_files/foo]
matchrule = <SUBJECT>.*CN=TRVMRC[A-Z0-9]+/6090033068507002\.UyMnHxfF3gkAeBYHhxa6V1Edazs=.*

[pam]
pam_cert_auth = True
```

#### Troubleshooting

User mapping can be tested working in versions newer than Ubuntu 20.04 with:

```bash
$ sudo dbus-send --system --print-reply \
    --dest=org.freedesktop.sssd.infopipe \
    /org/freedesktop/sssd/infopipe/Users \
    org.freedesktop.sssd.infopipe.Users.ListByCertificate \
    string:"$(cat card-cert.pem)" uint32:10
```
That should return the object path containing the expected user ID:
```text
method return time=1605127192.698667 sender=:1.1628 -> destination=:1.1629 serial=6 reply_serial=2
   array [
      object path "/org/freedesktop/sssd/infopipe/Users/implicit_5ffiles/1000"
   ]
```

### Basic SSSD configuration

The SSSD configuration for accessing to the system is out of the scope of this document, however for smart card login it should contain at least such values:

```ini
[sssd]
# Comma separated list of domains
;domains = your-domain1, your-domain2

# comma-separated list of SSSD services
# pam might be implicitly loaded already, so the line is optional
services = pam

# You can enable debug of the SSSD daemon
# Logs will be in /var/log/sssd/sssd.log
;debug_level = 10

# A mapping between the SC certificate and users
;[certmap/your-domain1/<username>]
;matchrule = <SUBJECT>.*CN=<REGEX MATCHING YOUR CN>.*

[pam]
pam_cert_auth = True

# The Certificate DB to be used:
# - Needs to be an openSSL CA certificates
;pam_cert_db_path = /etc/ssl/certs/ca-certificates.crt

# You can enable debug infos for the PAM module
# Logs will be in /var/log/sssd/sssd_pam.log
# p11 child logs are in /var/log/sssd/p11_child.log
# standard auth logs are in /var/log/auth.log
;pam_verbosity = 10
;debug_level = 10
```

In general what's in the configuration file will affect the way SSSD will call the `p11_child` tool (that is the one in charge for the actual authentication).
Check `man sssd.conf` for details.

Remember that this file should be owned by `root` and have permission set to `600`, otherwise won't be loaded and SSSD will not complain gracefully.
On errors you can test running SSSD temporary with `sudo sssd -d9 -i`.

Every time the configuration is changed sssd should be restarted (`systemctl restart sssd`).

### Add `pam_sss` to PAM

The next step includes the `pam_sss` module into the PAM stack. There are various ways to do this depending on your local policy. The following example enables smart card support for general authentication.

Edit `/etc/pam.d/common-auth` to include the `pam_sss` module as follows:

#### For Ubuntu later than 23.10

```
$ sudo pam-auth-update
```

Then you can interactively enable SSSD profiles for smart-card only or optional smart card access.

You can also set this non-interactively by using:

```
# To use smart-card only authentication
$ sudo pam-auth-update --disable sss-smart-card-optional --enable sss-smart-card-required

# To use smart-card authentication with fallback
$ sudo pam-auth-update --disable sss-smart-card-required --enable sss-smart-card-optional

```

#### For Ubuntu 23.10 and lower

```
# require SSSD smart card login
auth    [success=done default=die]    pam_sss.so allow_missing_name require_cert_auth
```

or only try to use it:

```
# try SSSD smart card login
auth    [success=ok default=ignore]    pam_sss.so allow_missing_name try_cert_auth
```

See [`man pam.conf`](https://manpages.ubuntu.com/manpages/jammy/en/man5/pam.conf.5.html), [`man pam_sss`](https://manpages.ubuntu.com/manpages/jammy/en/man8/pam_sss.8.html) for further details.

---
**Warning:** A global configuration such as this requires a smart card for su and sudo authentication as well!
If you want to reduce the scope of this module, move it to the appropriate pam configuration file in `/etc/pam.d` and ensure that's referenced by `pam_p11_allowed_services` in `sssd.conf`.

---

The OS is now ready to do a smart card login for the user foo.

#### Troubleshooting

`pamtester` is your friend!

To get better debug logging, also increase the SSSD verbosity by changing `/etc/sssd/sssd.conf` so that it has:

```ini
[pam]
pam_verbosity = 10
debug_level = 10
```

You can use it to check your configuration without having to login/logout for real, by just using:

```bash
# Install it!
$ sudo apt install pamtester

# Run the authentication service as standalone
$ pamtester -v login $USER authenticate

# Run the authentication service to get user from cert
$ pamtester -v login "" authenticate

# You can check what happened in the logs, reading:
sudo less /var/log/auth.log
sudo less /var/log/sssd/sssd_pam.log
sudo less /var/log/sssd/p11_child.log
```

## SSH authentication

See [this page on SSH authentication with smart cards](smart-card-authentication-with-ssh.md).
