(dnssec-troubleshooting)=
# Basic DNSSEC troubleshooting

Some of the troubleshooting tips that will be shown here are focused on the BIND9 {term}`DNS` server and its tools, but the general principle applies to {term}`DNSSEC` in all implementations.

## Handy "bad" and "good" DNSSEC domains
It helps to have some good known domains with broken and working DNSSEC available for testing, so we can be sure our tooling is catching those, and not just failing everywhere. There is no guarantee that these domains will be up forever, and certainly there are more out there, but this list is a good first choice:

 * These should fail DNSSEC validation:
   * *dnssec-failed.org*
   * *sigfail.ippacket.stream*
 * These should pass DNSSEC validation:
   * *isc.org*
   * *sigok.ippacket.stream*

## Logs

By default, the BIND9 server will log certain DNSSEC failures, and the journal log should be the first place to check.

For example, if we ask a BIND9 Validating Resolver for the IP address of the `www.dnssec-failed.org` name, we get a failure:

    $ dig @127.0.0.1 -t A www.dnssec-failed.org
    ; <<>> DiG 9.18.28-0ubuntu0.24.04.1-Ubuntu <<>> @127.0.0.1 -t A www.dnssec-failed.org
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 26260
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 1232
    ; COOKIE: 6339d7228b8587f401000000671bc2eb2fe25bdf099ef1af (good)
    ;; QUESTION SECTION:
    ;www.dnssec-failed.org.         IN      A

    ;; Query time: 460 msec
    ;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
    ;; WHEN: Fri Oct 25 16:10:19 UTC 2024
    ;; MSG SIZE  rcvd: 78

That's a very generic failure: it just says `SERVFAIL`, and gives us no IP: `IN A` is empty. The BIND9 logs, however, tell a more detailed story:

    $ journalctl -u named.service -f
    (...)
    named[286]: validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
    named[286]: no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 68.87.85.132#53
    named[286]: validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
    named[286]: no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 68.87.68.244#53
    named[286]: validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
    named[286]: no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 68.87.76.228#53
    named[286]: validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
    named[286]: no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 68.87.72.244#53
    named[286]: validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
    named[286]: no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 69.252.250.103#53
    named[286]: broken trust chain resolving 'www.dnssec-failed.org/A/IN': 68.87.72.244#53

## Client-side tooling: dig

One of the more versatile DNS troubleshooting tools is `dig`, generally used for interrogating DNS name servers to lookup and display domain information, but its broad functionality makes it a flexible aid for DNS troubleshooting. It provides direct control over setting most of the DNS flags in queries, and displays detailed responses for inspection.

For DNSSEC troubleshooting purposes, we are interested in the following features:

 * `+dnssec`: Set the "DNSSEC OK" bit in the queries, which tells the resolver to include in its responses the DNSSEC RRSIG records. This is also shown as a `do` flag in queries.
 * `+cd`: This means *check disabled* and tells the resolver we can accept unauthenticated data in the DNS responses.
 * `ad`: When included in a response, this flag means *authenticated data*, and tells us that the resolver who provided this answer has performed DNSSEC validation.
 * `@<IP>`: This parameter lets us direct the query to a specific DNS server running at the provided IP address.

For example, let's query a local DNS server for the *isc.org* type *A* record, and request DNSSEC data:

    $ dig @127.0.0.1 -t A +dnssec +multiline isc.org

    ; <<>> DiG 9.18.28-0ubuntu0.24.04.1-Ubuntu <<>> @127.0.0.1 -t A +dnssec +multiline isc.org
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25738
    ;; flags: qr rd ra ad; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags: do; udp: 1232
    ; COOKIE: 8c4c8391524d28af01000000671bd625936966d67a5f7061 (good)
    ;; QUESTION SECTION:
    ;isc.org.               IN A

    ;; ANSWER SECTION:
    isc.org.                207 IN A 151.101.2.217
    isc.org.                207 IN A 151.101.66.217
    isc.org.                207 IN A 151.101.130.217
    isc.org.                207 IN A 151.101.194.217
    isc.org.                207 IN RRSIG A 13 2 300 (
                                    20241107074911 20241024070338 27566 isc.org.
                                    BIl7hov5X11CITexzV9w7wbCOpKZrup3FopjgF+RIgOI
                                    5A8p8l2dJCLp/KBn/G6INj7TOHTtrGs1StTSJVNksw== )

    ;; Query time: 0 msec
    ;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
    ;; WHEN: Fri Oct 25 17:32:21 UTC 2024
    ;; MSG SIZE  rcvd: 231

