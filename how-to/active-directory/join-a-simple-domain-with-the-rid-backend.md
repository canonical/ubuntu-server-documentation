(join-a-simple-domain-with-the-rid-backend)=
# Join a simple domain with the rid backend

Let's expand on the configuration we had for the *rid* backend and complete the `/etc/samba/smb.conf` configuration file with the remaining details. We are joining a single domain called `EXAMPLE.INTERNAL`. The new configuration options were added at the end of the `[global]` section:

    [global]
        security = ads
        realm = EXAMPLE.INTERNAL
        workgroup = EXAMPLE
    
        idmap config * : backend       = tdb
        idmap config * : range         = 100000 - 199999
        idmap config EXAMPLE : backend = rid
        idmap config EXAMPLE : range   = 1000000 - 1999999

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

Right after saving `/etc/samba/smb.conf`, it's always good practice to run the `testparm` utility. It will perform a quick syntax check on the configuration file and alert you of any issues. Here is the output we get with the above configuration settings:

    Load smb config files from /etc/samba/smb.conf
    Loaded services file OK.
    Weak crypto is allowed by GnuTLS (e.g. NTLM as a compatibility fallback)

    Server role: ROLE_DOMAIN_MEMBER

    Press enter to see a dump of your service definitions
    (...)


During the domain join process, the tooling will attempt to update the DNS server with the hostname of this system. Since its IP is likely not yet registered in DNS, that's kind of a chicken and egg problem. It helps to, beforehand, set the hostname manually to the FQDN. For this example, we will use a host named `n1` in the `example.internal` domain:

    sudo hostnamectl hostname n1.example.internal

So that the output of `hostname -f` (and also just `hostname`) is `n1.example.internal`.

With the config file in place and checked, and all the other changes we made in the previous section, the domain join can be performed:

    $ sudo net ads join -U Administrator
    Password for [EXAMPLE\Administrator]:
    Using short domain name -- EXAMPLE
    Joined 'N1' to dns domain 'example.internal'

You can now revert the `hostnamectl` change from before, and set the hostname back to the short version, i.e., `n1` in this example:

    sudo hostnamectl hostname n1

As the last step of the process, the `winbind` service must be restarted:

    sudo systemctl restart winbind.service

## Verifying the join

The quickest way to test the integrity of the domain join is via the `wbinfo` command:

    $ sudo wbinfo -t
    checking the trust secret for domain EXAMPLE via RPC calls succeeded

The next verification step should be to actually try to resolve an existing username from the domain. In the `EXAMPLE.INTERNAL` domain, for example, we have some test users we can check:

    $ id jammy@example.internal
    uid=1001103(EXAMPLE\jammy) gid=1000513(EXAMPLE\domain users) groups=1000513(EXAMPLE\domain users),1001103(EXAMPLE\jammy)

Another valid syntax for domain users is prefixing the name with the domain, like this:

    $ id EXAMPLE\\jammy
    uid=1001103(EXAMPLE\jammy) gid=1000513(EXAMPLE\domain users) groups=1000513(EXAMPLE\domain users),1001103(EXAMPLE\jammy)

And finally, attempt a console login:

    n1 login: jammy@example.internal
    Password:
    Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.5.0-26-generic x86_64)
    (...)
    Creating directory '/home/EXAMPLE/jammy'.
    EXAMPLE\jammy@n1:~$

The output above also shows the automatic on-demand home directory creation, according to the template defined in `/etc/samba/smb.conf`.

> **Note**:
> The actual login name used can have multiple formats: `DOMAIN\user` at the terminal login prompt, `DOMAIN\\user` when referred to in shell scripts (note the escaping of the '`\`' character), and `user@domain` is also accepted.
