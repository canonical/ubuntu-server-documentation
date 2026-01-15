---
myst:
  html_meta:
    description: "Learn about DNS Security Extensions (DNSSEC) for securing DNS queries and protecting against DNS spoofing on Ubuntu Server."
---

(dnssec)=
# DNS Security Extensions (DNSSEC)

DNSSEC is a security extension for the Domain Name System (DNS). DNS is a mapping between names and Internet Protocol (IP) addresses, allowing the use of friendly names instead of sequences of numbers when reaching web sites. Additionally, it stores extra information about a given domain, such as:

* Who the point of contact is
* When it was last updated
* What are the authoritative name servers for the domain
* What are the mail exchangers for the domain (i.e., which systems are responsible for email for this domain)
* How host names are mapped to IP addresses, and vice-versa
* What information about other services, such as kerberos realms, LDAP servers, etc (usually on internal domains only) are there

When DNS was first conceived, security wasn't a top priority. At its origins, DNS is susceptible to multiple vulnerabilities, and has many weaknesses. Most of them are a consequence of spoofing: there is no guarantee that the reply you received to a DNS query was not tampered with or that it came from the true source.

This is not news, and other mechanisms on top of DNS and around it are in place to counteract that weakness. For example, the famous *HTTPS* padlock that can be seen when accessing most websites nowadays, which uses the TLS protocol to both authenticate the website, and encrypt the connection. It doesn't prevent DNS spoofing, and your web browser might still be tricked into attempting a connection with a fraudulent website, but the moment the TLS certificate is inspected, a warning will be issued to the user. Depending on local policies, the connection might be even immediately blocked. Still, DNS spoofing is a real problem, and TLS itself is subject to other types of attacks.

## What is it?

DNSSEC, which stands for Domain Name System Security Extensions, is an extension to DNS that introduces digital signatures. This allows each DNS response to be verified for:

* **Integrity**: The answer was not tampered with and did not change during transit.
* **Authenticity**: The data came from the true source, and not another entity impersonating the source.

It's important to note that DNSSEC, however, will NOT encrypt the data: it is still sent in the clear.

DNSSEC is based on public key cryptography, meaning that every DNS zone has a public/private key pair. The private key is used to sign the zone's DNS records, and the corresponding public key can be used to verify those signatures. This public key is also published in the zone. Anyone querying the zone can also fetch the public key to verify the signature of the data.

A crucial question arises: How can we trust the authenticity of this public key? The answer lies in a hierarchical signing process. The key is signed by the parent zone's key, which, in turn, is signed by its parent, and so on, forming the "chain of trust", ensuring the integrity and authenticity of DNS records. The **root zone keys** found at the root DNS zone are implicitly trusted, serving as the foundation of the trust chain. 

The public key cryptography underpinning SSL/TLS operates in a similar manner, but relies on Certificate Authority (CA) entities to issue and vouch for certificates. Web browsers and other SSL/TLS clients must maintain a list of trusted CAs, typically numbering in the dozens. In contrast, DNSSEC simplifies this process by requiring only a single trusted root zone key.