Let's unpack this answer for the important troubleshooting parts:

 * The answer has the `ad` flag set, meaning this data was authenticated. In other words, DNSSEC validation was successful.
 * The status of the query is `NOERROR`, and we have 5 records in the answer section.
 * An RRSIG record for the "A" Resource Record was returned as requested by the `+dnssec` command-line parameter. This is also confirmed by the presence of the "do" flag in the "OPT PSEUDOSECTION".

If we repeat this query with a domain that we know fails DNSSEC validation, we get the following reply:

    $ dig @127.0.0.1 -t A +dnssec +multiline dnssec-failed.org

    ; <<>> DiG 9.18.28-0ubuntu0.24.04.1-Ubuntu <<>> @127.0.0.1 -t A +dnssec +multiline dnssec-failed.org
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 41300
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags: do; udp: 1232
    ; COOKIE: b895f4fe3f3d605401000000671bd719636ef1cfc4e615f3 (good)
    ;; QUESTION SECTION:
    ;dnssec-failed.org.     IN A

    ;; Query time: 1355 msec
    ;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
    ;; WHEN: Fri Oct 25 17:36:25 UTC 2024
    ;; MSG SIZE  rcvd: 74

This time:

 * There is no `ad` flag set in the answer.
 * The status of the query is a generic `SERVFAIL`, and zero answers were provided.

We can tell the Validating Resolver (the service running on the `@127.0.0.1` address) that we don't want it to perform DNSSEC validation. We do that by setting the `+cd` (check disabled) flag. Then things change in our answer:

    $ dig @127.0.0.1 -t A +dnssec +cd +multiline dnssec-failed.org

    ; <<>> DiG 9.18.28-0ubuntu0.24.04.1-Ubuntu <<>> @127.0.0.1 -t A +dnssec +cd +multiline dnssec-failed.org
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7269
    ;; flags: qr rd ra cd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags: do; udp: 1232
    ; COOKIE: dd66930044348f2501000000671bd808f6852a18a0089b3f (good)
    ;; QUESTION SECTION:
    ;dnssec-failed.org.     IN A

    ;; ANSWER SECTION:
    dnssec-failed.org.      297 IN A 96.99.227.255
    dnssec-failed.org.      297 IN RRSIG A 5 2 300 (
                                    20241111145122 20241025144622 44973 dnssec-failed.org.
                                    fa53BQ7HPpKFIPKyn3Md4bVLawQLeatny47hTq1QouG8
                                    DwyVqmsfs3d5kUTFO5FHdCy4U7o97ODYXiVuilEZS/aZ
                                    n6odin2SCm0so4TnIuKBgZFW41zpI6oIRmIVPv6HLerI
                                    uUxovyMEtaGyd5maNgxGldqLzgWkl18TWALYlrk= )

    ;; Query time: 0 msec
    ;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
    ;; WHEN: Fri Oct 25 17:40:24 UTC 2024
    ;; MSG SIZE  rcvd: 267

Looks like we have some sort of answer, but:

 * There is no `ad` flag in the answer, so this data was not authenticated.
 * The status is `NOERROR`, and we got two answers.
 * Note there is a `cd` flag in the answer, meaning "check disabled". No attempt at validating the answer was done by the resolver, as requested.

In none of these cases, though, did `dig` perform DNSSEC validation: it just presented the results provided by the Validating Resolver, which in some cases was no validation at all (via the `+cd` flag). To perform the validation ourselves, we have to use a different tool.

## Digging a bit deeper: `delv`

The `delv` tool is very similar to `dig`, and can perform the same DNS queries, but with a crucial difference: it can also validate DNSSEC. This is very useful in troubleshooting, because rather than returning a generic `SERVFAIL` error when something goes wrong with DNSSEC validation, it can tell us what was wrong in more detail.

But to bring the responsibility of doing DNSSEC validation to the tool itself, we use the `+cd` flag in our queries, to tell the resolver to not attempt that validation. Otherwise we will just get back a generic `SERVFAIL` error:

    $ delv @127.0.0.1 -t A +dnssec +multiline dnssec-failed.org
    ;; resolution failed: SERVFAIL

