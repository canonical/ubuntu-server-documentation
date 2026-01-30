---
myst:
  html_meta:
    description: Configure mail services on Ubuntu Server with installation and configuration guides for Postfix, Exim4, and Dovecot.
---

(how-to-mail-services)=
# Mail services

Sending email from one person to another over a network or the Internet requires:

1. The sender's email client (**Mail User Agent**) sends the message.
2. One or more **Mail Transfer Agents** (MTA) to transfer the message.
3. The final MTA sends the message to a **Mail Delivery Agent** (MDA) for delivery to the recipient's inbox.
4. Finally, the recipient's email client retrieves the message, usually via a **POP3** or **IMAP** server.

These systems must all be configured correctly to successfully deliver a message.

## Mail User Agent

[Thunderbird](https://www.thunderbird.net/) is the default Mail User Agent (email client) used by Ubuntu. It comes pre-installed on all Ubuntu machines from Ubuntu 16.04 LTS (Xenial) onward.

If you need to install Thunderbird manually, [this short guide](https://snapcraft.io/install/thunderbird/ubuntu) will walk you through the steps. 

## Mail Transfer Agent

On Ubuntu, [Postfix](https://www.postfix.org/) is the default supported MTA. It is compatible with the [sendmail](https://www.authsmtp.com/sendmail/index.html) MTA.  
  
* {ref}`Install Postfix <install-postfix>` explains how to install and configure Postfix, including how to configure SMTP for secure communications.

[Exim4](https://www.exim.org/) can be installed in place of sendmail, although its configuration is quite different. 

* {ref}`Install Exim4 <install-exim4>` explains how to install and configure Exim4 on Ubuntu.
  
```{toctree}
:hidden:

Install Postfix <mail-services/install-postfix>
Install Exim4 <mail-services/install-exim4>
```
    
## Mail Delivery Agent

[Dovecot](https://dovecot.org/) is an MDA written with security primarily in mind. It supports the [mbox](https://en.wikipedia.org/wiki/Mbox) and [Maildir](https://en.wikipedia.org/wiki/Maildir) mailbox formats. 
  
* {ref}`Install Dovecot <install-dovecot>` explains how to set up Dovecot as an IMAP or POP3 server

```{toctree}
:hidden:

Install Dovecot <mail-services/install-dovecot>
```