For a more detailed explanation of how the DNSSEC validation is performed, please refer to the [Simplified 12-step DNSSEC validation process](https://bind9.readthedocs.io/en/latest/dnssec-guide.html#the-12-step-dnssec-validation-process-simplified) guide from ISC.

## DNS daemons
Ubuntu supports multiple DNS resolvers, covering a variety of use cases. Most of them support DNSSEC validation, but it might not be activated and set up with valid trust-anchors automatically.

<!-- Using non-breaking hyphen & non-breaking space for improved table spacing. -->
| Daemon | Type | DNSSEC support |
| --- | --- | --- |
| systemd&#8209;resolved | Stub&nbsp;Resolver&nbsp;(local) | Yes. Disabled by default. Controlled via `DNSSEC=...` setting in `/etc/systemd/resolved.conf.d`. |
| dnsmasq | Stub Resolver | Yes. Disabled by default. Controlled via `dnssec` and `conf-file=../trust-anchors.conf` settings. |
| bind9 | Recursive Resolver | Yes. Enabled by default via `dnssec-validation auto;` setting. |
<!-- TODO: What about "unbound"? -->

The **systemd-resolved** stub resolver is pre-installed in Ubuntu but ships with DNSSEC validation disabled by default. It supports two optional DNSSEC modes: fallback or strict validation. Either mode can be configured using the `DNSSEC=` setting, e.g. in a new `/etc/systemd/resolved.conf.d/10-dnssec.conf` drop-in configuration (see example below).

* You can enable the **fallback mode**, using the `DNSSEC=allow-downgrade` setting, which tries to validate the DNSSEC records whenever possible, but at the same time accepts unsigned responses for backwards compatibility with unsigned zones.

* Should authenticity of DNS records be a concern to you, it's advised to opt-in to the **strict mode** by using the `DNSSEC=yes` setting and reloading the configuration.

For example, here is how the strict mode can be enabled. To use the fallback mode instead, replace `DNSSEC=yes` with `DNSSEC=allow-downgrade`:

```
$ sudo mkdir -p /etc/systemd/resolved.conf.d
$ sudo tee /etc/systemd/resolved.conf.d/10-dnssec.conf >/dev/null <<EOF
[Resolve]
DNSSEC=yes
EOF

$ sudo systemctl reload systemd-resolved.service
```

Once reloaded, the functionality of DNSSEC in **systemd-resolved** can be confirmed, using the `dig` command on the local stub resolver at `127.0.0.53`, by checking for the existence of the **ad** (Authenticated Data) flag:
```
$ dig @127.0.0.53 isc.org +dnssec
[...]
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1
```

DNSSEC validation will reject DNS resource records, originating from a DNS resolver that indicates DNSSEC support through the `EDNS0` "DNSSEC OK" (`DO`) flag (c.f. [RFC 3225](https://datatracker.ietf.org/doc/html/rfc3225)), but at the same time does not properly respond to DNSSEC queries (e.g. the missing "authenticated data" = `AD` flag or missing `RRSIG` or `NSEC` records). In the past this has led to issues, especially in virtualization environments or when edge routers are involved, e.g. those provided by ISPs for home connectivity ({lpbug}`2119652`, [ref2](https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/AFHNUEHKC5KJVGBGSJBH2BMESUAGDF4H/), [ref3](https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/P63RI3VBQ7NGL3AKMTR7PCVHVSCPYCLF/), {lpbug}`2121483`). Therefore, DNSSEC should only be enabled in controlled environments, where the upstream DNS server is correctly configured to handle DNSSEC queries.

```{warning}
Be aware that enforcing DNSSEC in strict mode can lead to errors, especially for local, unsigned domains and you would only be able to reach such services by accessing them through their IP address directly. For example this could manifest itself by errors like `DNS_PROBE_FINISHED_NXDOMAIN` in your browser, when trying to access services in the local network.
<!-- TODO: What about DNS64? (https://blog.apnic.net/2016/06/09/lets-talk-ipv6-dns64-dnssec/) -->
```

Once strict DNSSEC validation is enabled, you should also be able to confirm it through higher level checks in your browser, e.g. using those 3rd party services:
 * https://internet.nl/test-connection/
 * https://wander.science/projects/dns/dnssec-resolver-test/

```{note}
In case of issues with Domain Name resolution, make sure to remove relevant drop-in configs in `/etc/resolved.conf.d` and execute `systemctl reload systemd-resolved.service`. This will reset any DNSSEC configuration to the default `DNSSEC=no` and can be confirmed by executing `resolvectl dnssec`.
```

## New Resource Records (RRs)
DNSSEC introduces a set of new Resource Records. Here are the most important ones:

 * RRSIG: Resource Record Signature. Each RRSIG record matches a corresponding Resource Record, i.e., it's the digital cryptographic signature of that Resource Record.
 * DNSKEY: There are several types of keys used in DNSSEC, and this record is used to store the public key in each case.
 * DS: Delegation Signer. This stores a secure delegation, and is used to build the authentication chain to child DNS zones. This makes it possible for a parent zone to "vouch" for its child zone.
 * NSEC, NSEC3, NSEC3PARAM: Next Secure record. These records are used to prove that a DNS name does not exist.

For instance, when a DNSSEC-aware client queries a Resource Record that is signed, the corresponding RRSIG record is also returned:

    $ dig @1.1.1.1 +dnssec -t MX isc.org

    ; <<>> DiG 9.18.28-0ubuntu0.24.04.1-Ubuntu <<>> @1.1.1.1 +dnssec -t MX isc.org
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 51256
    ;; flags: qr rd ra ad; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags: do; udp: 1232
    ;; QUESTION SECTION:
    ;isc.org.                       IN      MX

    ;; ANSWER SECTION:
    isc.org.                300     IN      MX      5 mx.pao1.isc.org.
    isc.org.                300     IN      MX      10 mx.ams1.isc.org.
    isc.org.                300     IN      RRSIG   MX 13 2 300 20241029080338 20241015071431 27566 isc.org. LG/cvFmZ8jLz+CM14foaCtwsyCTwKXfVBZV2jcl2UV8zV79QRLs0YXJ3 sjag1vYCqc+Q5AwUi2DB8L/wZR6EJQ==

    ;; Query time: 199 msec
    ;; SERVER: 1.1.1.1#53(1.1.1.1) (UDP)
    ;; WHEN: Tue Oct 22 16:44:33 UTC 2024
    ;; MSG SIZE  rcvd: 187


## Other uses

DNSSEC makes it more attractive and secure to store other types of information in DNS zones. Although it has always been possible to store SRV, TXT and other generic records in DNS, now these can be signed, and can thus be relied upon to be true. A well known initiative that leverages DNSSEC for this purpose is DANE: DNS-based Authentication of Named Entities (RFC 6394, RFC 6698, RFC 7671, RFC 7672, RFC 7673).

For example, consider a scenario where SSH host keys are stored and secured in DNS using DNSSEC. Rather than manually verifying a host key fingerprint, the verification process could be automated using DNSSEC and the SSHFP Resource Record published in the DNS zone for that host. OpenSSH already supports this feature through the `VerifyHostKeyDNS` configuration option.


## Where does the DNSSEC validation happen?

DNSSEC validation involves fetching requested DNS data, retrieving their corresponding digital signatures, and cryptographically verifying them. Who is responsible for this process?

It depends.

Let's analyze the simple scenario of a system on a local network performing a DNS query for a domain.

![Simple DNS](../images/ubuntu-local-recursive-dns.png)

Here we have:

 * An Ubuntu system, like a desktop, configured to use a DNS server in the local network.
 * A DNS server configured to perform recursive queries on behalf of the clients from the local network.

Let's zoom in a little bit on that Ubuntu system:

![Stub Resolver](../images/ubuntu-stub-resolver.png)

To translate a {term}`hostname` into an IP address, applications typically rely on standard `glibc` functions. This process involves a stub resolver, often referred to as a DNS client. A stub resolver is a simple client that doesn't perform recursive queries itself; instead, it delegates the task to a recursive DNS server, which handles the complex query resolution.

In Ubuntu, the default stub resolver is `systemd-resolved`. That's a daemon, running locally, and listening on port 53/udp on IP 127.0.0.53. The system is configured to use that as its nameserver via `/etc/resolv.conf`:

    nameserver 127.0.0.53
    options edns0 trust-ad

This stub resolver has its own configuration for which recursive DNS servers to use. That can be seen with the command `resolvectl`. For example:

    Global
             Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
      resolv.conf mode: stub

    Link 12 (eth0)
        Current Scopes: DNS
             Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
    Current DNS Server: 10.10.17.1
           DNS Servers: 10.10.17.1
            DNS Domain: lxd

This configuration is usually provided via {term}`DHCP`, but could also be set via other means. In this particular example, the DNS server that the stub resolver (`systemd-resolved`) will use for all queries that go out on that network interface is 10.10.17.1. The output above also has `DNSSEC=no/unsupported`: we will get back to that in a moment, but it means that `systemd-resolved` is not performing the DNSSEC cryptographic validation.

Given what we have:
 * an application
 * stub resolver ("DNS client")
 * recursive DNS server in the local network
 * several other DNS servers in the internet that will be queried by our recursive DNS server

Where does the DNSSEC validation happen? Who is responsible?

Well, any DNS server can perform the validation. Let's look at two scenarios, and what it means in each case.

### Validating Resolver

When a recursive DNS server is also performing DNSSEC validation, it's called a *Validating Resolver*. That will typically be the DNS server on your local network, at your company, or in some cases at your ISP.

![Validating Resolver](../images/ubuntu-local-validating-resolver.png)

This is the case if you install the BIND9 DNS server: the default configuration is to act as a Validating Resolver. This can be seen in `/etc/bind/named.conf.options` after installing the `bind9` package:

    options {
        ...
        dnssec-validation auto;
        ...
    };

```{note}
Starting with version `1:9.18.34-1` in Ubuntu 24.10 and above, the `dnssec-validation auto` setting became the implicit default and does not need to be set explicitly in `named.conf.options` anymore.
```

A critical aspect of this deployment model is the trust in the network segment between the stub resolver and the Validating Resolver. If this network is compromised, the security benefits of DNSSEC can be undermined. While the Validating Resolver performs DNSSEC checks and returns only verified responses, the response could still be tampered with on the final ("last mile") network segment.

This is where the `trust-ad` setting from `/etc/resolv.conf` comes into play:

    nameserver 127.0.0.53
    options edns0 trust-ad

The `trust-ad` setting is documented in the {manpage}`resolv.conf(5)` manual page. It means that the local resolver will:

 * Set the `ad` bit (Authenticated Data) in the outgoing queries.
 * Trust the `ad` bit in the responses from the specified nameserver.

When the `ad` bit is set in a DNS response, it means that DNSSEC validation was performed and successful. The data was authenticated.

Specifying `trust-ad` in `/etc/resolv.conf` implies in these assumptions:

 * The 127.0.0.53 name server is trusted to set the `ad` flag correctly in its responses. If it performs DNSSEC validation, it is trusted to perform this validation correctly, and set the `ad` flag accordingly. If it does not perform DNSSEC validation, then the `ad` flag will always be unset in the responses.
 * The network path between localhost and 127.0.0.53 is trusted.

When using `systemd-resolved` as a stub resolver, as configured above, the network path to the local DNS resolver is inherently trusted, as it is a localhost interface. However, the actual nameserver used is not 127.0.0.53; it depends on `systemd-resolved`'s configuration. Unless local DNSSEC validation is enabled, `systemd-resolved` will strip the ad bit from queries sent to the Validating Resolver and from the received responses.

This is the default case in Ubuntu systems.

Another valid configuration is to not use `systemd-resolved`, but rather point at the Validating Resolver of the network directly, like in this example:

    nameserver 10.10.17.11
    options edns0 trust-ad

The `trust-ad` configuration functions similarly to the previous scenario. The `ad` bit is set in outgoing queries, and the resolver trusts the `ad` bit in incoming responses. However, in this case, the nameserver is located at a different IP address on the network. This configuration relies on the same assumptions as before:

 * The 10.10.17.11 name server is trusted to perform DNSSEC validation and set the `ad` flag accordingly in its responses.
 * The network path between localhost and 10.10.17.11 is trusted.

As these assumptions have a higher chance of not being true, this is not the default configuration.

In any case, having a Validating Resolver in the network is a valid and very useful scenario, and good enough for most cases. And it has the extra benefit that the DNSSEC validation is done only once, at the resolver, for all clients on the network.

### Local DNSSEC validation
Some stub resolvers, such as systemd-resolved, can perform DNSSEC validation locally. This eliminates the risk of network attacks between the resolver and the client, as they reside on the same system. However, local DNSSEC validation introduces additional overhead in the form of multiple DNS queries. For each DNS query, the resolver must fetch the desired record, its digital signature, and the corresponding public key. This process can increase latency, and with multiple clients on the same network requesting the same records, that's duplicated work.

In general, local DNSSEC validation is still the more secure approach, validating and authenticating the DNS resource records end-to-end, without the need to trust any DNS server along the way. Besides this, {term}`DNS-over-TLS (DoT) <DoT>` or {term}`DNS-over-HTTPS (DoH) <DoH>` could be used to increase privacy, by encrypting the DNS connection between your local client and the remote Recursive Resolver.

As an example, let's perform the same query using `systemd-resolved` with and without local DNSSEC validation enabled.

Without local DNSSEC validation. First, let's show it's disabled indeed:

    $ resolvectl dnssec
    Global: no
    Link 44 (eth0): no

Now we perform the query:

    $ resolvectl query --type=MX isc.org
    isc.org IN MX 10 mx.ams1.isc.org                            -- link: eth0
    isc.org IN MX 5 mx.pao1.isc.org                             -- link: eth0

    -- Information acquired via protocol DNS in 37.2ms.
    -- Data is authenticated: no; Data was acquired via local or encrypted transport: no
    -- Data from: network

Notice the `Data is authenticated: no` in the result.

Now we enable local DNSSEC validation:

    $ sudo resolvectl dnssec eth0 true

And repeat the query:

    $ resolvectl query --type=MX isc.org
    isc.org IN MX 5 mx.pao1.isc.org                             -- link: eth0
    isc.org IN MX 10 mx.ams1.isc.org                            -- link: eth0

    -- Information acquired via protocol DNS in 3.0ms.
    -- Data is authenticated: yes; Data was acquired via local or encrypted transport: no
    -- Data from: network

There is a tiny difference in the output:

    -- Data is authenticated: yes

This shows that local DNSSEC validation was applied, and the result is authenticated.

## What happens when DNSSEC validation fails
When DNSSEC validation fails, how this error is presented to the user depends on multiple factors.

For example, if the DNS client is not performing DNSSEC validation, and relying on a Validating Resolver for that, typically what the client will see is a generic failure. For example:

    $ resolvectl query www.dnssec-failed.org
    www.dnssec-failed.org: resolve call failed: Could not resolve 'www.dnssec-failed.org', server or network returned error SERVFAIL

The Validating Resolver logs, however, will have more details about what happened:

    Oct 22 17:14:50 n-dns named[285]: validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
    Oct 22 17:14:50 n-dns named[285]: no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 68.87.68.244#53
    ...
    Oct 22 17:14:52 n-dns named[285]: broken trust chain resolving 'www.dnssec-failed.org/AAAA/IN': 68.87.72.244#53

In contrast, when DNSSEC validation is being performed locally, the error is more specific:

    $ sudo resolvectl dnssec eth0 true
    $ resolvectl query www.dnssec-failed.org
    www.dnssec-failed.org: resolve call failed: DNSSEC validation failed: no-signature

But even when the validation is local, simpler clients might not get the full picture, and still just return a generic error:

    $ host www.dnssec-failed.org
    Host www.dnssec-failed.org not found: 2(SERVFAIL)

## Further reading

 * [DNSSEC - What Is It and Why Is It Important](https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en)
 * [Tool to visualize the DNSSEC chain of trust of a domain](https://dnsviz.net/)
 * [DANE](https://en.wikipedia.org/wiki/DNS-based_Authentication_of_Named_Entities)
 * [RFC 4255](https://datatracker.ietf.org/doc/html/rfc4255) - Using DNS to Securely Publish Secure Shell (SSH) Key Fingerprints
 * {ref}`dnssec-troubleshooting`
