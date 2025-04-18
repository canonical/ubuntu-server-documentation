(the-rid-idmap-backend)=
# The rid idmap backend

The [rid](https://manpages.ubuntu.com/manpages/noble/man8/idmap_rid.8.html) idmap backend provides an algorithmic mapping between Linux uids/{term}`gids <GID>` and Active Directory SIDs. That means that a given SID will always map to the same uid/gid, and vice-versa, within the same domain.

To use this backend, we have to choose two or more ID ranges:
- a range for the domain we are joining
- another range to serve as a "catch all", which will store mappings for users and groups that might come from other domains, as well as the default built-in entries

Let's analyse an example configuration:

    [global]
        ...
        security = ads
        realm = EXAMPLE.INTERNAL
        workgroup = EXAMPLE
        ...
        idmap config * : backend       = tdb
        idmap config * : range         = 100000 - 199999

        idmap config EXAMPLE : backend = rid
        idmap config EXAMPLE : range   = 1000000 - 1999999

```{note}
This is not yet a complete configuration file, and is just illustrating the idmap configuration. More is needed to join an Active Directory domain.
```

This configuration is using two idmap backends, and carving out two ranges:
- `*` domain, or "default domain": any SID that is not mapped via another more specific idmap configuration will use this backend. Since this mapping is not deterministic, a database is needed to keep a record, hence the `tdb` backend is used.
- `EXAMPLE` domain: uses the *rid* idmap backend, and users from the `EXAMPLE` domain will be allocated IDs in the range of 1.000.000 to 1.999.999, that is, there is space for 1 million IDs. Since the mapping is deterministic, there is no need for a database.

![simple-rid-ranges|794x315, 75%](https://assets.ubuntu.com/v1/87c43d5d-simple-rid-ranges.png)



```{important}
Planning a range of IDs to be used for the mapping critically important. Such a range can never be reduced, just expanded (carefully!), and it must **NEVER** overlap with another allocated range.
```

Once this system is joined to the `EXAMPLE.INTERNAL` domain, users from that domain will be allocated corresponding Linux uids and gids from the specified range in a deterministic way, following a formula. As long as the above configuration is used in all Ubuntu systems joined to the domain, the same Active Directory user will always get the same Linux IDs in all those systems.

Things start to get more complicated if the `EXAMPLE.INTERNAL` domain establishes a trust relationship with another Active Directory domain. The correct way to handle this is to, *before*, add a new idmap configuration for that domain. For example:

    [global]
        ...
        security = ads
        realm = EXAMPLE.INTERNAL
        workgroup = EXAMPLE
        ...
        idmap config * : backend       = tdb
        idmap config * : range         = 100000 - 199999

        idmap config EXAMPLE : backend = rid
        idmap config EXAMPLE : range   = 1000000 - 1999999

        idmap config COMPANY : backend = rid
        idmap config COMPANY : range   = 2000000 - 2999999

This change is allocating a new range for the new `COMPANY` domain. Then, when the domain trust relationship is established between the Active Directory domains, the Ubuntu systems with this extra idmap configuration will know that users from the `COMPANY` belong to the range `2000000 - 2999999`.

If, however, the domain trust relationship is established between `EXAMPLE` and `COMPANY` before the new idmap range is configured, then the users and groups from `COMPANY` will have their ID allocations taken from the default domain "`*`", which is NOT deterministic and is done on a first come, first serve, basis. This means that the **same** Active Directory user from domain `COMPANY` connecting to different Ubuntu systems will likely get a **different** Linux ID.

## Pros and Cons of the rid backend
We now have enough information to understand the pros and cons of the *`idmap_rid`* backend, and which scenarios are a better fit for it.

Pros:
- Stable mapping of SIDs to IDs within a single domain: all Ubuntu systems sharing the same configuration will arrive at the same mapping for Active Directory users.

Cons:
- extra config for trusted domains: you must add *idmap config* entries for all trusted domains, and deploy these changes to all joined systems before the domains establish a new trust relationship, or else you risk having users of the new trusted domain be allocated IDs from the default backend ("`*`") range.

With that in mind, *`idmap_rid`* is best used in the following scenarios:
- Single domain with no trust relationships
- If there are trust relationships, they are fairly static, and well planned in advance, and there is a configuration file management system in place to easily update the `smb.conf` config file with the new idmap config lines across all joined systems.
- Stability of Linux IDs across multiple joined systems is important. For example, NFSv3 is being used.

Next:

* [The autorid idmap backend](the-autorid-idmap-backend.md)
