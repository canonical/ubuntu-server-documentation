---
myst:
  html_meta:
    description: "Obtain trusted TLS certificates with Let's Encrypt and Certbot on Ubuntu, or set up your own Certificate Authority for internal networks."
---

(obtain-tls-certificates)=
# Obtain TLS certificates

Transport Layer Security (TLS) certificates authenticate your server's identity and enable encrypted connections. There are two main approaches:

- **Let's Encrypt** (recommended for internet-facing servers): a free, automated Certificate Authority (CA) whose certificates are trusted by all major browsers and clients.
- **Manual CA** (for internal networks or air-gapped environments): run your own CA and sign certificates yourself; requires distributing the CA certificate to all clients.

## Use Let's Encrypt

[Let's Encrypt](https://letsencrypt.org/) is operated by the Internet Security Research Group (ISRG). It issues certificates via the Automated Certificate Management Environment (ACME) protocol. Certificates are valid for 90 days and can be renewed automatically.

### Prerequisites

- A registered domain name with DNS records pointing to the server.
- Port 80 open in your firewall. The default [HTTP-01 challenge](https://letsencrypt.org/docs/challenge-types/#http-01-challenge) verifies domain ownership by making an HTTP request to your server on port 80, so it must be reachable from the internet during certificate issuance and renewal.

### Install Certbot

[Certbot](https://certbot.eff.org/) is the recommended ACME client for Let's Encrypt. Install it from the snap store:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo snap install --classic certbot
```

### Obtain a certificate

Certbot supports several modes depending on whether a web server is already running.

**With an nginx server running:**

Certbot's [nginx plugin](https://certbot.eff.org/docs/using.html#nginx) finds the server block matching the specified domains in your nginx configuration (typically in `/etc/nginx/sites-enabled/`) and adds the necessary TLS directives in place, then reloads nginx:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo certbot --nginx -d example.com -d www.example.com
```

**With an Apache server running:**

Certbot's [Apache plugin](https://certbot.eff.org/docs/using.html#apache) finds the VirtualHost block matching the specified domains in your Apache configuration (typically in `/etc/apache2/sites-enabled/`) and adds the necessary TLS directives in place, then reloads Apache:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo certbot --apache -d example.com -d www.example.com
```

**Without a web server (standalone mode):**

Certbot starts a temporary web server on port 80 to complete the ACME challenge. Stop any service already listening on port 80 before running this.

```{terminal}
:copy:
:user:
:host:
:dir:
sudo certbot certonly --standalone -d example.com -d www.example.com
```

**With a web server managing the document root (webroot mode):**

If you want to obtain a certificate without modifying your web server configuration, specify the directory the web server serves:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo certbot certonly --webroot -w /var/www/html -d example.com
```

**Multiple domains:**

Each `-d` flag adds a domain as a Subject Alternative Name (SAN), so a single certificate can cover multiple domains and subdomains. If a certificate for any of the listed domains already exists, Certbot expands it to include all specified domains. Pass the complete desired domain list — both existing and new — in a single command:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo certbot --nginx -d example.com -d www.example.com -d mail.example.com
```

### Other challenge methods

The modes above all use the [HTTP-01 challenge](https://letsencrypt.org/docs/challenge-types/#http-01-challenge) and require port 80. For servers not reachable on port 80, or when you need wildcard certificates (e.g., `*.example.com`), you can use the [DNS-01 challenge](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge) instead: it verifies domain ownership via a DNS TXT record and has no inbound port requirements. Certbot supports DNS-01 via [DNS plugins](https://certbot.eff.org/docs/using.html#dns-plugins) for common providers (Cloudflare, Route 53, etc.).

For environments where running an ACME client on each server is not practical — such as air-gapped networks or large fleets — an [ACME proxy server](https://smallstep.com/docs/step-ca/) (such as step-ca) can act as an internal CA that forwards requests to Let's Encrypt, or a centralised ACME client such as [acme.sh](https://acme.sh) or [lego](https://go-acme.github.io/lego/) can manage certificate issuance and distribution centrally.

### Locate the issued certificate files

After a successful run, Certbot writes the certificate files to `/etc/letsencrypt/live/<domain>/`:

| File | Contents |
|------|----------|
| `fullchain.pem` | Server certificate plus any intermediate certificates (use this in most service configurations) |
| `privkey.pem` | Private key |
| `cert.pem` | Server certificate only |
| `chain.pem` | Intermediate certificates only |

Point your service configuration at the files in this directory. For example in nginx:

```text
ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
```

### Automatic renewal

Certbot installs a systemd timer that attempts renewal twice a day. Check that it is active:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo systemctl status snap.certbot.renew.timer
```

Test the renewal process without making any changes:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo certbot renew --dry-run
```

Services configured using the Certbot nginx or Apache plugins are reloaded automatically after a successful renewal. For other services, add a renewal hook. Create `/etc/letsencrypt/renewal-hooks/deploy/reload-service.sh`:

```sh
#!/bin/sh
systemctl reload <your-service>
```

Then make it executable:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-service.sh
```

Replace `<your-service>` with the name of the service to reload after renewal (e.g., `postfix`, `dovecot`, `slapd`).

## Set up a manual Certificate Authority

If the services on your network require more than a few self-signed certificates it may be worth the additional effort to set up your own internal Certification Authority (CA). Using certificates signed by your own CA allows the various services using the certificates to easily trust other services using certificates issued from the same CA.

:::{note}
Clients that connect to your services must trust your CA. You will need to install your CA certificate in the trust store of every client, or distribute it to users. See {ref}`install-a-root-ca-certificate-in-the-trust-store` for how to add a CA certificate to Ubuntu's trust store.
:::

### Create the CA directory structure

First, create the directories to hold the CA certificate and related files:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo mkdir /etc/ssl/CA
```
```{terminal}
:copy:
:user:
:host:
:dir:
sudo mkdir /etc/ssl/newcerts
```

The CA needs a few additional files to operate: one to keep track of the last serial number used by the CA (each certificate must have a unique serial number), and another file to record which certificates have been issued:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo sh -c "echo '01' > /etc/ssl/CA/serial"
```
```{terminal}
:copy:
:user:
:host:
:dir:
sudo touch /etc/ssl/CA/index.txt
```

### Configure OpenSSL

The third file needed is a CA configuration file. Though not strictly necessary, it is convenient when issuing multiple certificates. Edit `/etc/ssl/openssl.cnf`, and in the `[ CA_default ]` section, change:

```ini
dir             = /etc/ssl               # Where everything is kept
database        = $dir/CA/index.txt      # database index file.
certificate     = $dir/certs/cacert.pem  # The CA certificate
serial          = $dir/CA/serial         # The current serial number
private_key     = $dir/private/cakey.pem # The private key
```

### Create the self-signed root certificate

```{terminal}
:copy:
:user:
:host:
:dir:
openssl req -new -x509 -extensions v3_ca -keyout cakey.pem -out cacert.pem -days 3650
```

You will then be asked to enter the details about the certificate. Next, install the root certificate and key:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo mv cakey.pem /etc/ssl/private/
```
```{terminal}
:copy:
:user:
:host:
:dir:
sudo mv cacert.pem /etc/ssl/certs/
```

### Generate a Certificate Signing Request (CSR)

You are now ready to start signing certificates. The first item needed is a Certificate Signing Request (CSR). If the certificate will be used by service daemons, such as Apache, Postfix, Dovecot, etc., a key without a passphrase is often appropriate. Not having a passphrase allows the services to start without manual intervention, usually the preferred way to start a daemon.

:::{warning}
Running your secure service without a passphrase is convenient but insecure -- a compromise of the key means a compromise of the server as well.
:::

To generate the keys for the Certificate Signing Request (CSR) run the following command from a terminal prompt:

```{terminal}
:copy:
:user:
:host:
:dir:
openssl genrsa -des3 -out server.key 2048

Generating RSA private key, 2048 bit long modulus
..........................++++++
.......++++++
e is 65537 (0x10001)
Enter pass phrase for server.key:
```

You can now enter your passphrase. For best security, it should contain **at least** eight characters. The minimum length when specifying `-des3` is four characters. As a best practice it should also include numbers and/or punctuation and not be a word in a dictionary. Also remember that your passphrase is case-sensitive.

Re-type the passphrase to verify. Once you have re-typed it correctly, the server key is generated and stored in the `server.key` file.

Now create the insecure key, the one without a passphrase, and shuffle the key names:

```{terminal}
:copy:
:user:
:host:
:dir:
openssl rsa -in server.key -out server.key.insecure
mv server.key server.key.secure
mv server.key.insecure server.key
```

The insecure key is now named `server.key`, and you can use this file to generate the CSR without a passphrase.

To create the CSR, run the following command at a terminal prompt:

```{terminal}
:copy:
:user:
:host:
:dir:
openssl req -new -key server.key -out server.csr
```

It will prompt you to enter the passphrase. If you enter the correct passphrase, it will prompt you to enter 'Company Name', 'Site Name', 'Email ID', etc. Once you enter all these details, your CSR will be created and it will be stored in the `server.csr` file.

### Sign the certificate

Enter the following to generate a certificate signed by the CA:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo openssl ca -in server.csr -config /etc/ssl/openssl.cnf
```

After entering the password for the CA key, you will be prompted to sign the certificate, and again to commit the new certificate. You should then see a somewhat large amount of output related to the certificate creation.

There should now be a new file, `/etc/ssl/newcerts/01.pem`, containing the same output. Copy and paste everything beginning with the `-----BEGIN CERTIFICATE-----` line and continuing through to the `----END CERTIFICATE-----` lines to a file named after the {term}`hostname` of the server where the certificate will be installed. For example `mail.example.com.crt` is a descriptive name.

Subsequent certificates will be named `02.pem`, `03.pem`, etc.

:::{note}
Replace `mail.example.com.crt` with your own descriptive name.
:::

### Install the certificate

Copy the new certificate to the host that needs it, and configure the appropriate applications to use it. The default location to install certificates is `/etc/ssl/certs`. This enables multiple services to use the same certificate without overly complicated file permissions.

```{terminal}
:copy:
:user:
:host:
:dir:
sudo cp server.key /etc/ssl/private/
```
```{terminal}
:copy:
:user:
:host:
:dir:
sudo cp mail.example.com.crt /etc/ssl/certs/
```

For applications that can be configured to use a CA certificate, you should also copy the `/etc/ssl/certs/cacert.pem` file to the `/etc/ssl/certs/` directory on each server that needs to trust certificates issued by your CA.

## Further reading

- [Let's Encrypt documentation](https://letsencrypt.org/docs/)
- [Certbot documentation](https://certbot.eff.org/docs/)
- The Wikipedia article on [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) provides background on TLS and its history.
- {ref}`certificates` explains the concepts behind public-key cryptography and certificate types.
