---
myst:
  html_meta:
    description: "Understand different methods for integrating Ubuntu Server with Active Directory, including SSSD, Samba, and Winbind options."
---

(choosing-an-integration-method)=
# Choosing an integration method

There are multiple mechanisms to join an Ubuntu system to an Active Directory tree (single domain) or a forest (multiple domains with trust relationships). It's important to understand the features, pros, and cons, of each method, and cross reference those with what is the objective of the integration.

Three main criteria need to be evaluated:
* forest or single domain: Is the Active Directory deployment being joined composed of a single domain, or multiple domains (forest)?
* member server or workstation: Is the Ubuntu system that is being joined to Active Directory going to be a member server (it provides authentication and shares), or just a workstation/desktop which will not share files via the SMB protocol? If a workstation is also going to share files via SMB, then consider it a member server.
* Deterministic Linux ID: is it important that the same Active Directory user obtains the same Linux ID on all joined systems? For example, if NFS exports will be used between the joined systems.

| Requirement/Method       | SSSD | `idmap_rid` | `idmap_autorid` |
|--------------------------|:----:|:-----------:|:---------------:|
| Deterministic ID         | Y    |    Y        |      N          |
| Undetermined  ID         | Y    |    Y        |      Y          |
| Member server            | N    |    Y        |      Y          |
| Not a member server      | Y    |    Y        |      Y          |
| AD multi-domain (forest) | N    |    N(\*)    |      Y          |
| AD single domain         | Y    |    Y        |      Y          |

(\*) The *`idmap_rid`* choice for multi-domain Active Directory is doable, but with important caveats that are better explained in {ref}`Joining a forest with the rid backend <join-a-forest-with-the-rid-backend>`.

Before going into the details of each integration method, it's a good idea to familiarise yourself with the other basic concepts of Active Directory integration. These are shown next:

* {ref}`Security identifiers <security-identifiers-sids>`
* {ref}`Identity mapping backends <identity-mapping-idmap-backends>`
* {ref}`The rid idmap backend <the-rid-idmap-backend>`
* {ref}`The autorid idmap backend <the-autorid-idmap-backend>`
