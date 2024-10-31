(dnssec)=
# DNS Security Extensions (DNSSEC)

DNS is a mapping system between names and IP addresses. Besides this main purpose that allows us to use friendly names instead of a sequence of numbers to reach a web site, it may store more information about a particular domain, such as:
 * point of contact
 * when it was last updated
 * what are the authoritative name servers for the domain
 * what are the mail exchangers for the domain (i.e., which systems are responsible for email for this domain)
 * mapping of host names to IP addresses, and vice-versa
 * information about other services, such as kerberos realms, LDAP servers, etc (usually on internal domains only)
 * and more

When DNS was first conceived, security wasn't a top priority yet. At its origins, DNS is susceptible to multiple vulnerabilities, and has many weaknesses. Most of them are a consequence of spoofing: there is no guarantee that the reply you got to a DNS query a) was not tampered with; b) came from the true source.

This is not news, and other mechanisms on top of DNS and around it are in place to counteract that weakness. For example, the famous *HTTPS* padlock that can be seen when accessing most websites nowadays, which uses the TLS protocol to both authenticate the website, and encrypt the connection. It doesn't prevent DNS spoofing, and your web browser might still be tricked into attempting a connection with a fraudulent website, but the moment the TLS certificate is inspected, a warning will be issued to the user. Depending on local policies, the connection might be even immediately blocked. Still, DNS spoofing is a real problem, and TLS itself is subject to other types of attacks.

## What is it?

DNSSEC stands for Domain Name System (DNS) Security Extensions (SEC). It's an extension to DNS that introduces digital signatures so that each DNS response can be verified for:

 * integrity: The answer was not tampered with and did not change during transit.
 * authenticity: The data came from the true source, and not another entity impersonating the source.

It's important to note that DNSSEC, however, will NOT encrypt the data: it is still sent in the clear.

DNSSEC is based on public key cryptography, meaning that every DNS zone has a public/private key pair. The private key is used to sign the zone's DNS records, and the corresponding public key can be used to very those signatures. This public key is also published in the zone, and anyone fetching records can also fetch the public key to verify the signature of the data.

The question then becomes, how to trust that this public key is authentic? Turns out the key is also signed: it's signed by the parent zone's key, which is also signed by its parent, and so on, all the way to the top: the root DNS zone. The root zone keys are trusted implicitly, and all DNS resolvers have it as a trust anchor. This sequence of keys and signatures all the way to the top is called the chain of trust.

The public key cryptography behind SSL/TLS is similar, but there we have the Certificate Authority entity (CA) that issues the certificates and vouches for them. Every single web browser or other SSL/TLS client or operating system needs to have a "bootstrap" list of CAs that it will trust by default, and there are dozens. In DNSSEC, the only bootstrap public key the resolver needs is the root zone one. It's as if there was only one trusted CA.

In the references section there is a very nice and simplified 12-step example on how a Validating DNS Resolver would go about returning the result of a query and validating it using DNSSEC.

## New resource records (RRs)
DNSSEC introduces a set of new Resource Records. Here are the most important ones:

 * RRSIG: Resource Record Signature. Each RRSIG record matches a corresponding Resource Record, i.e., it's the digital cryptographic signature of that Resource Record.
 * DNSKEY: There are several types of keys used in DNSSEC, and this record is used to store the public key in each case.
 * DS: Delegation Signer. This stores a secure delegation, and is used to build the authentication chain to child DNS zones. This makes it possible for a parent zone to "vouch" for its child zone.
 * NSEC, NSEC3, NSEC3PARAM: Next Secure record. These records are used to prove that a DNS name does not exist.

As an example, when a query is performed by a client that declares it understands DNSSEC, and the resource record it's querying for has a signature, the RRSIG is also returned:

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

DNSSEC suddenly made it more attractive and secure to store other types of information in DNS zones. Although it has always been possible to store SRV, TXT and other generic records in DNS, now these can be signed, and can thus be relied upon to be true. A well known initiative that leverages DNSSEC for this purpose is DANE: DNS-based Authentication of Named Entities (RFC 6394, RFC 6698, RFC 7671, RFC 7672, RFC 7673).

For example, imagine if the SSH fingerprints for a host you are logging into for the first time were also stored in DNS, and secured via DNSSEC. Instead of being prompted if you recognize the fingerprint, and wish to proceed, all this verification could happen in the background via DNSSEC and the SSHFP resource record published in the DNS zone for that host. OpenSSH is already capable of this via the configuration option `VerifyHostKeyDNS`.


