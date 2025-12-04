(install-a-squid-server)=
# How to install a Squid server

Squid is a filtering and caching mechanism for web servers that can optimise bandwidth and performance. For more information about Squid proxy servers, {ref}`refer to this guide <about-squid-proxy-servers>`.

## Install Squid

At a terminal prompt, enter the following command to install the Squid server:

```bash
sudo apt install squid
```

## Configure Squid

Squid is configured by editing directives in the `/etc/squid/squid.conf` configuration file. The following examples illustrate a sample of directives that can be modified to configure the Squid server's behavior. For more in-depth configuration details, see the links at the bottom of the page.

### Protect the original config file

Before editing the configuration file, you should make a copy of the original and protect it from writing. You will then have the original settings as a reference, and can reuse it when needed. Run the following commands to make a copy of the original configuration file and protect it from being written to:

```bash
sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.original
sudo chmod a-w /etc/squid/squid.conf.original
```

### Change TCP port

To set your Squid server to listen on TCP port 8888 instead of the default TCP port 3128, change the **`http_port`** directive as such:

```text
http_port 8888
```

### Set the hostname

Change the **`visible_hostname`** directive to give the Squid server a specific {term}`hostname`. This hostname does not need to be the same as the computer's hostname. In this example it is set to `weezie`:

```text
visible_hostname weezie
```

### Configure the memory cache

The default setting is to use on-memory cache. This example tells squid to use up to 512MB of memory, erasing the last recently used content when the cache is full to free space for new items:

```text
cache_mem 512 MB
maximum_memory_policy lru
```

### Configure on-disk cache

By changing the **`cache_dir`** directive you can configure use of an on-disk cache. The `cache_dir` directive takes the following arguments:

```text
cache_dir <Type> <Directory-Name> <Size-in-MB> <L1-Dirs> <L2-Dirs> [options]
```

In this example we set the cache configuration to use a `ufs` storage in `/var/spool/squid`, up to 10GB, with 16 directories on the first level of the hierarchy, each of those containing 256 directories for organization.

```text
cache_dir ufs /var/spool/squid 10000 16 256
```

The available storage types are:
* `ufs`: This is the common Squid storage format, good for general use.
* `aufs`: Uses the same storage format as `ufs`, using POSIX-threads to avoid blocking the main Squid process on disk-I/O. This was formerly known in Squid as `async-io`.
* `diskd`: Uses the same storage format as `ufs`, using a separate process to avoid blocking the main Squid process on disk-I/O.
* `rock`: This is a database-style storage. All cached entries are stored in a "database" file, using fixed-size slots. A single entry occupies one or more slots.

### Configure cached objects size limits

The following configuration directives control which objects get cached based on their size, for space optimization, both on disk and in memory:

```text
maximum_object_size 512 MB
minimum_object_size 0 KB
maximum_object_size_in_memory 512 KB
```

### Configure cached objects lifetime

Using the `refresh_pattern` configuration directive controls how long cached objects stay fresh before they need to be re-validated with the origin server. It is configured as:

```text
refresh_pattern regex min percent max [options]
```

where `regex` needs to match against the filename, `min` and `max` set the time limits in minutes for freshness, and a `percent` of the object's age to calculate the refresh threshold.

In the following example, static web assets (such as images, css and scripts) are configured to be kept for 7 to 30 days + 90% of their age, based on the `Last-Modified` header, while everything else is kept up to 3 days + 20% of their age.

```text
refresh_pattern -i \.(gif|jpg|png|css|js)$  10080  90%  43200
refresh_pattern .                           0      20%  4320
```

### Caching HTTPS content

By default, Squid can't cache HTTPS because the traffic is encrypted. There are different strategies for enabling HTTPS caching, such as TLS interception via `CONNECT` requests, origin server caching based on `Cache-Control` and `ETag` headers, or access-control only solutions.

Please refer to the [Squid HTTPS documentation](https://wiki.squid-cache.org/Features/HTTPS) to learn more.

### Other caching configuration options

Different options can be used to fine-tune the caching behavior overall, by determining how squid stores files in the hierarchy, the algorithm for the replacement policy, DNS cache settings, compatibility with different scenarios, and more.

For a full list of configuration entries, please refer to the [Squid configuration guide](https://www.squid-cache.org/Doc/config/).

### Access control

Using Squid's access control, you can configure use of Squid-proxied Internet services to be available only to users with certain Internet Protocol (IP) addresses. For example, we will illustrate access by users of the `192.168.42.0/24` subnetwork only:

* Add the following to the **bottom** of the {term}`ACL` section of your `/etc/squid/squid.conf` file:
   
   ```text
   acl fortytwo_network src 192.168.42.0/24
   ```

* Then, add the following to the **top** of the `http_access` section of your `/etc/squid/squid.conf` file:
    
   ```text
   http_access allow fortytwo_network
   ```

Using Squid's access control features, you can configure Squid-proxied Internet services to only be available during normal business hours. As an example, we'll illustrate access by employees of a business which is operating between 9:00AM and 5:00PM, Monday through Friday, and which uses the `10.1.42.0/24` subnetwork:
    
* Add the following to the **bottom** of the ACL section of your `/etc/squid/squid.conf` file:

   ```text
   acl biz_network src 10.1.42.0/24
   acl biz_hours time M T W T F 9:00-17:00
   ```

* Then, add the following to the **top** of the `http_access` section of your `/etc/squid/squid.conf` file:

   ```text
   http_access allow biz_network biz_hours
   ```

## Restart the Squid server

After making any changes to the `/etc/squid/squid.conf` file, you will need to save the file and restart the squid server application. 

First, you can verify the syntax of your configuration file by running:

```bash
sudo squid -k parse
```

You can restart the server using the following command:

```bash
sudo systemctl restart squid.service
```

```{note}
If a formerly customized squid3 was used to set up the spool at `/var/log/squid3` to be a mount point, but otherwise kept the default configuration, the upgrade will fail. The upgrade tries to rename/move files as needed, but it can't do so for an active mount point. In that case you will need to adapt either the mount point or the config in `/etc/squid/squid.conf` so that they match.
The same applies if the **include** config statement was used to pull in more files from the old path at `/etc/squid3/`. In those cases you should move and adapt your configuration accordingly.
```

## Troubleshooting

To monitor Squid behavior and check for potential errors and problems, there are useful commands to be executed and files to be checked.

Squid version and status can be checked with:

```bash
sudo squid -v
sudo systemctl status squid
```

Checking or watching the log files may be useful to see potential errors, and to verify cache hits and misses:

```bash
sudo cat /var/log/squid/cache.log
sudo cat /var/log/squid/access.log
```

For a status summary containing runtime statistics and configuration, run:

```bash
squidclient mgr:info
```

While monitoring, these cache status indicators can help identifying what is happening with requests:
- `TCP_MISS`: Content not in cache, fetched from origin
- `TCP_HIT`: Content served from disk cache
- `TCP_MEM_HIT`: Content served from memory cache
- `TCP_REFRESH_HIT`: Cached content re-validated with origin
- `TCP_TUNNEL`: HTTPS traffic (not cached by default)

A healthy cache should show increasing hit ratios over time, of non-zero size, and a growing number of cached objects.

## Further reading

- [The Squid Website](http://www.squid-cache.org/)

- [Ubuntu Wiki page on Squid](https://help.ubuntu.com/community/Squid).
