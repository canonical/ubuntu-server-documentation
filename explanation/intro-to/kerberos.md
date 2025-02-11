(introduction-to-kerberos)=
# Introduction to Kerberos


Kerberos is a network authentication system based on the principal of a trusted third party. The other two parties being the user and the service the user wishes to authenticate to. Not all services and applications can use Kerberos, but for those that can, it brings the network environment one step closer to being Single Sign On (SSO).

This section covers installation and configuration of a Kerberos server, and some example client configurations.

## Overview

If you are new to Kerberos there are a few terms that are good to understand before setting up a Kerberos server. Most of the terms will relate to things you may be familiar with in other environments:

  - *Principal:* any users, computers, and services provided by servers need to be defined as Kerberos Principals.

  - *Instances:* are a variation for service principals. For example, the principal for an NFS service will have an instance for the hostname of the server, like `nfs/server.example.com@REALM`. Similarly admin privileges on a principal use an instance of `/admin`, like `john/admin@REALM`, differentiating it from `john@REALM`. These variations fit nicely with ACLs.

  - *Realms:* the unique realm of control provided by the Kerberos installation. Think of it as the domain or group your hosts and users belong to. Convention dictates the realm should be in uppercase. By default, Ubuntu will use the {term}`DNS` domain converted to uppercase (`EXAMPLE.COM`) as the realm.

  - *Key Distribution Center:* (KDC) consist of three parts: a database of all principals, the authentication server, and the ticket granting server. For each realm there must be at least one KDC.

  - *Ticket Granting Ticket:* issued by the Authentication Server (AS), the Ticket Granting Ticket (TGT) is encrypted in the user's password which is known only to the user and the KDC. This is the starting point for a user to acquire additional tickets for the services being accessed.

  - *Ticket Granting Server:* (TGS) issues service tickets to clients upon request.

  - *Tickets:* confirm the identity of the two principals. One principal being a user and the other a service requested by the user. Tickets establish an encryption key used for secure communication during the authenticated session.

  - *Keytab Files:* contain encryption keys for a service or host extracted from the KDC principal database.

To put the pieces together, a Realm has at least one KDC, preferably more for redundancy, which contains a database of Principals. When a user principal logs into a workstation that is configured for Kerberos authentication, the KDC issues a Ticket Granting Ticket (TGT). If the user supplied credentials match, the user is authenticated and can then request tickets for Kerberized services from the Ticket Granting Server (TGS). The service tickets allow the user to authenticate to the service without entering another username and password.

## Resources

  - For more information on MIT's version of Kerberos, see the [MIT Kerberos](http://web.mit.edu/Kerberos/) site.

  - Also, feel free to stop by the *\#ubuntu-server* and *\#kerberos* IRC channels on [Libera.Chat](https://libera.chat/) if you have Kerberos questions.

 - [Another guide for installing Kerberos on Debian, includes PKINIT](http://techpubs.spinlocksolutions.com/dklar/kerberos.html)
