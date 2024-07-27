(how-to-provision-samba-ad-controller)=
# Provisioning a Samba Active Directory Domain Controller
A Samba Active Directory Domain Controller (also known as just Samba AD/DC) is a server running Samba services that can provide authentication to domain users and computers, linux or Windows. It should be dedicated to authentication and authorization services, and not provide file or print services: that should be the role of member servers joined to the domain.

```{seealso}
For more information on why the Samba AD/DC server should not be used to provide file and print services, please refer to this [list of reasons and caveats in the Samba Wiki](https://wiki.samba.org/index.php/Setting_up_Samba_as_an_Active_Directory_Domain_Controller#Using_the_Domain_Controller_as_a_File_Server_(Optional)).
```

This guide will show how to bootstrap a Samba AD/DC server and verify it's functioning properly.

## Installation
This command will install the packages necessary for bootstrapping and testing the Samba AD/DC services:

    sudo apt install samba-ad-dc krb5-user bind9-dnsutils

Note that the installation of `krb5-user` might prompt some questions. It's fine to answer with just the default values (just hit ENTER) at this stage, including when it asks about what the Kerberos realm and servers are.

Next, we should make sure that the normal Samba services `smbd`, `nmbd`, and `windind`, are disabled:

    sudo systemctl disable --now smbd nmbd winbind
    sudo systemctl mask smbd nmbd winbind

And enable the Samba AD/DC service, but without starting it yet:

    sudo systemctl unmask samba-ad-dc
    sudo systemctl enable samba-ad-dc

```{note}
A Samba AD/DC deployment represents a collection of services connected to each other, and needs its own specific systemd service unit.
```

The Samba AD/DC provisioning tool will want to create a new Samba configuration file, dedicated to the AD/DC role, but it will refrain from replacing an existing one. We have to therefore move it away before continuing:

    sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.orig

## Provisioning
With the packages installed, the Samba AD/DC service can be provisioned. For this how-to, we will use the following values:

- Domain: `EXAMPLE`
- Realm: `EXAMPLE.INTERNAL`
- Administrator password: `Passw0rd` (pick your own)

To perform the provisioning, run this command:

    sudo samba-tool domain provision \
        --domain EXAMPLE \
        --realm=EXAMPLE.INTERNAL \
        --adminpass=Passw0rd \
        --server-role=dc \
        --use-rfc2307 \
        --dns-backend=SAMBA_INTERNAL

If you omit the `--adminpass` option, a random password will be chosen and be included in the provisioning output. Be sure to save it!

```{warning}
Providing passwords in the command line is generally unsafe. Other users on the system who can see the process listing can spot the password, and it will also be saved in the shell history, unless the command starts with a blank space.
```

The command will take a few seconds to run, and will output a lot of information. In the end, it should be like this (long lines truncated for better readability):

    (...)
    INFO ... #498: Server Role:     active directory domain controller
    INFO ... #499: Hostname:        ad
    INFO ... #500: NetBIOS Domain:  EXAMPLE
    INFO ... #501: DNS Domain:      example.internal
    INFO ... #502: DOMAIN SID:      S-1-5-21-2373640847-2123283686-338028823

If you didn't use the `--adminpass` option, the administrator password will be part of the output above in a line like this:

    INFO ... #497: Admin password:  sbruR-Py>];k=KDn1H58PB#

## Post-installation steps
The AD/DC services are not running yet. Some post-installation steps are necessary before the services can be started.

First, adjust `dns forwarder` in `/etc/samba/smb.conf` to point at your DNS server. It will be used for all queries that are not local to the Active Directory domain we just deployed (`EXAMPLE.INTERNAL`). The provisioning script simply copied the server IP from `/etc/resolv.conf` to this parameter, but if we leave it like that, it will point back to itself:

    [global]
        dns forwarder = 127.0.0.53

If unsure, it's best to use the current DNS server this system is already using. That can be seen with the `resolvectl status` command. Look for the `Current DNS Server` line and note the IP address:

    Global
             Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
      resolv.conf mode: stub

    Link 2 (enp5s0)
        Current Scopes: DNS
             Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
    Current DNS Server: 10.10.17.1
           DNS Servers: 10.10.17.1
            DNS Domain: lxd

In the above example, the DNS server is `10.10.17.1`, so that should be used in `/etc/samba/smb.conf`'s `dns forwarder`:

    [global]
        dns forwarder = 10.10.17.1

Next, we need to be sure this system will be using the Samba DNS server for its queries, and for that we need to adjust `/etc/resolv.conf`. That file will be a symlink, so instead of just rewriting its contents, first we have to remove it:

    sudo unlink /etc/resolv.conf

Note: this will make sudo issue complaints about DNS from this point on, until the Samba DNS service is up and running.

And now recreate the file `/etc/resolv.conf` with this content:

    nameserver 127.0.0.1
    search example.internal

Stop and disable `systemd-resolved` as the resolver will now be using the Samba DNS server directly:

    sudo systemctl disable --now systemd-resolved

Finally, we need to update `/etc/krb5.conf` with the content generated by the Samba provisioning script. Since this system is dedicated to being a Samba AD/DC server, we can just copy the generated file over:

    sudo cp -f /var/lib/samba/private/krb5.conf /etc/krb5.conf

If there are other Kerberos realms involved, you should manually merge the two files.

We are now ready to start the Samba AD/DC services:

    sudo systemctl start samba-ad-dc

And this concludes the installation. The next section will show how to perform some basic checks.

## Verification
Here are some verification steps that can be run to check that the provisioning was done correctly and the service is ready.

### Kerberos authentication
A Kerberos ticket for the *Administrator* principal can be obtained with the `kinit` command. Note you don't have to be *root* to run this command. It's perfectly fine to get a ticket for a different principal than your own user, even a privileged one:

    kinit Administrator

