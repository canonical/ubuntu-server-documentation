(how-to-install-a-squid-server)=
# How to install a Squid server

Squid is a filtering and caching mechanism for web servers that can optimise bandwidth and performance. For more information about Squid proxy servers, [refer to this guide](../explanation/about-squid-proxy-servers.md).

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

Change the **`visible_hostname`** directive to give the Squid server a specific hostname. This hostname does not need to be the same as the computer's hostname. In this example it is set to `weezie`:
    
```text
visible_hostname weezie
```

### Configure on-disk cache

The default setting is to use on-memory cache. By changing the **`cache_dir`** directive you can configure use of an on-disk cache. The `cache_dir` directive takes the following arguments:

```text
cache_dir <Type> <Directory-Name> <Fs-specific-data> [options]
```

In the config file you can find the default `cache_dir` directive commented out:

```text
# Uncomment and adjust the following to add a disk cache directory.
#cache_dir ufs /var/spool/squid 100 16 256
```

You can use the default option but you can also customise your cache directory, by changing the `<Type>` of this directory. It can be one of the following options: 

* `ufs`: This is the common Squid storage format.
* `aufs`: Uses the same storage format as `ufs`, using POSIX-threads to avoid blocking the main Squid process on disk-I/O. This was formerly known in Squid as `async-io`.
* `diskd`: Uses the same storage format as `ufs`, using a separate process to avoid blocking the main Squid process on disk-I/O.
* `rock`: This is a database-style storage. All cached entries are stored in a "database" file, using fixed-size slots. A single entry occupies one or more slots.

If you want to use a different directory type please take a look at their different options.

### Access control

Using Squid's access control, you can configure use of Squid-proxied Internet services to be available only to users with certain Internet Protocol (IP) addresses. For example, we will illustrate access by users of the `192.168.42.0/24` subnetwork only:

* Add the following to the **bottom** of the ACL section of your `/etc/squid/squid.conf` file:
   
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

> **Note**:
> If a formerly customised squid3 was used to set up the spool at `/var/log/squid3` to be a mount point, but otherwise kept the default configuration, the upgrade will fail. The upgrade tries to rename/move files as needed, but it can't do so for an active mount point. In that case you will need to adapt either the mount point or the config in `/etc/squid/squid.conf` so that they match.
> The same applies if the **include** config statement was used to pull in more files from the old path at `/etc/squid3/`. In those cases you should move and adapt your configuration accordingly.

## Further reading

- [The Squid Website](http://www.squid-cache.org/)

- [Ubuntu Wiki page on Squid](https://help.ubuntu.com/community/Squid).
