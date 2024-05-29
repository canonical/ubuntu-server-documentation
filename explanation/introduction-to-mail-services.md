# Introduction to mail services

The process of getting an email from one person to another over a network or the Internet involves many systems working together. Each of these systems must be correctly configured for the process to work. 

The sender uses a *Mail User Agent* (MUA), or email client, to send the message through one or more *Mail Transfer Agents* (MTA), the last of which will hand it off to a *Mail Delivery Agent* (MDA) for delivery to the recipient's mailbox, from which it will be retrieved by the recipient's email client, usually via a POP3 or IMAP server.

## Mail User Agent 

* **Thunderbird**
  The default MUA used by Ubuntu is [Thunderbird](https://www.thunderbird.net/). It comes pre-installed on all Ubuntu machines from Ubuntu 16.04 LTS (Xenial) onwards.
  
  If you need to install Thunderbird manually, [this short guide](https://snapcraft.io/install/thunderbird/ubuntu) will walk you through the steps. 

## Mail Transfer Agent

* **Postfix**
  On Ubuntu, [Postfix](https://www.postfix.org/) is the default supported MTA. It aims to be fast and secure, with flexibility in administration. It is compatible with the [sendmail](https://www.authsmtp.com/sendmail/index.html) MTA. 
  
  This guide explains [how to install and configure Postfix](../how-to/install-and-configure-postfix.md), including how to configure SMTP for secure communications.

* **Exim4**
  [Exim4](https://www.exim.org/) was developed at the University of Cambridge for use on Unix systems connected to the Internet. Exim can be installed in place of sendmail, although its configuration is quite different. 
  
  This guide explains [how to install and configure Exim4](../how-to/install-and-configure-exim4.md) on Ubuntu.

## Mail Delivery Agent

* **Dovecot**
  [Dovecot](https://www.dovecot.org/) is an MDA written with security primarily in mind. It supports the [mbox](https://en.wikipedia.org/wiki/Mbox) and [Maildir](https://en.wikipedia.org/wiki/Maildir) mailbox formats. 
  
  This guide explains [how to set up Dovecot](../how-to/install-and-configure-dovecot.md) as an IMAP or POP3 server.
