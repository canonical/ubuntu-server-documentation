(bind-9-dnssec-cryptography-selection)=
# BIND 9 DNSSEC cryptography selection

Domain Name System Security Extensions (DNSSEC), which provides a set of security features to [DNS](https://documentation.ubuntu.com/server/reference/glossary/#term-DNS), is a broad topic. In this article, we will briefly show DNSSEC validation happening on a `bind9` DNS server, and then introduce the topic of how we can disable certain cryptographic algorithms from being used in this validation.

## DNSSEC validation

Out of the box, the BIND 9 DNS server is configured to try to use DNSSEC whenever it's available, doing all the validation checks automatically. This is done via the `dnssec-validation` setting in `/etc/bind/named.conf.options`:

```text
options {
    (...)
    dnssec-validation auto;
    (...)
};
```

This can be quickly checked with the help of `dig`. Right after you installed `bind9`, you can run `dig` and ask it about the `isc.org` domain:

```text
$ dig @127.0.0.1 isc.org +dnssec +multiline

; <<>> DiG 9.18.12-0ubuntu0.22.04.1-Ubuntu <<>> @127.0.0.1 isc.org +dnssec +multiline
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 57669
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
; COOKIE: 71aa6b4e4ca6bb4b01000000643fee81edf0840b48d28d44 (good)
;; QUESTION SECTION:
;isc.org.		IN A

;; ANSWER SECTION:
isc.org.		300 IN A 149.20.1.66
isc.org.		300 IN RRSIG A 13 2 300 (
				20230510161711 20230410161439 27566 isc.org.
				EUA5QPEjtVC0scPsvf1c/EIBKHRpS8ektiWiOqk6nb3t
				JhJAt9uCr3e0KNAcc3WDU+wJzEvqDyJrlZoELqT/pQ== )

;; Query time: 740 msec
;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
;; WHEN: Wed Apr 19 13:37:05 UTC 2023
;; MSG SIZE  rcvd: 183
```

We can see that a `RRSIG` DNSSEC record was returned, but the important information in this output is the `ad` flag near the top. That stands for "authenticated data", and means that the DNSSEC records in the response were validated.

To see an example where this verification fails, we can use the `www.dnssec-failed.org` domain, which is specially crafted for this:

```text
$ dig @127.0.0.1 www.dnssec-failed.org +dnssec +multiline

; <<>> DiG 9.18.12-0ubuntu0.22.04.1-Ubuntu <<>> @127.0.0.1 www.dnssec-failed.org +dnssec +multiline
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 56056
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
; COOKIE: 541f6c66a216acdb01000000643fef9ebb21307fee2ea0e3 (good)
;; QUESTION SECTION:
;www.dnssec-failed.org.	IN A

;; Query time: 1156 msec
;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
;; WHEN: Wed Apr 19 13:41:50 UTC 2023
;; MSG SIZE  rcvd: 78
```

Here we see that:

* There is no `IN A` IP address shown in the reply
* The status is `SERVFAIL`
* There is no `ad` flag

In the `bind9` logs, we will see DNSSEC validation errors:

```text
$ journalctl -u named.service -n 10

Apr 19 13:41:50 j named[3018]: validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
Apr 19 13:41:50 j named[3018]: no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 68.87.76.228#53
Apr 19 13:41:50 j named[3018]: broken trust chain resolving 'www.dnssec-failed.org/A/IN': 68.87.85.132#53
(...)
```

We can run `dig` with the `+cd` command line parameter which disables this verification, but notice that still we don't get the `ad` flag in the reply:

```text
$ dig @127.0.0.1 www.dnssec-failed.org +dnssec +multiline +cd

; <<>> DiG 9.18.12-0ubuntu0.22.04.1-Ubuntu <<>> @127.0.0.1 www.dnssec-failed.org +dnssec +multiline +cd
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42703
;; flags: qr rd ra cd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
; COOKIE: 3d6a4f4ff0014bdc01000000643ff01c3229ed7d798c5f8d (good)
;; QUESTION SECTION:
;www.dnssec-failed.org.	IN A

;; ANSWER SECTION:
www.dnssec-failed.org.	7031 IN	A 68.87.109.242
www.dnssec-failed.org.	7031 IN	A 69.252.193.191
www.dnssec-failed.org.	7074 IN	RRSIG A 5 3 7200 (
				20230505145108 20230418144608 44973 dnssec-failed.org.
				R6/u+5Gv3rH93gO8uNvz3sb9ErQNuvFKu6W5rtUleXF/
				vkqJXbNe8grMuiV6Y+CNEP6jRBu0jOBPncb5cXbfcmfo
				CoVOjpsLySxt4D1EUl4yByWm2ZAdXRrk6A8SaldIdDv8
				9t+FguTdQrZv9Si+afKrLyC7L/mltXMllq3stDI= )

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
;; WHEN: Wed Apr 19 13:43:56 UTC 2023
;; MSG SIZE  rcvd: 287
```

## Restricting DNSSEC algorithms

It's possible to limit the cryptographic algorithms used by BIND to validate DNSSEC records. This is done via two configuration settings, located inside the `options { }` block of `/etc/named/named.conf.options`:

* `disable-algorithms "<domain>" { a; b; ... };`
   Disables the listed algorithms for the specified domain and all subdomains of it.

* `disable-ds-digests "<domain>" { a; b; ... };`
   Disables the listed digital signature digests for the specified domain and all subdomains of it.

For example, the following disables `RSAMD5`, `DSA` and `GOST` for all zones:

```text
disable-algorithms "." {
    RSAMD5;
    DSA;
};
disable-ds-digest "." {
    GOST;
};
```

The list of algorithm names can be obtained at [DNSSEC Algorithm Numbers](https://www.iana.org/assignments/dns-sec-alg-numbers/dns-sec-alg-numbers.xhtml), in the **Mnemonic** column of the **Available Formats** table. The algorithm number is also standardised, and is part of the DNSSEC records.

For example, if we go back to the `dig` result from before where we inspected the `isc.org` domain, the `RRSIG` record had this (showing just the first line for brevity):

```text
isc.org.        300 IN RRSIG A 13 2 300 (
```

In that record, the number `13` is the algorithm number, and in this case it means the algorithm `ECDSAP256SHA256` was used.

Just to see how BIND would react to an algorithm being disabled, let's temporarily add `ECDSAP256SHA256` to the list of disabled algorithms:

```text
disable-algorithms "." {
   RSAMD5;
   DSA;
   ECDSAP256SHA256;
};
```

And restart BIND:

```text
sudo systemctl restart bind9.service
```

Now the `ad` flag is gone, meaning that this answer wasn't validated:

```text
$ dig @127.0.0.1 isc.org +dnssec +multiline

; <<>> DiG 9.18.1-1ubuntu1-Ubuntu <<>> @127.0.0.1 isc.org +dnssec +multiline
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 43893
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
; COOKIE: 6527ce585598025d01000000643ff8fa02418ce38af13fa7 (good)
;; QUESTION SECTION:
;isc.org.               IN A

;; ANSWER SECTION:
isc.org.                300 IN A 149.20.1.66
isc.org.                300 IN RRSIG A 13 2 300 (
                                20230510161711 20230410161439 27566 isc.org.
                                EUA5QPEjtVC0scPsvf1c/EIBKHRpS8ektiWiOqk6nb3t
                                JhJAt9uCr3e0KNAcc3WDU+wJzEvqDyJrlZoELqT/pQ== )

;; Query time: 292 msec
;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
;; WHEN: Wed Apr 19 14:21:46 UTC 2023
;; MSG SIZE  rcvd: 183
```

The logs only say there was no valid signature found:

```text
Apr 19 14:23:01 j-bind9 named[2786]: validating isc.org/A: no valid signature found
```

Note this is different from rejecting the response: it just means that this response is being treated as if it didn't have any DNSSEC components in it, or in other words, it's treated as "insecure".

In general, as always with cryptography, be careful with which algorithms you decide to disable and remove from DNSSEC validation, as such errors can be hard to diagnose. To help with troubleshooting, the Internet Systems Consortium (ISC) has published a very extensive DNSSEC guide, which contains a detailed troubleshooting section (see below).

> **Note**:
> Remember now to remove the disabling of `ECDSAP256SHA256` from `/etc/bind/named.conf.options` and restart BIND 9. This change was just a quick test!

## References

* [ISC's DNSSEC Guide](https://bind9.readthedocs.io/en/v9.18.14/dnssec-guide.html)
* [DNSSEC troubleshooting section of the ISC DNSSEC guide](https://bind9.readthedocs.io/en/v9.18.14/dnssec-guide.html#basic-dnssec-troubleshooting)
* [Standard algorithms used for DNSSEC](https://www.iana.org/assignments/dns-sec-alg-numbers/dns-sec-alg-numbers.xhtml)
