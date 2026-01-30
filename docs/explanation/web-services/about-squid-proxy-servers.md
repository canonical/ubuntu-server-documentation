---
myst:
  html_meta:
    description: "Learn about Squid proxy servers for caching web content, access control, and improving network performance on Ubuntu Server."
---

(about-squid-proxy-servers)=
# About Squid proxy servers

[Squid](http://www.squid-cache.org/) is a proxy caching server. It provides proxy and cache services for Hyper Text Transport Protocol (HTTP), File Transfer Protocol (FTP), and other popular network protocols. It acts as an intermediary between web servers and clients, storing content from the web and then providing a local copy for fast access, which improves network performance. It can also filter web traffic, helping to improve security.

The Squid proxy cache server scales from the branch office to enterprise level networks. It provides extensive, granular access controls, and monitoring of critical parameters via the Simple Network Management Protocol (SNMP).

## Caching

Squid improves network performance by storing frequently accessed web content locally. When a client requests content, Squid retrieves it from the origin server and caches a copy. Subsequent requests for the same content are served from the cache, eliminating redundant network traffic and reducing latency.

Besides HTTP and FTP, Squid can implement caching and proxying of Secure Sockets Layer (SSL) requests and caching of Domain Name Server ({term}`DNS`) lookups, and perform transparent caching. Squid also supports a wide variety of caching protocols, such as Internet Cache Protocol (ICP), the Hyper Text Caching Protocol (HTCP), the Cache Array Routing Protocol (CARP), and the Web Cache Coordination Protocol (WCCP).

Squid caching can be done in-RAM for fastest access, on disk for larger capacity, and may use a hierarchical directory structure for efficient file organization.

## Filtering

Squid provides access control and content filtering capabilities through Access Control Lists (ACLs). ACLs define rules that match specific traffic characteristics, which are then combined with allow/deny directives to control request handling. This enables administrators to implement security policies, restrict access to inappropriate content, and manage bandwidth consumption.

Filters can be applied based on source criteria (client IP addresses, network ranges, authenticated usernames), destination criteria (domain names, URL patterns, destination IPs, port numbers), content characteristics (MIME types, file extensions, HTTP methods), temporal restrictions (time of day, day of week, date ranges), protocol attributes (HTTP headers, request methods, SSL certificate properties), and content keywords (regular expressions matching URLs or request content).

## Installing and configuring

If you would like to know how to install and configure your own Squid server, refer to {ref}`our installation guide <install-a-squid-server>`.

## Further reading

- [The Squid website](http://www.squid-cache.org/)

- [Ubuntu Wiki page on Squid](https://help.ubuntu.com/community/Squid).
