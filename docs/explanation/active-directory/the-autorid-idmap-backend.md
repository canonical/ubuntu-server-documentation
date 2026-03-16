---
myst:
  html_meta:
    description: "Learn about the AutoRID IDMap backend for simplified UID/GID allocation in Active Directory environments, particularly multidomain deployments."
---

(the-autorid-idmap-backend)=
# The AutoRID IDMap backend

The {manpage}`idmap_autorid(8)` identity mapping backend, like the `rid` one, also provides an algorithmic mapping between SIDs and Linux IDs, with the advantage that it can also automatically cope with Active Directory deployed across multiple domains. There is no need to pre-allocate ranges for each specific existing or future domain. Some planning is required, though:

- Range: the first and last ID that will be allocated on the Linux side by this backend. This includes all possible domains.
- RangeSize: how many IDs to allocate to each domain.

Let's see an example:

    [global]
        ...
        security = ads
        realm = EXAMPLE.INTERNAL
        workgroup = EXAMPLE
        ...
        idmap config * : backend = autorid
        # 1,000,000 - 19,999,999
        idmap config * : range   = 1000000 - 19999999
        # 1,000,000
        idmap config * : rangesize = 1000000

The configuration above gives us 19 domains (or slots) with the capacity of 1 million IDs in each:
- first slot: IDs from `1000000` up to `1999999`
- second slot: IDs from `2000000` up to `2999999`
- ...
- 19th slot (last): IDs from `19000000` up to `19999999`

![domain-slots-2|794x188](https://assets.ubuntu.com/v1/346983ee-domain-slots-2.png)


Which domain will get which slot? That is **not deterministic**. It will basically be a first come, first serve. Furthermore, if a domain exhausts the available IDs from a slot, an extension slot will be used, in which case the domain will be using two (possibly non-consecutive even) slots.

This also means that a persistent database is required to record which domain goes into which slot. This is managed automatically by the `autorid` backend in the `autorid.tdb` file.

```{note}
The `autorid.tdb` domain mapping database file is kept in `/var/lib/samba/` and should be backed up regularly.
```

## Pros and cons of the AutoRID backend

Let's examine the pros and cons of the `idmap_autorid` backend, and which scenarios are a better fit for it.

Pros:
- Automatic handling of trusted domains
- Simple initial planning, only done once

Cons:
- Non-deterministic SID to ID mapping with multiple domains, even if the same IDMap config settings are used for all domain-joined systems
- Extra concern to backup the domain mapping database file

So when to use the `idmap_autorid` backend?
- Multiple domains are involved via trust relationships, and the stability of IDs is not required on the joined systems.
- Single domain systems can also benefit from the easier and simpler up-front configuration.
- If you need to share files owned by domain users via NFS or another mechanism which relies on stability of IDs, then this backend must not be used.
