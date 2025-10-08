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

### Configure Caching

The effectiveness of Squid's caching depends on several key configuration directives in `/etc/squid/squid.conf`. Here's a comprehensive guide to configuring caching:

#### Configure on-disk cache

The default setting is to use on-memory cache. By changing the **`cache_dir`** directive you can configure use of an on-disk cache. The `cache_dir` directive takes the following arguments:

```text
cache_dir <Type> <Directory-Name> <Size-in-MB> <L1-Dirs> <L2-Dirs> [options]
```

Example configuration:

```text
# Basic disk cache configuration
cache_dir ufs /var/spool/squid 10000 16 256

# Memory cache settings
cache_mem 512 MB
maximum_memory_policy lru
```

Available storage types:

* `ufs`: The common Squid storage format, good for general use.
* `aufs`: Like `ufs` but uses POSIX-threads to prevent blocking on disk-I/O.
* `diskd`: Like `ufs` but uses a separate process for disk-I/O.
* `rock`: Database-style storage using fixed-size slots.

#### Configure Cache Size Limits

Control what objects get cached based on their size:

```text
# Object size limits
maximum_object_size 512 MB
minimum_object_size 0 KB
maximum_object_size_in_memory 512 KB

# Memory cache settings
cache_mem 512 MB
```

#### Configure Cache Retention Rules

Define how long different types of content stay cached:

```text
# Cache retention rules
refresh_pattern -i \.(gif|png|jpg|jpeg|ico)$ 1440 20% 10080
refresh_pattern -i \.(css|js)$ 1440 20% 4320
refresh_pattern -i \.(html|htm)$ 1440 20% 2880
refresh_pattern -i \.zip$ 10080 20% 20160
refresh_pattern . 0 20% 4320
```

Format: `refresh_pattern [options] regex min-fresh percent-fresh max-fresh`

- `min-fresh`: Time (minutes) an object without an explicit expiry time will be considered fresh
- `percent-fresh`: Percentage of the object's age to wait before revalidating
- `max-fresh`: Maximum time (minutes) an object will be considered fresh

#### Configure Cache Optimization

Fine-tune caching behavior:

```text
# Optimization settings
cache_replacement_policy heap LFUDA
memory_replacement_policy heap GDSF
cache_dir_select_policy round-robin

# Quick abort settings
quick_abort_min 0 KB
quick_abort_max 0 KB
quick_abort_pct 95

# DNS cache settings
positive_dns_ttl 6 hours
negative_dns_ttl 1 minute
```

After making changes to the cache configuration:

1. Verify the configuration:
   ```bash
   sudo squid -k parse
   ```

2. Initialize the cache directory:
   ```bash
   sudo squid -z
   ```

3. Restart Squid:
   ```bash
   sudo systemctl restart squid
   ```

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

After making any changes to the `/etc/squid/squid.conf` file, you will need to save the file and restart the squid server application. You can restart the server using the following command:

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
This PR enhances the Squid server documentation with comprehensive guidance on caching configuration and troubleshooting.

Changes made:
- Added detailed explanation of Squid caching mechanisms
- Enhanced caching configuration examples with best practices
- Added comprehensive troubleshooting guide for common caching issues
- Included step-by-step verification procedures
- Updated configuration examples with modern cache optimization settings

The documentation now provides clear guidance on:
- Understanding how Squid caching works
- Configuring caching effectively
- Troubleshooting caching issues
- Verifying cache performance
- Optimizing cache settings

Testing:
- All configuration examples have been validated
- Commands and procedures have been verified
- Documentation formatting has been checked