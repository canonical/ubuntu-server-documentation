(install-dnssec)=
# Installing DNS Security Extensions (DNSSEC)

DNSSEC is a set of security extensions to [DNS](https://documentation.ubuntu.com/server/reference/glossary/#term-DNS) which allow DNS data to be verified for authenticity and integrity.

This guide will show you how to enable DNSSEC for an existing zone in your BIND9 DNS server deployment.

## Starting point
The starting point for this how-to is an existing BIND9 DNS server deployed with an authoritative zone. For details on how to deploy BIND9 in this fashion, please see the {ref}`DNS How-To <install-dns>`. One key difference from that guide, however, is that we need the zone file to be in a directory where the server can write to, like `/var/lib/bind`, instead of `/etc/bind`.

Nevertheless, here is a quick set of steps to reach that state for an example domain called `example.internal`.

First, install the `bind9` package:

    sudo apt install bind9 -y

Edit `/etc/bind/named.conf.local` and add this *zone* block:

    zone "example.internal" {
        type master;
        file "/var/lib/bind/db.example.internal";
    };

Create the file `/var/lib/bind/db.example.internal` with these contents:

    $TTL 86400      ; 1 day
    example.internal.       IN SOA  example.internal. root.example.internal. (
                                    1          ; serial
                                    43200      ; refresh (12 hours)
                                    900        ; retry (15 minutes)
                                    1814400    ; expire (3 weeks)
                                    7200       ; minimum (2 hours)
                                    )
    example.internal.       IN  NS      ns.example.internal.
    ns                      IN  A       192.168.1.10
    noble                   IN  A       192.168.1.11

Restart the service:

    sudo systemctl restart named

Check if the service can resolve the name `noble.example.internal`:

    $ dig @127.0.0.1 +short noble.example.internal
    192.168.1.11

## Enabling DNSSEC
Enabling DNSSEC for a zone involves multiple steps. Thankfully for us, the BIND9 DNS server takes care of all of them by default, automatically, leaving very little for us to do. Converting a zone in this way means at least generating new keys, and signing all the Resource Records of the zone. But that is only "day 1": such a zone must be maintained properly. Keys must be rotated, expiration dates must be set, etc. The current versions of BIND9 take care of that with a DNSSEC policy, and of course there is a default one that can be used from the start.

To migrate our *example.internal* zone to DNSSEC, we just need to add two lines to its definition in `/etc/bind/named.conf.local`, so that it looks like this:

    zone "example.internal" {
        type master;
        file "/var/lib/bind/db.example.internal";
        dnssec-policy default;
        inline-signing yes;
    };

What was added:

 * `dnssec-policy default`: Use the default DNSSEC policy. A DNSSEC policy includes settings for key rotation, default TTL, and many others.
 * `inline-signing yes`: keep a separate file for the signed zone.

After this change, there is no need to restart the service, but it needs to be told to reload its configuration. This can be done with the `rndc` tool:

    sudo rndc reconfig

The server will immediately notice the new configuration and start the process to sign the *example.internal* zone. The journal logs will show the progress, and can be inspected with the command:

    sudo journalctl -u named.service -f

The logs will show something similar to this:

    named[3246]: zone example.internal/IN (unsigned): loaded serial 1
    named[3246]: zone example.internal/IN (signed): loaded serial 1
    named[3246]: zone example.internal/IN (signed): receive_secure_serial: unchanged
    named[3246]: zone example.internal/IN (signed): sending notifies (serial 1)
    named[3246]: zone example.internal/IN (signed): reconfiguring zone keys
    named[3246]: keymgr: DNSKEY example.internal/ECDSAP256SHA256/44911 (CSK) created for policy default
    named[3246]: Fetching example.internal/ECDSAP256SHA256/44911 (CSK) from key repository.
    named[3246]: DNSKEY example.internal/ECDSAP256SHA256/44911 (CSK) is now published
    named[3246]: DNSKEY example.internal/ECDSAP256SHA256/44911 (CSK) is now active
    named[3246]: zone example.internal/IN (signed): next key event: 23-Oct-2024 22:47:12.544
    named[3246]: any newly configured zones are now loaded
    named[3246]: running
    named[3246]: resolver priming query complete: success
    named[3246]: managed-keys-zone: Key 20326 for zone . is now trusted (acceptance timer complete)
    named[3246]: zone example.internal/IN (signed): sending notifies (serial 3)

Depending on the zone size, signing all records can take longer.

A few interesting events can be seen in the logs above:

  * Keys were generated for the *example.internal* zone.
  * The *example.internal* zone became signed.
  * A *key event* was scheduled. This is BIND9 also taking care of the maintenance tasks of the signed zone and its keys.
  * Since the zone changed, its serial number was incremented (started as 1, now it's 3).

The DNSSEC keys are kept in `/var/cache/bind`:

    -rw-r--r-- 1 bind bind  413 Oct 23 20:50 Kexample.internal.+013+48112.key
    -rw------- 1 bind bind  215 Oct 23 20:50 Kexample.internal.+013+48112.private
    -rw-r--r-- 1 bind bind  647 Oct 23 20:50 Kexample.internal.+013+48112.state

This is the bulk of the work. This zone is now signed, and maintained automatically by BIND9 using the *default* DNSSEC policy.

## Verification

The zone that was just signed is almost ready to serve DNSSEC. Let's perform some verification steps.

As it is now, this zone *example.internal* is "disconnected" from the parent zone. Its name was made up for this guide, but even if it represented a real domain, it would still be missing the connection to the parent zone. Remember that DNSSEC relies on the chain of trust, and the parent of our zone needs to be able to vouch for it.

Before taking that step, however, it's important to verify if everything else is working. In particular, we would want to perform some DNSSEC queries, and perform validation. A good tool to perform this validation is `delv`.

`delv` is similar to `dig`, but it will perform validation on the results using the same internal resolver and validator logic as the BIND9 server itself.

Since our zone is disconnected, we need to tell `delv` to use the public key created for the zone as a trusted anchor, and to not try to reach out to the root servers of the internet.

First, copy the public zone key somewhere else so it can be edited. For example:

    cp /var/cache/bind/Kexample.internal.+013+48112.key /tmp/example.key

That file will have some comments at the top, and then have a line that starts with the zone name, like this (the full key was truncated below for brevity):

    example.internal. 3600 IN DNSKEY 257 3 13 jkmS5hfyY3nSww....

We need to make some changes here:

 * Remove the comment lines from the top.
 * Edit that line and replace the `3600 IN DNSKEY` text with `static-key`.
 * The key material after the `13` number must be enclosed in double quotes (`"`).
 * The line needs to end with a `;`.
 * And finally the line needs to be inside a `trust-anchors` block.

 In the end, the `/tmp/example.key` file should look like this:

    trust-anchors {
        example.internal. static-key 257 3 13 "jkmS5hfyY3nSww....";
    };

Now `delv` can be used to query the *example.internal* zone and perform DNSSEC validation:

    $ delv @127.0.0.1 -a /tmp/example.key +root=example.internal noble.example.internal +multiline
    ; fully validated
    noble.example.internal. 86400 IN A 192.168.1.11
    noble.example.internal. 86400 IN RRSIG A 13 3 86400 (
                                    20241106131533 20241023195023 48112 example.internal.
                                    5fL4apIwCD9kt4XbzzlLxMXY3mj8Li1WZu3qzlcBpERp
                                    lXPgLODbRrWyp7L81xEFnfhecKtEYv+6Y0Xa5iVRug== )

This output shows important DNSSEC attributes:

 * `; fully validated`: The DNSSEC validation was completed successfully, and the presented data is authenticated.
 * `RRSIG`: This is the signature Resource Record that accompanies the `A` record from the result.

## Connecting the dots: the parent zone
In order to complete the chain of trust, the parent zone needs to be able to vouch for the child zone we just signed. How this is exactly done varies, depending on who is the administrator of the parent zone. It could be as simple as just pasting the DS or DNSKEY records in a form.

Typically what is needed is either a DS record, or a DNSKEY record. Here is how to produce them, ready to be sent to the parent.

### DS record format
A DS record can be produced from the zone public key via the `dnssec-dsfromkey` tool. For example:

    $ dnssec-dsfromkey /var/cache/bind/Kexample.internal.+013+48112.key
    example.internal. IN DS 48112 13 2 1212DE7DA534556F1E11898F2C7A66736D5107962A19A0BFE1C2A67D6841962A

### DNSKEY record format
The DNSKEY format doesn't need tooling, and can be found directly in the zone's public key file, after the lines that start with the comment delimiter `;`:

    $ cat /var/cache/bind/Kexample.internal.+013+48112.key
    ; This is a key-signing key, keyid 48112, for example.internal.
    ; Created: 20241023205023 (Wed Oct 23 20:50:23 2024)
    ; Publish: 20241023205023 (Wed Oct 23 20:50:23 2024)
    ; Activate: 20241023205023 (Wed Oct 23 20:50:23 2024)
    ; SyncPublish: 20241024215523 (Thu Oct 24 21:55:23 2024)
    example.internal. 3600 IN DNSKEY 257 3 13 jkmS5hfyY3nSww4tD9Fy5d+GGc3A/zR1CFUxmN8T2TKTkgGWp8dusllM 7TrIZTEg6wZxmMs754/ftoTA6jmM1g==

Taking that line, the actual record to send to the parent zone just needs a little bit of tweaking so it looks like this:

    example.internal. 3600 IN DNSKEY 257 3 13 (jkmS5hfyY3nSww4tD9Fy5d+GGc3A/zR1CFUxmN8T2TKTkgGWp8dusllM 7TrIZTEg6wZxmMs754/ftoTA6jmM1g==);


## Further reading

 * [The DNSSEC Guide from bind9](https://bind9.readthedocs.io/en/stable/dnssec-guide.html)
 * [Easy-Start Guide for Signing Authoritative Zones](https://bind9.readthedocs.io/en/stable/dnssec-guide.html#signing)
 * [Creating a Custom DNSSEC Policy](https://bind9.readthedocs.io/en/stable/dnssec-guide.html#signing-custom-policy)
 * [Detailed DNSSEC chapter from the bind9 documentation](https://bind9.readthedocs.io/en/stable/chapter5.html)
 * [`delv` manual page](https://manpages.ubuntu.com/manpages/noble/man1/delv.1.html)
 * [Working with the parent zone](https://bind9.readthedocs.io/en/latest/dnssec-guide.html#working-with-the-parent-zone)
