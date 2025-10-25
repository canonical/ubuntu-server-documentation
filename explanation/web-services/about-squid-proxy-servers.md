(about-squid-proxy-servers)=
# About Squid proxy servers

[Squid](http://www.squid-cache.org/) is a proxy caching server which provides proxy and cache services for Hyper Text Transport Protocol (HTTP), File Transfer Protocol (FTP), and other popular network protocols. 

It acts as an intermediary between web servers and clients. When a client sends a request for content, Squid fetches the content from the web server and creates a local copy. Then, if a request is made again, it shows the local, cached copy instead of making another request to the web server. In this way, performance is improved and network bandwidth is optimised. It can also filter web traffic, helping to improve security.

## Features

The Squid proxy cache server scales from the branch office to enterprise level networks. It provides extensive, granular access controls, and monitoring of critical parameters via the Simple Network Management Protocol (SNMP).

When selecting a computer system for use as a dedicated Squid caching proxy server, it is helpful to configure it with a large amount of physical memory as Squid maintains an in-memory cache for increased performance.

## Caching

Squid implements a sophisticated caching system that stores frequently requested web content locally, reducing bandwidth usage and improving response times. When a client requests web content, Squid follows this process:

1. Checks if the requested content exists in its cache
2. If found (cache hit), validates if the content is still fresh using HTTP headers
3. If fresh, serves the content directly from cache
4. If not found (cache miss) or stale, fetches the content from the origin server

### Cache Storage

Squid offers multiple storage types for its cache:
- Memory cache (in-RAM) for fastest access
- Disk cache for larger storage capacity
- Hierarchical cache directories for efficient file organization

### Cache Control Factors

Several factors determine whether and how long content is cached:

1. HTTP Headers
   - Cache-Control directives from origin servers
   - Expires headers
   - Last-Modified timestamps
   - ETag values

2. Squid Configuration
   - `cache_dir` settings for disk cache size and structure
   - `maximum_object_size` limiting cache entry size
   - `minimum_object_size` for efficiency
   - `refresh_pattern` rules for cache retention policies

3. Content Type
   - Static content (images, CSS, JS) is highly cacheable
   - Dynamic content may require special configuration
   - HTTPS traffic needs SSL bump configuration to cache

For installation and configuration instructions, refer to {ref}`our installation guide <install-a-squid-server>`.

## Further reading

- [The Squid website](http://www.squid-cache.org/)

- [Ubuntu Wiki page on Squid](https://help.ubuntu.com/community/Squid).