With the `+cd` flag present, however, `delv` itself will do the validation. It will fail again, but now with a DNSSEC-specific error:

    $ delv @127.0.0.1 -t A +dnssec +cd +multiline dnssec-failed.org
    ;; validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
    ;; no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 127.0.0.1#53
    ;; broken trust chain resolving 'dnssec-failed.org/A/IN': 127.0.0.1#53
    ;; resolution failed: broken trust chain

If needed, `delv` can be told to not perform DNSSEC validation at all, by passing the `-i` flag. Together with the `+cd` flag, which instructs the Validating Resolver to not perform validation either, we get this result:

    $ delv @127.0.0.1 -i -t A +dnssec +cd +multiline dnssec-failed.org
    ; answer not validated
    dnssec-failed.org.      100 IN A 96.99.227.255

For a good DNSSEC domain, `delv` will return a validated answer:

    $ delv @127.0.0.1 -t A +multiline +cd isc.org
    ; fully validated
    isc.org.                300 IN A 151.101.2.217
    isc.org.                300 IN A 151.101.66.217
    isc.org.                300 IN A 151.101.130.217
    isc.org.                300 IN A 151.101.194.217
    isc.org.                300 IN RRSIG A 13 2 300 (
                                    20241107074911 20241024070338 27566 isc.org.
                                    BIl7hov5X11CITexzV9w7wbCOpKZrup3FopjgF+RIgOI
                                    5A8p8l2dJCLp/KBn/G6INj7TOHTtrGs1StTSJVNksw== )

Given that above we used the `+cd` flag, this means that the validation was done by `delv` itself. We will get the same result without that flag if the Validating Resolver also succeeds in the DNSSEC validation, and provides an answer.

## Incorrect time

As with everything related to cryptography, having an accurate measurement of time is of crucial importance. In a nutshell, digital signatures and keys have expiration dates.

An RRSIG record (a digital signature of a Resource Record) has a validity. For example, this record:

    noble.example.internal. 86400 IN RRSIG A 13 3 86400 (
                                    20241106131533 20241023195023 48112 example.internal.
                                    5fL4apIwCD9kt4XbzzlLxMXY3mj8Li1WZu3qzlcBpERp
                                    lXPgLODbRrWyp7L81xEFnfhecKtEYv+6Y0Xa5iVRug== )

Has this validity range:

 * valid until: 20241106131533 (2024-11-06 13:15:33 UTC)
 * valid since: 20241023195023 (2024-10-23 19:50:23 UTC)

If the DNSSEC validator has an incorrect clock, outside of the validity range, the DNSSEC validation will fail. For example, with the clock incorrectly set to before the beginning of the validity period, `delv` will complain like this:

    $ date
    Tue Oct 10 10:10:19 UTC 2000

    $ delv @10.10.17.229 -a example.internal.key +root=example.internal +multiline noble.example.internal
    ;; validating example.internal/DNSKEY: verify failed due to bad signature (keyid=48112): RRSIG validity period has not begun
    ;; validating example.internal/DNSKEY: no valid signature found (DS)
    ;; no valid RRSIG resolving 'example.internal/DNSKEY/IN': 10.10.17.229#53
    ;; broken trust chain resolving 'noble.example.internal/A/IN': 10.10.17.229#53
    ;; resolution failed: broken trust chain

Any other Validating Resolver will fail in a similar way, and should indicate this error in its logs.

BIND9 itself will complain loudly if it's running on a system with an incorrect clock, as the root zones will fail validation:

    named[3593]: managed-keys-zone: DNSKEY set for zone '.' could not be verified with current keys
    named[3593]:   validating ./DNSKEY: verify failed due to bad signature (keyid=20326): RRSIG validity period has not begun
    named[3593]:   validating ./DNSKEY: no valid signature found (DS)
    named[3593]: broken trust chain resolving './NS/IN': 199.7.83.42#53
    named[3593]: resolver priming query complete: broken trust chain

## Third-party Web-based diagnostics

There are some public third-party web-based tools that will check the status of DNSSEC of a public domain. Here are some:

 * https://dnsviz.net/: Returns a graphical diagram showing the chain of trust and where it breaks down, if that's the case.
 * https://dnssec-debugger.verisignlabs.com/: A DNSSEC debugger which also shows the chain of trust and where it breaks down, in a table format.

## Further reading

 * [bind9's guide to DNSSEC troubleshooting](https://bind9.readthedocs.io/en/latest/dnssec-guide.html#basic-dnssec-troubleshooting)
 * {manpage}`delv(1)` manpage
 * {manpage}`dig(1)` manpage
