(security-identifiers-sids)=
# Security identifiers (SIDs)

One of the more challenging aspects of integrating with Active Directory is called Identity Mapping. Windows entities (users, groups, computers, etc) have identifiers called SID, which stands for *Security IDentifier*. This is not just a number: it has a structure and is composed of several values. Linux users and groups identifiers, on the other hand, are a single number..

```{note}
For a full explanation of what an SID is, and how they are structured and allocated, please refer to [Understand Security Identifiers](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers).
```

For the purposes of integration, the more important fields of a SID are the *Domain Identifier* and the *Relative Identifier*:

    S-1-5-<Domain-Identifier>-<Relative-Identifier>

Here are some examples of what an SID looks like:
- `S-1-5-32-544`: this is the so called well-known SID of the built-in (`32`) Administrators (`544`) group
- `S-1-5-21-1004336348-1177238915-682003330-512`: a Domain Admins group (`512`) in a specific domain (`21-1004336348-1177238915-682003330`)
- `S-1-5-21-1132786674-3270659749-157314226-512`: also a Domain Admins group (`512`), but in another domain (`21-1132786674-3270659749-157314226`)
- `S-1-5-21-1132786674-3270659749-157314226-1103`: a user with *Relative Identifier* (RID) of `1103`, in the domain `21-1132786674-3270659749-157314226`

Within a domain, the *Domain Identifier* remains the same, and the *Relative Identifier* is what distinguishes the users and groups of that domain. In other words, the *Domain Admins* group will always have a *Relative Identifier* (RID) of `512` in all domains, but the *Domain Identifier* will be different. And thus we have a unique global *Secure Identifier*.

In order to integrate an Ubuntu system with Active Directory, some sort of mapping is needed between the SIDs on the AD site, and the numeric identifiers on the Linux side. At first glance, the RID component of the SID looks like a very good candidate, and indeed it is used by most mapping mechanisms, but it's not truly unique since it misses the Domain Identifier.

The *winbind* package, part of the Samba suite of applications, is capable of performing a mapping between SIDs and Linux IDs, and has several mechanisms to do so, each with some pros and cons. These mechanisms are called *Identity Mapping Backends*, and how to choose one will depend on the type of domain being joined (single, forest, etc), and what level of integration we want on the Ubuntu System.

See next:

* [Identity mapping backends](identity-mapping-idmap-backends.md)
* [The rid idmap backend](the-rid-idmap-backend.md)
* [The autorid idmap backend](the-autorid-idmap-backend.md)
