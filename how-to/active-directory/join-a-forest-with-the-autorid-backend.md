(join-a-forest-with-the-autorid-backend)=
# Join a forest with the autorid backend

Joining a more complex Active Directory forest with the autorid backend is very similar to the rid backend. The only difference is in the idmap configuration in `/etc/samba/smb.conf`:

    [global]
        security = ads
        realm = EXAMPLE.INTERNAL
        workgroup = EXAMPLE

        idmap config * : backend = autorid
        # 1,000,000 - 19,999,999
        idmap config * : range   = 1000000 - 19999999
        # 1,000,000
        idmap config * : rangesize = 1000000

        # allow logins when the DC is unreachable
        winbind offline logon = yes
        # this *can* be yes if there is absolute certainty that there is only a
        # single domain involved
        winbind use default domain = no
        # setting these enumeration options to yes has a high performance impact
        # and can cause instabilities
        winbind enum groups = no
        winbind enum users = no
        winbind refresh tickets = yes
        # if domain users should be allowed to login, they will need a login shell
        template shell = /bin/bash
        # the home directory template for domain users
        template homedir = /home/%D/%U
        kerberos method = secrets and keytab

Note that there is no specific domain mentioned in the idmap configuration. That's because the autorid backend does the allocations on demand, according to the defined slots. The configuration above defines the following:
- 1 million IDs per slot
- 19 slots (or domains)
- full ID range, covering all slots, is from 1,000,000 to 19,999,999

That being said, the machine still needs to be joined to a specific domain of that forest, and in this example that will be *EXAMPLE.INTERNAL*.

Running the recommended `testparm` command gives us confidence that the configuration is at least free from syntax and other logical errors:

    $ testparm
    Load smb config files from /etc/samba/smb.conf
    Loaded services file OK.
    Weak crypto is allowed by GnuTLS (e.g. NTLM as a compatibility fallback)

    Server role: ROLE_DOMAIN_MEMBER

    Press enter to see a dump of your service definitions

Like with the *rid* idmap backend, if this system is not yet in the AD {term}`DNS` server, it's best to change its {term}`hostname` (including the short hostname) to be the fully qualified domain name (FQDN), as that will allow the joining procedure to also update the DNS records, if so allowed by the AD server (normally it is).

For this example, the system's hostname is `n2` in the `example.internal` domain, so the FQDN is `n2.example.internal`:

    sudo hostnamectl hostname n2.example.internal

Now the domain join can be performed:

    $ sudo net ads join -U Administrator
    Password for [EXAMPLE\Administrator]:
    Using short domain name -- EXAMPLE
    Joined 'N2' to dns domain 'example.internal'

And we can revert the hostname change:

    sudo hostnamectl hostname n2

If the DNS server was updated correctly (and there were no errors about that in the join output above), then the hostname should now be correctly set, even though we have just the short name in `/etc/hostname`:

    $ hostname
    n2

    $ hostname -f
    n2.example.internal

The last step is to restart the *winbind* service:

    sudo systemctl restart winbind.service

## Verifying the join
The quickest way to test the integrity of the domain join is via the *wbinfo* command:

    $ sudo wbinfo -t
    checking the trust secret for domain EXAMPLE via RPC calls succeeded

The next verification step should be to actually try to resolve an existing username from the domain. In the *EXAMPLE.INTERNAL* domain, for example, we have some test users we can check:

	$ id jammy@example.internal
	uid=2001103(EXAMPLE\jammy) gid=2000513(EXAMPLE\domain users) groups=2000513(EXAMPLE\domain users),2001103(EXAMPLE\jammy)

If you compare this with the *rid* domain join, note how the ID that the *jammy* user got is different. That's why it's important to correctly chose an idmap backend, and correctly assess if deterministic IDs are important for your use case or not.

Another valid syntax for domain users is prefixing the name with the domain, like this:

	$ id EXAMPLE\\jammy
	uid=2001103(EXAMPLE\jammy) gid=2000513(EXAMPLE\domain users) groups=2000513(EXAMPLE\domain users),2001103(EXAMPLE\jammy)

And here we try a console login:

    n2 login: jammy@example.internal
    Password:
    Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.5.0-26-generic x86_64)
    (...)
    Creating directory '/home/EXAMPLE/jammy'.
    EXAMPLE\jammy@n1:~$

The output above also shows the automatic on-demand home directory creation, according to the template defined in `/etc/samba/smb.conf`.

Since we joined a forest, we should also be able to verify users from other domains in that forest. For example, in this example, the domain *MYDOMAIN.INTERNAL* is also part of the forest, and we can verify its users:

	$ id noble@mydomain.internal
	uid=3001104(MYDOMAIN\noble) gid=3000513(MYDOMAIN\domain users) groups=3000513(MYDOMAIN\domain users),3001104(MYDOMAIN\noble)

	$ id MYDOMAIN\\noble
	uid=3001104(MYDOMAIN\noble) gid=3000513(MYDOMAIN\domain users) groups=3000513(MYDOMAIN\domain users),3001104(MYDOMAIN\noble)

A console login also works:

	n2 login: noble@mydomain.internal
	Password:
	Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-31-generic x86_64)
	(...)
	Creating directory '/home/MYDOMAIN/noble'.
	MYDOMAIN\noble@n2:~$

Notice how the domain name being part of the home directory path is useful: it separates the users from different domains, avoiding collisions for the same username.

```{note}
The actual login name used can have multiple formats: `DOMAIN\user` at the terminal login prompt, `DOMAIN\\user` when refered to in shell scripts (note the escaping of the '`\`' character), and `user@domain` is also accepted.
```
