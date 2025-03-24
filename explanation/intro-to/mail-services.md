(introduction-to-mail-services)=
# Introduction to mail servers

Sending email from one person to another over a network or the Internet requires many systems to work together. First, the sender's email client (**Mail User Agent**) sends the message. Then one or more **Mail Transfer Agents** (MTA) transfers the message. The final MTA sends the message to a **Mail Delivery Agent** (MDA) for delivery to the recipient's inbox. Finally, the recipient's email client retrieves the message, usually via a **POP3** or **IMAP** server. These systems must all be configured correctly to successfully deliver a message.

## Mail User Agent

### Thunderbird

[Thunderbird](https://www.thunderbird.net/) is the default Mail User Agent (email client) used by Ubuntu. It comes pre-installed on all Ubuntu machines from Ubuntu 16.04 LTS (Xenial) onwards.
  
  If you need to install Thunderbird manually, [this short guide](https://snapcraft.io/install/thunderbird/ubuntu) will walk you through the steps. 

## Mail Transfer Agent

### Postfix

On Ubuntu, [Postfix](https://www.postfix.org/) is the default supported MTA. It aims to be fast and secure, with flexibility in administration. It is compatible with the [sendmail](https://www.authsmtp.com/sendmail/index.html) MTA.  
  
  This guide explains {ref}`how to install and configure Postfix <install-postfix>`, including how to configure SMTP for secure communications.

### Exim4

[Exim4](https://www.exim.org/) was developed at the University of Cambridge for use on Unix systems connected to the Internet. Exim can be installed in place of sendmail, although its configuration is quite different. 
  
  This guide explains {ref}`how to install and configure Exim4 <install-exim4>` on Ubuntu.

## Mail Delivery Agent

### Dovecot
[Dovecot](https://www.dovecot.org/) is an MDA written with security primarily in mind. It supports the [mbox](https://en.wikipedia.org/wiki/Mbox) and [Maildir](https://en.wikipedia.org/wiki/Maildir) mailbox formats. 
  
  This guide explains {ref}`how to set up Dovecot <install-dovecot>` as an IMAP or POP3 server.