The command will ask for a password. The password is the one supplied to the `samba-tool` command earlier, when the domain was provisioned, or the randomly chosen one if the `--adminpass` option was not used.

    Password for Administrator@EXAMPLE.INTERNAL:

```{seealso}
If you are not familiar with Kerberos, please see our {ref}`Introduction to Kerberos<introduction-to-kerberos>`.
```

To verify the ticket was obtained, use `klist`, which should have output similar to the following:

    Ticket cache: FILE:/tmp/krb5cc_1000
    Default principal: Administrator@EXAMPLE.INTERNAL

    Valid starting     Expires            Service principal
    07/24/24 13:52:33  07/24/24 23:52:33  krbtgt/EXAMPLE.INTERNAL@EXAMPLE.INTERNAL
            renew until 07/25/24 13:52:02

### DNS tests
Using the Kerberos ticket from the step above, we can check the DNS server that Samba is running.

If everything is correct, the `hostname` command should be able to return both the short hostname, and the fully qualified hostname.

For the short hostname, use the command:

    hostname

For the fully qualified hostname, run this instead:

    hostname -f

For example, `hostname -f` would return something like `ad.example.internal`, while `hostname` returns only `ad`.

#### Server Information
With that information at hand and verified, we can perform further checks. Let's get information about the DNS service provided by this domain controller:

    samba-tool dns serverinfo $(hostname -f)

This command will produce a long output, truncated below:

    dwVersion                   : 0xece0205
    fBootMethod                 : DNS_BOOT_METHOD_DIRECTORY
    fAdminConfigured            : FALSE
    fAllowUpdate                : TRUE
    fDsAvailable                : TRUE
    pszServerName               : AD.example.internal
    pszDsContainer              : CN=MicrosoftDNS,DC=DomainDnsZones,DC=example,DC=internal
    (...)

Even though it doesn't look like it, the `samba-tool dns serverinfo` command used Kerberos authentication. The `klist` command output now shows another ticket that was obtained automatically:

    Ticket cache: FILE:/tmp/krb5cc_1000
    Default principal: Administrator@EXAMPLE.INTERNAL

    Valid starting     Expires            Service principal
    07/24/24 14:29:55  07/25/24 00:29:55  krbtgt/EXAMPLE.INTERNAL@EXAMPLE.INTERNAL
            renew until 07/25/24 14:29:53
    07/24/24 14:29:59  07/25/24 00:29:55  host/ad.example.internal@EXAMPLE.INTERNAL
            renew until 07/25/24 14:29:53

A ticket for the `host/ad.example.internal@EXAMPLE.INTERNAL` principal is now also part of the ticket cache.

#### DNS records
The DNS server backing the Samba Active Directory deployment also needs to have some specific DNS records in its zones, which are needed for service discoverability. Let's check if they were added correctly with this simple script:

    for srv in _ldap._tcp _kerberos._tcp _kerberos._udp _kpasswd._udp; do
        echo -n "${srv}.example.internal: "
        dig @localhost +short -t SRV ${srv}.example.internal
    done

The output should have no errors, and show the DNS records for each query:

    _ldap._tcp.example.internal: 0 100 389 ad.example.internal.
    _kerberos._tcp.example.internal: 0 100 88 ad.example.internal.
    _kerberos._udp.example.internal: 0 100 88 ad.example.internal.
    _kpasswd._udp.example.internal: 0 100 464 ad.example.internal.

And, of course, our own hostname must be in DNS as well:

    dig @localhost +short -t A $(hostname)

The above command should return your own IP address.

### User creation test
Users (and groups, and other entities as well) can be created with the `samba-tool` command. It can be used remotely, to manage users on a remote Samba AD server, or locally on the same server it is managing.

When run **_locally as root_**, no further authentication is required:

    samba-tool user add noble

The command above will prompt for the desired password for the `noble` user, and if it satisfies the password complexity criteria, the user will be created. As with the *Administrator* Samba user, `kinit noble` can be used to test that the `noble` user can be authenticated.

```{note}
`samba-tool` creates **Samba** users, not local Linux users! These Samba users only exist for domain joined computers and other SMB connections/shares.
```

The default password policy is quite severe, requiring complex passwords. To display the current policy, run:

    sudo samba-tool domain passwordsettings show

Which will show the default password policy for the domain:

    Password information for domain 'DC=example,DC=internal'

    Password complexity: on
    Store plaintext passwords: off
    Password history length: 24
    Minimum password length: 7
    Minimum password age (days): 1
    Maximum password age (days): 42
    Account lockout duration (mins): 30
    Account lockout threshold (attempts): 0
    Reset account lockout after (mins): 30

Each one of these can be changed, including the password complexity. For example, to set the minimum password length to 12:

    sudo samba-tool domain passwordsettings set --min-pwd-length=12

To see all the options, run:

    samba-tool domain passwordsettings set --help

## Next steps
This Samba AD/DC server can be treated as an Active Directory server for Window and Linux systems. Typically next steps would be to create users and groups, and join member servers and workstations to this domain. Workstation users would login using the domain credentials, and member servers are used to provide file and print services.

## References

- [Active Directory Domain Services Overview](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview)
- [`samba-tool` manual page](https://manpages.ubuntu.com/manpages/noble/man8/samba-tool.8.html)
- Active Directory integration:
  - {ref}`Choosing an integration method <choosing-an-integration-method>`
  - {ref}`Joining a Member Server <join-a-domain-with-winbind-preparation>`
  - {ref}`Joining Workstations (without Samba services) <how-to-set-up-sssd-with-active-directory>`