## Where does the DNSSEC validation happen?

DNSSEC validation is the act of fetching the DNS data that was requested, their signatures, and performing the cryptographic validation of that data. Who is responsible for that?

It depends.

Let's analyze the simple scenario of a system on a local network performing a DNS query for a domain.

![Simple DNS](../images/ubuntu-local-recursive-dns.png)

Here we have:

 * An Ubuntu system, like a desktop, configured to use a DNS server in the local network.
 * A DNS server configured to perform recursive queries on behalf of the clients from the local network.

Let's zoom in a little bit on that Ubuntu system:

![Stub Resolver](../images/ubuntu-stub-resolver.png)

When an application needs to translate a hostname to an IP address, it uses standard glibc calls for that job. That is called a stub resolver, or simply a "dns client". This is a very simple client in the sense that it does not perform recursive queries: it expects to dispatch the DNS query to a recursive DNS server, which will do all the hard work.

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

This configuration is usually provided via DHCP, but could also be set via other means. In this particular example, the DNS server that the stub resolver (`systemd-resolved`) will use for all queries that go out on that network interface is 10.10.17.1. The output above also has `DNSSEC=no/unsupported`: we will get back to that in a moment, but it means that `systemd-resolved` is not performing the DNSSEC cryptographic validation.

Given what we have:
 * an application
 * stub resolver ("dns client")
 * recursive DNS server in the local network
 * several other DNS servers in the internet that will be queried by our recursive DNS server

Where does the DNSSEC validation happen? Who is responsible?

Well, any DNS server can perform the validation. Let's look at two scenarios, and what it means in each case.

### Validating Resolver

When a recursive DNS server is also performing DNSSEC validation, it's called a *Validating Resolver*. That will typically be the DNS server on your local network, your company's, or in some cases even your ISP's.

![Validating Resolver](../images/ubuntu-local-validating-resolver.png)

In Ubuntu, the default configuration of the `bind9` DNS server is to act as a validating resolver. This can be seen in `/etc/bind/named.conf.options` after installing the `bind9` package:

    options {
        ...
        dnssec-validation auto;
        ...
    };

The key aspect of this deployment type is that the network between the stub resolved and the validating resolver has to be trusted, otherwise this is not useful. The Validating Resolver will be performing all the DNSSEC checks, and only returning a response if it was validated, but that response could have been altered on that "last mile" network segment.

Still, this is a valid and very useful scenario, and good enough for most cases. And it has the extra benefit that the DNSSEC validation is done only once, at the resolver, for all clients on the network.

### Local DNSSEC validation
Some stub resolvers, like `systemd-resolved`, can perform DNSSEC validation by themselves. In this scenario, there is no insecure network path between the resolver and the dns client, as they are on the same system. But since the stub resolver will be doing the validation, that means more DNS queries, and a higher latency, because now it's not just one query, but multiple ones: a query for the actual desired record, than another query for the digital signature, then the public key, than it has to validate that key, etc. And if another client on the network happens to be making the same query, it will also have to repeat all those steps.

In general, local DNSSEC validation is only required in more specific secure environments.

As an example, let's perform the same query using `systemd-resolved` with and without local DNSSEC validation enabled.

Without local DNSSEC validation. First, let's show it's disabled indeed:

    $ resolvectl dnssec
    Global: no
    Link 44 (eth0): no

Now we perform the query:

    $ resolvectl query --type=MX isc.org
    isc.org IN MX 10 mx.ams1.isc.org                            -- link: eth0
    isc.org IN MX 5 mx.pao1.isc.org                             -- link: eth0

    -- Information acquired via protocol DNS in 229.5ms.
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

 * DNSSEC - What Is It and Why Is It Important: https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en
 * Tool to visualize the DNSSEC chain of trust of a domain: https://dnsviz.net/
 * DANE: https://en.wikipedia.org/wiki/DNS-based_Authentication_of_Named_Entities
 * RFC 4255 - Using DNS to Securely Publish Secure Shell (SSH) Key Fingerprints: https://datatracker.ietf.org/doc/html/rfc4255
 * Simplified 12-step DNSSEC validation process: https://bind9.readthedocs.io/en/v9.18.24/dnssec-guide.html#the-12-step-dnssec-validation-process-simplified

