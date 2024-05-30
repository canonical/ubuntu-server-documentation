(join-a-forest-with-the-rid-backend)=
# Join a forest with the rid backend

It's also possible to join an Active Directory forest using the *rid* identity mapping backend. To better understand what is involved, and why it is tricky, let's reuse the example where we joined a single domain with this backend:

    [global]
        security = ads
        realm = EXAMPLE.INTERNAL
        workgroup = EXAMPLE

        idmap config * : backend       = tdb
        # 100,000 - 199,999
        idmap config * : range         = 100000 - 199999
        idmap config EXAMPLE : backend = rid
        # 1,000,000 - 1,999,999
        idmap config EXAMPLE : range   = 1000000 - 1999999

![simple-rid-ranges|600x238, 100%](https://assets.ubuntu.com/v1/87c43d5d-simple-rid-ranges.png)


With this configuration, we are expected to join the *EXAMPLE.INTERNAL* domain, and have given it a range of 1 million IDs starting with the ID `1000000` (1,000,000). There is also the mandatory reserved range for the default domain, represented by the identity mapping configuration for "`*`", which has a smaller range of 100,000 IDs, starting at `100000` (100,000).

The `testparm` utility is happy with this configuration, and there is no overlap of ID ranges:

    $ testparm
    Load smb config files from /etc/samba/smb.conf
    Loaded services file OK.
    Weak crypto is allowed by GnuTLS (e.g. NTLM as a compatibility fallback)

    Server role: ROLE_DOMAIN_MEMBER

We next adjust the hostname and perform the join:

    $ sudo hostnamectl hostname n3.example.internal

    $ hostname
    n3.example.internal

    $ hostname -f
    n3.example.internal

    $ sudo net ads join -U Administrator
    Password for [EXAMPLE\Administrator]:
    Using short domain name -- EXAMPLE
    Joined 'N3' to dns domain 'example.internal'

    $ sudo hostnamectl hostname n3
    $ sudo systemctl restart winbind.service

A quick check shows that the users from *EXAMPLE.INTERNAL* are recognized:

    $ id jammy@example.internal
    uid=1001103(EXAMPLE\jammy) gid=1000513(EXAMPLE\domain users) groups=1000513(EXAMPLE\domain users),1001103(EXAMPLE\jammy)

But what happens if this single domain establishes a trust relationship with another domain, and we don't modify the `/etc/samba/smb.conf` file to cope with that? Where will the users from the new trusted domain get their IDs from? Since there is no specific idmap configuration for the new trusted domain, its users will get IDs from the default domain:

    $ id noble@mydomain.internal
    uid=100000(MYDOMAIN\noble) gid=100000(MYDOMAIN\domain users) groups=100000(MYDOMAIN\domain users)

Oops. That is from the much smaller range 100,000 - 199,999, reserved for the catch-all default domain. Furthermore, if yet another trust relationship is established, those users will also get their IDs from this range, mixing multiple domains up in the same ID range, in whatever order they are being looked up.

If above we had looked up another user instead of *noble@mydomain.internal*, that other user would have been given the ID 100000. There is no deterministic formula for the default domain ID allocation, like there is for the *rid* backend. In the default domain, IDs are allocated on a first come, first serve basis.

To address this, we can add another *idmap config* configuration for the *rid* backend, giving the new domain a separate range:

    [global]
        security = ads
        realm = EXAMPLE.INTERNAL
        workgroup = EXAMPLE

        idmap config * : backend       = tdb
        # 100,000 - 199,999
        idmap config * : range         = 100000 - 199999
        idmap config EXAMPLE : backend = rid
        # 1,000,000 - 1,999,999
        idmap config EXAMPLE : range   = 1000000 - 1999999

        # MYDOMAIN.INTERNAL idmap configuration
        idmap config MYDOMAIN : backend = rid
        # 2,000,000 - 2,999,999
        idmap config MYDOMAIN : range   = 2000000 - 2999999

![forest-rid-ranges|799x238](https://assets.ubuntu.com/v1/42506c6d-forest-rid-ranges.png)


With this configuration, nothing changed for the *EXAMPLE.INTERNAL* users, as expected:

    $ id jammy@example.internal
    uid=1001103(EXAMPLE\jammy) gid=1000513(EXAMPLE\domain users) groups=1000513(EXAMPLE\domain users),1001103(EXAMPLE\jammy)

But the users from the trusted domain *MYDOMAIN.INTERNAL* will get their IDs allocated from the 2,000,000 - 2,999,999 range, instead of the default one:

    $ id noble@mydomain.internal
    uid=2001104(MYDOMAIN\noble) gid=2000513(MYDOMAIN\domain users) groups=2000513(MYDOMAIN\domain users),2001104(MYDOMAIN\noble)

And this allocation, which is using the *rid* backend, is deterministic.

Problem solved! Well, until another trust relationship is established, then we have to allocate another range for it.

So is it possible to use the *rid* identity mapping backend with an Active Directory forest, with multiple domains? Yes, but following these steps **BEFORE** establishing any new trust relationship:
- plan an ID range for the new domain
- update **ALL** systems that are using the *rid* idmap backend with the new range configuration for the new domain
- restart winbind on **ALL** such systems
- then the new trust relationship can be established

If a system is missed, and doesn't have an idmap configuration entry for the new domain, the moment a user from that new domain is looked up, it will be assigned an ID from the default domain, which will be non-deterministic and different from the ID assigned to the same user in another system which had the new idmap configuration entry. Quite a mess. Unless the different ID is not important, in which case it's much simpler to just use the *autorid* identity mapping backend.
