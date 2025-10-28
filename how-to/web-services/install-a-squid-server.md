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

Using the `refresh_pattern` configuration directive controls how long cached objects stay fresh before they need to be revalidated with the origin server. It is configured as:

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
If a formerly customised squid3 was used to set up the spool at `/var/log/squid3` to be a mount point, but otherwise kept the default configuration, the upgrade will fail. The upgrade tries to rename/move files as needed, but it can't do so for an active mount point. In that case you will need to adapt either the mount point or the config in `/etc/squid/squid.conf` so that they match.
The same applies if the **include** config statement was used to pull in more files from the old path at `/etc/squid3/`. In those cases you should move and adapt your configuration accordingly.
```

## Troubleshooting

### Diagnosing Caching Issues

Before making any changes, gather information about your Squid server's current state:

1. Check Squid Status and Version
   ```bash
   # Verify Squid version
   sudo squid -v
   
   # Check service status
   sudo systemctl status squid
   ```

2. Monitor Logs in Real-time
   ```bash
   # Watch access log for cache hits/misses
   sudo tail -f /var/log/squid/access.log
   
   # Check cache log for errors
   sudo tail -f /var/log/squid/cache.log
   ```

3. Review Cache Statistics
   ```bash
   # Get cache manager statistics
   squidclient mgr:info
   ```

### Common Cache Issues and Solutions

#### 1. Cache Directory Problems
```text
# Proper cache directory configuration
cache_dir ufs /var/spool/squid 5000 16 256

# Check directory permissions
sudo chown proxy:proxy /var/spool/squid
sudo chmod 750 /var/spool/squid
```
- Ensure cache_dir is uncommented
- Set appropriate cache size (5000 MB in example)
- Verify permissions for Squid user (usually 'proxy')

#### 2. Object Size Configuration
```text
# Adjust object size limits
maximum_object_size 100 MB
minimum_object_size 0 KB
maximum_object_size_in_memory 512 KB
```
- Increase limits if large files aren't being cached
- Monitor cache.log for size-related rejections
- Balance memory cache size with server resources

#### 3. Access Control Configuration
```text
# Example ACL configuration
acl ALLOWED_CLIENTS src 192.168.1.0/24
http_access allow ALLOWED_CLIENTS

# For HTTPS traffic
ssl_bump server-first all
sslcrtd_program /usr/lib/squid/security_file_certgen -s /var/lib/squid/ssl_db -M 4MB
```
- Verify client IPs match ACLs
- Configure SSL bump for HTTPS caching
- Check for TCP_DENIED in access.log

#### 4. Cache Retention Rules
```text
# Optimized refresh patterns
refresh_pattern -i \.(gif|png|jpg|jpeg|ico)$ 1440 20% 10080
refresh_pattern -i \.(css|js)$ 1440 20% 4320
refresh_pattern -i \.(html|htm)$ 1440 20% 2880
refresh_pattern . 0 20% 4320
```
- Adjust patterns based on content types
- Monitor effectiveness with access.log
- Balance freshness vs cache hits

### Verifying and Monitoring Cache Performance

1. Check Cache Hit Rates
   ```bash
   # Monitor cache hits
   squidclient mgr:info | grep "Hit Rate"
   
   # Watch for cache hits in real-time
   sudo tail -f /var/log/squid/access.log | grep 'TCP_HIT\|TCP_MEM_HIT'
   ```

2. Analyze Access Log Entries
   - TCP_HIT: Served from cache
   - TCP_MISS: Not in cache
   - TCP_REFRESH_HIT: Validated with origin
   - TCP_TUNNEL: HTTPS traffic (not cached)
   - TCP_DENIED: Blocked by ACLs

3. Advanced Debugging
   ```text
   # Enable detailed logging
   debug_options ALL,1 28,3
   
   # Check cache directory status
   sudo squid -k check
   ```

4. Reset Corrupt Cache
   ```bash
   # Clear and reinitialize cache
   sudo systemctl stop squid
   sudo rm -rf /var/spool/squid/*
   sudo squid -z
   sudo systemctl start squid
   ```

### Applying Configuration Changes

After making changes to squid.conf:

1. Back up the configuration
   ```bash
   sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.backup
   ```

2. Validate and apply changes
   ```bash
   # Check configuration syntax
   sudo squid -k parse
   
   # Restart Squid service
   sudo systemctl restart squid
   
   # Verify service status
   sudo systemctl status squid
   ```

### Verifying Caching Effectiveness

After applying configuration changes, follow these steps to verify that Squid is caching content correctly:

#### 1. Monitor Real-time Caching Activity
```bash
# Watch access log in real-time
sudo tail -f /var/log/squid/access.log
```

While monitoring, look for these cache status indicators:
- `TCP_MISS`: Content not in cache, fetched from origin
- `TCP_HIT`: Content served from disk cache
- `TCP_MEM_HIT`: Content served from memory cache
- `TCP_REFRESH_HIT`: Cached content revalidated with origin
- `TCP_TUNNEL`: HTTPS traffic (not cached without SSL bump)

Test caching by:
1. Configure a client browser to use the proxy
2. Visit a website with static content (images, CSS, JS)
3. Visit the same site again
4. First visit should show `TCP_MISS`, second should show `TCP_HIT`

#### 2. Analyze Cache Statistics
```bash
# Get detailed cache statistics
squidclient mgr:info

# Filter for hit ratios
squidclient mgr:info | grep -i "hit ratio"
```

Look for:
- Request Hit Ratios (should be > 0%)
- Byte Hit Ratios (indicates bandwidth savings)
- Memory and Disk utilization
- Number of objects cached

A healthy cache should show:
- Increasing hit ratios over time
- Non-zero byte hit ratios
- Growing number of cached objects

#### 3. Monitor Cache Directory Growth
```bash
# Check initial cache size
sudo du -sh /var/spool/squid

# List cache directories
sudo ls -l /var/spool/squid

# Monitor directory size changes
watch -n 60 'sudo du -sh /var/spool/squid'
```

Verify:
- Cache directory size increases with usage
- New swap directories are created
- Proper permissions for Squid user

#### 4. Check for Error Conditions
```bash
# Review cache log for errors
sudo tail -n 100 /var/log/squid/cache.log

# Monitor for new errors
sudo tail -f /var/log/squid/cache.log | grep -i "error\|warn\|fatal"
```

Success Criteria:
1. Access log shows mix of `TCP_MISS` and `TCP_HIT`
2. Cache hit ratios are positive and increasing
3. Cache directory shows growth
4. No critical errors in logs
5. Clients report improved response times

## Further reading

- [The Squid Website](http://www.squid-cache.org/)

- [Ubuntu Wiki page on Squid](https://help.ubuntu.com/community/Squid).
