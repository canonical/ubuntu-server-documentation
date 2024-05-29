# Install and configure Postfix

> **Note**:
> This guide does not cover setting up Postfix *Virtual Domains*. For information on Virtual Domains and other advanced configurations see the references list at the end of this page.

## Install Postfix

To install [Postfix](https://www.postfix.org/) run the following command:

```bash
sudo apt install postfix
```

It is OK to accept defaults initially by pressing return for each question. Some of the configuration options will be investigated in greater detail in the configuration stage.

> **Deprecation warning:**
> The `mail-stack-delivery` metapackage has been deprecated in Focal. The package still exists for compatibility reasons, but won't setup a working email system.

## Configure Postfix

There are four things you should decide before configuring:

  - The \<Domain> for which you'll accept email (we'll use **`mail.example.com`** in our example)
  - The network and class range of your mail server (we'll use **`192.168.0.0/24`**)
  - The username (we're using **`steve`**)
  - Type of mailbox format (*`mbox`* is the default, but we'll use the alternative, **`Maildir`**)

To configure postfix, run the following command:

```bash
sudo dpkg-reconfigure postfix
```

The user interface will be displayed. On each screen, select the following values:

  - Internet Site
  - **`mail.example.com`**
  - **`steve`**
  - **`mail.example.com`**, `localhost.localdomain`, `localhost`
  - No
  - `127.0.0.0/8 \[::ffff:127.0.0.0\]/104 \[::1\]/128` **`192.168.0.0/24`**
  - 0
  - \+
  - all

To set the mailbox format, you can either edit the configuration file directly, or use the `postconf` command.  In either case, the configuration parameters will be stored in `/etc/postfix/main.cf` file. Later if you wish to re-configure a particular parameter, you can either run the command or change it manually in the file.

### Configure mailbox format

To configure the mailbox format for **`Maildir`**:

```bash
sudo postconf -e 'home_mailbox = Maildir/'
```

This will place new mail in `/home/<username>/Maildir` so you will need to configure your Mail Delivery Agent (MDA) to use the same path.

## SMTP authentication

SMTP-AUTH allows a client to identify itself through the Simple Authentication and Security Layer (SASL) authentication mechanism, using Transport Layer Security (TLS) to encrypt the authentication process. Once it has been authenticated, the SMTP server will allow the client to relay mail.

### Configure SMTP authentication

To configure Postfix for SMTP-AUTH using SASL (Dovecot SASL), run these commands at a terminal prompt:

```bash
sudo postconf -e 'smtpd_sasl_type = dovecot'
sudo postconf -e 'smtpd_sasl_path = private/auth'
sudo postconf -e 'smtpd_sasl_local_domain ='
sudo postconf -e 'smtpd_sasl_security_options = noanonymous,noplaintext'
sudo postconf -e 'smtpd_sasl_tls_security_options = noanonymous'
sudo postconf -e 'broken_sasl_auth_clients = yes'
sudo postconf -e 'smtpd_sasl_auth_enable = yes'
sudo postconf -e 'smtpd_recipient_restrictions = \
permit_sasl_authenticated,permit_mynetworks,reject_unauth_destination'
```

> **Note**:
> The `smtpd_sasl_path` config parameter is a path relative to the Postfix queue directory.

There are several SASL mechanism properties worth evaluating to improve the security of your deployment. The options "noanonymous,noplaintext" prevent the use of mechanisms that permit anonymous authentication or that transmit credentials unencrypted.

### Configure TLS

Next, generate or obtain a digital certificate for TLS. MUAs connecting to your mail server via TLS will need to recognise the certificate used for TLS. This can either be done using a certificate from Let's Encrypt, from a commercial CA or with a self-signed certificate that users manually install/accept.

For MTA-to-MTA, TLS certificates are never validated without prior agreement from the affected organisations. For MTA-to-MTA TLS, there is no reason not to use a self-signed certificate unless local policy requires it. See our [guide on security certificates](../explanation/certificates.md) for details about generating digital certificates and setting up your own Certificate Authority (CA).

Once you have a certificate, configure Postfix to provide TLS encryption for both incoming and outgoing mail:

```bash
sudo postconf -e 'smtp_tls_security_level = may'
sudo postconf -e 'smtpd_tls_security_level = may'
sudo postconf -e 'smtp_tls_note_starttls_offer = yes'
sudo postconf -e 'smtpd_tls_key_file = /etc/ssl/private/server.key'
sudo postconf -e 'smtpd_tls_cert_file = /etc/ssl/certs/server.crt'
sudo postconf -e 'smtpd_tls_loglevel = 1'
sudo postconf -e 'smtpd_tls_received_header = yes'
sudo postconf -e 'myhostname = mail.example.com'
```

If you are using your own Certificate Authority to sign the certificate, enter:

```bash
sudo postconf -e 'smtpd_tls_CAfile = /etc/ssl/certs/cacert.pem'
```

Again, for more details about certificates see our [security certificates guide](../explanation/certificates.md).

### Outcome of initial configuration

After running all the above commands, Postfix will be configured for SMTP-AUTH with a self-signed certificate for TLS encryption.

Now, the file `/etc/postfix/main.cf` should look like this:

```text
# See /usr/share/postfix/main.cf.dist for a commented, more complete
# version
    
smtpd_banner = $myhostname ESMTP $mail_name (Ubuntu)
biff = no
    
# appending .domain is the MUA's job.
append_dot_mydomain = no
    
# Uncomment the next line to generate "delayed mail" warnings
#delay_warning_time = 4h
    
myhostname = server1.example.com
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
myorigin = /etc/mailname
mydestination = server1.example.com, localhost.example.com, localhost
relayhost =
mynetworks = 127.0.0.0/8
mailbox_command = procmail -a "$EXTENSION"
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
smtpd_sasl_local_domain =
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
broken_sasl_auth_clients = yes
smtpd_recipient_restrictions =
permit_sasl_authenticated,permit_mynetworks,reject _unauth_destination
smtpd_tls_auth_only = no
smtp_tls_security_level = may
smtpd_tls_security_level = may
smtp_tls_note_starttls_offer = yes
smtpd_tls_key_file = /etc/ssl/private/smtpd.key
smtpd_tls_cert_file = /etc/ssl/certs/smtpd.crt
smtpd_tls_CAfile = /etc/ssl/certs/cacert.pem
smtpd_tls_loglevel = 1
smtpd_tls_received_header = yes
smtpd_tls_session_cache_timeout = 3600s
tls_random_source = dev:/dev/urandom
```

The Postfix initial configuration is now complete. Run the following command to restart the Postfix daemon:

```bash
sudo systemctl restart postfix.service
```

## SASL

Postfix supports SMTP-AUTH as defined in [RFC2554](http://www.ietf.org/rfc/rfc2554.txt). It is based on [SASL](http://www.ietf.org/rfc/rfc2222.txt). However it is still necessary to set up SASL authentication before you can use SMTP-AUTH.

When using IPv6, the `mynetworks` parameter may need to be modified to allow IPv6 addresses, for example:

```text
mynetworks = 127.0.0.0/8, [::1]/128
```

### Configure SASL

Postfix supports two SASL implementations: **Cyrus SASL** and **Dovecot SASL**. 

To enable Dovecot SASL the `dovecot-core` package will need to be installed:

```bash
sudo apt install dovecot-core
```

Next, edit `/etc/dovecot/conf.d/10-master.conf` and change the following:

```text
service auth {
  # auth_socket_path points to this userdb socket by default. It's typically
  # used by dovecot-lda, doveadm, possibly imap process, etc. Its default
  # permissions make it readable only by root, but you may need to relax these
  # permissions. Users that have access to this socket are able to get a list
  # of all usernames and get results of everyone's userdb lookups.
  unix_listener auth-userdb {
    #mode = 0600
    #user = 
    #group = 
  }
    
  # Postfix smtp-auth
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix
  }
 }
```

To permit use of SMTP-AUTH by Outlook clients, change the following line in the **authentication mechanisms** section of `/etc/dovecot/conf.d/10-auth.conf` from:

```text
auth_mechanisms = plain
```

to this:

```text
auth_mechanisms = plain login
```

Once you have configured Dovecot, restart it with:

```bash
sudo systemctl restart dovecot.service
```

## Test your setup

SMTP-AUTH configuration is complete -- now it is time to test the setup. To see if SMTP-AUTH and TLS work properly, run the following command:

```bash
telnet mail.example.com 25
```

After you have established the connection to the Postfix mail server, type:

```bash
ehlo mail.example.com
```

If you see the following in the output, then everything is working perfectly. Type `quit` to exit.

```text
250-STARTTLS
250-AUTH LOGIN PLAIN
250-AUTH=LOGIN PLAIN
250 8BITMIME
```

## Troubleshooting

When problems arise, there are a few common ways to diagnose the cause.

### Escaping `chroot`

The Ubuntu Postfix package will, by default, install into a `chroot` environment for security reasons. This can add greater complexity when troubleshooting problems.

To turn off the `chroot` usage, locate the following line in the `/etc/postfix/master.cf` configuration file:

```text
smtp      inet  n       -       -       -       -       smtpd
```

Modify it as follows:

```text
smtp      inet  n       -       n       -       -       smtpd
```

You will then need to restart Postfix to use the new configuration. From a terminal prompt enter:

```bash
sudo service postfix restart
```

### SMTPS

If you need secure SMTP, edit `/etc/postfix/master.cf` and uncomment the following line:

```text
smtps     inet  n       -       -       -       -       smtpd
  -o smtpd_tls_wrappermode=yes
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
  -o milter_macro_daemon_name=ORIGINATING
```

### Log viewing

Postfix sends all log messages to `/var/log/mail.log`. However, error and warning messages can sometimes get lost in the normal log output so they are also logged to `/var/log/mail.err` and `/var/log/mail.warn` respectively.

To see messages entered into the logs in real time you can use the `tail -f` command:

```bash
tail -f /var/log/mail.err
```

### Increase logging detail

The amount of detail recorded in the logs can be increased via the configuration options. For example, to increase TLS activity logging set the `smtpd_tls_loglevel` option to a value from 1 to 4.

```bash
sudo postconf -e 'smtpd_tls_loglevel = 4'
```

Reload the service after any configuration change, to activate the new config:

```bash
sudo systemctl reload postfix.service
```

### Logging mail delivery

If you are having trouble sending or receiving mail from a specific domain you can add the domain to the `debug_peer_list` parameter.

```bash
sudo postconf -e 'debug_peer_list = problem.domain'
sudo systemctl reload postfix.service
```

### Increase daemon verbosity

You can increase the verbosity of any Postfix daemon process by editing the `/etc/postfix/master.cf` and adding a `-v` after the entry. For example, edit the `smtp` entry:

```bash
smtp      unix  -       -       -       -       -       smtp -v
```

Then, reload the service as usual:

```bash
sudo systemctl reload postfix.service
```

### Log SASL debug info

To increase the amount of information logged when troubleshooting SASL issues you can set the following options in `/etc/dovecot/conf.d/10-logging.conf`

```bash
auth_debug=yes
auth_debug_passwords=yes
```

As with Postfix, if you change a Dovecot configuration the process will need to be reloaded:

```bash
sudo systemctl reload dovecot.service
```

> **Note**:
> Some of the options above can drastically increase the amount of information sent to the log files. Remember to return the log level back to normal after you have corrected the problem -- then reload the appropriate daemon for the new configuration to take effect.

## References

Administering a Postfix server can be a very complicated task. At some point you may need to turn to the Ubuntu community for more experienced help.

- The [Postfix website](http://www.postfix.org/documentation.html) documents all available configuration options.
- O'Reilly's [Postfix: The Definitive Guide](http://shop.oreilly.com/product/9780596002121.do) is rather dated but provides deep background information about configuration options.
- The [Ubuntu Wiki Postfix](https://help.ubuntu.com/community/Postfix) page has more information from an Ubuntu context. 
- There is also a [Debian Wiki Postfix](https://wiki.debian.org/Postfix) page that's a bit more up to date; they also have a set of [Postfix Tutorials](https://wiki.debian.org/Postfix/Tutorials) for different Debian versions.
- Info on how to [set up mailman3 with postfix](https://mailman.readthedocs.io/en/latest/src/mailman/docs/mta.html#postfix).
