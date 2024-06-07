(introduction-to-samba)=
# Samba

Computer networks are often comprised of diverse systems. While operating a network made up entirely of Ubuntu desktop and server computers would definitely be fun, some network environments require both Ubuntu and Microsoft Windows systems working together in harmony. 

This is where [Samba](https://www.samba.org) comes in! Samba provides various tools for configuring your Ubuntu Server to share network resources with Windows clients. In this overview, we'll look at some of the key principles, how to install and configure the tools available, and some common Samba use cases.

## Samba functionality

There are several services common to Windows environments that your Ubuntu system needs to integrate with in order to set up a successful network. These services share data and configuration details of the computers and users on the network between them, and can each be classified under one of three main categories of functionality. 

### File and printer sharing services

These services use the Server Message Block (SMB) protocol to facilitate the sharing of files, folders, volumes, and the sharing of printers throughout the network. 

- **File server**
Samba can be [configured as a file server](../how-to/samba-as-a-file-server.md) to share files with Windows clients - our guide will walk you through that process.

- **Print server**
Samba can also be [configured as a print server](../how-to/samba-as-a-print-server.md) to share printer access with Windows clients, as detailed in this guide. 

### Directory services

These services share vital information about the computers and users of the network. They use technologies like the Lightweight Directory Access Protocol (LDAP) and Microsoft Active Directory. 

- **Microsoft Active Directory**
An Active Directory domain is a collection of users, groups, or hardware components within a Microsoft Active Directory network. This guide will show you how to set up your server as a [member of an Active Directory domain](../how-to/member-server-in-an-active-directory-domain.md).

- NT4 Domain Controller *(deprecated)*
This guide will show you how to configure your Samba server to appear [as a Windows NT4-style domain controller](../how-to/nt4-domain-controller-legacy.md).

- OpenLDAP backend *(deprecated)*
This guide will show you how to integrate Samba with [LDAP in Windows NT4 mode](../how-to/openldap-backend-legacy.md). 

### Authentication and access

These services establish the identity of a computer or network user, and determine the level of access that should be granted to the computer or user. The services use such principles and technologies as file permissions, group policies, and the Kerberos authentication service.

- **Share access controls**
This article provides more details on [controlling access to shared directories](../how-to/share-access-controls.md).

- **AppArmor profile for Samba**
This guide will briefly cover how to [set up a profile for Samba](../how-to/samba-apparmor-profile.md) using the Ubuntu security module, AppArmor.

- **Mounting CIFS shares permanently**
  This guide will show you [how to set up Common Internet File System (CIFS) shares](../how-to/how-to-mount-cifs-shares-permanently.md) to automatically provide access to network files and resources.
