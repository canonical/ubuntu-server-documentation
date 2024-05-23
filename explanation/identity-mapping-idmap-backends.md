# Identity Mapping (idmap) backends

In order to have Domain users and groups from an Active Directory system appear in an Ubuntu system as valid, they need to have Linux specific attributes. Some of these attributes map directly to equivalent ones in Active Directory, some need to be translated to something else, and others do not exist at all. This is the problem that the Identity Mapping Backends (`idmap`) try to solve.

There are basically three idmap backends to chose from:
- [ad](https://manpages.ubuntu.com/manpages/noble/man8/idmap_ad.8.html): requires that Active Directory be augmented with RFC-2307 attributes
- [rid](https://manpages.ubuntu.com/manpages/noble/man8/idmap_rid.8.html): algorithmic user/group id generation, manual domain configuration
- [autorid](https://manpages.ubuntu.com/manpages/noble/man8/idmap_autorid.8.html): algorithmic user/group id generation, automatic domain configuration

Of these, the simplest ones to use are *rid* and *autorid*, because they require no changes to Active Directory. These are the ones we will examine next.

There is another idmap backend that we need to introduce, not related to Active Directory integration, but necessary in some cases: the *tdb* (Trivial Data Base) backend. The [idmap_tdb](https://manpages.ubuntu.com/manpages/noble/man8/idmap_tdb.8.html) backend is an *allocating backend* that stores the mappings on a persistent database on disk. It is needed whenever the mapping is not deterministic, and is instead done on a first come, first serve, order. Configurations using the *idmap_rid* backend need to be supported by the *idmap_tdb* backend as well, as will be shown later.

To better understand how these mapping mechanisms work, it helps to have a quick refresher on the typical [user ID ranges on an Ubuntu/Debian system](https://www.debian.org/doc/debian-policy/ch-opersys.html#uid-and-gid-classes):
- `0-99`: builtin global allocations, shipped in the `base-passwd` package
- `100-999`: dynamically allocated system users and groups, typically created by packages for services as they are installed
- `1000-59999`: dynamically allocated normal user/group accounts (\*)
- `60000-64999`: other global allocations
- `65000-65533`: reserved
- `65534`: the `nobody` user, and corresponding `nogroup` group (\*)
- `65536-4294967293`: dynamically allocated user/group accounts
- `4294967294` and `4294967295`: do not use

Most of these ranges are configured in `/etc/adduser.conf`, and the above are the default values.

The Active Directory domain users and groups need to fit somewhere, and the largest block available is `65536-4294967293`, so that is typically what is used.

See next:

* [The rid idmap backend](the-rid-idmap-backend.md)
* [The autorid idmap backend](the-autorid-idmap-backend.md)
