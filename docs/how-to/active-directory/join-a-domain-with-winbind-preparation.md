---
myst:
  html_meta:
    description: Prepare to join an Active Directory domain with winbind by configuring DNS resolver, installing packages, and planning identity mapping.
---

(join-a-domain-with-winbind-preparation)=
# Join a domain with winbind: preparation

Choosing the identity mapping backend, and planning its ranges, is the first and most important aspect of joining a domain. To actually perform the join, however, a few more configuration steps are necessary. These steps are common to both backend types, the only difference being the actual idmap configuration.

To continue, this is the minimum set of packages that are needed:

    sudo apt install winbind libnss-winbind libpam-winbind

Next, it will make everything much easier if the {term}`DNS` resolver is pointed at the Active Directory DNS server. If that is already the case as provided by the {term}`DHCP` server, this part can be skipped.

For example, for a default netplan configuration file which looks like this:

```yaml
    network:
    version: 2
    ethernets:
        eth0:
            dhcp4: true
```

You can add a `nameservers` block which will override the DNS options sent by the DHCP server. For example, if the DNS server is at `10.10.4.5` and the domain search value is `example.internal`, this would be the new configuration:
```yaml
    network:
    version: 2
    ethernets:
        eth0:
            dhcp4: true
            nameservers:
                addresses: [10.10.4.5]
                search: [example.internal]
```

To make the changes effective, first make sure there are no syntax errors:

    sudo netplan generate

If there are no complaints, the changes can be applied:

    sudo netplan apply

```{note}
Be careful whenever changing network parameters over an ssh connection. If there are any mistakes, you might lose remote access!
```

To check if the resolver was updated, run `resolvectl status`:

    Global
             Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
      resolv.conf mode: stub

    Link 281 (eth0)
        Current Scopes: DNS
             Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
           DNS Servers: 10.10.4.5 10.10.4.1
            DNS Domain: example.internal

Now we need to configure the system to also use the winbind NSS module to look for users and groups. In Ubuntu 24.04 LTS and later, this is done automatically, but for older LTS releases, edit the file `/etc/nsswitch.conf` and add `winbind` to the end of the `passwd:` and `group:` lines:

    # /etc/nsswitch.conf
    #
    # Example configuration of GNU Name Service Switch functionality.
    # If you have the `glibc-doc-reference' and `info' packages installed, try:
    # `info libc "Name Service Switch"' for information about this file.

    passwd:         files systemd winbind
    group:          files systemd winbind
    (...)

Finally, let's enable automatic home directory creation for users as they login. Run the command:

    sudo pam-auth-update --enable mkhomedir

Now we are set to perform the final winbind configuration depending on the identity mapping backend that was chosen, and actually join the domain.
