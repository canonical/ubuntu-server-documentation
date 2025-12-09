(configure-apache2-settings)=
# How to configure Apache2 settings

After you have {ref}`installed Apache2 <install-apache2>`, you will likely need to configure it. In this explanatory guide, we will explain the Apache2 server essential configuration parameters.

## Basic directives

Apache2 ships with a "virtual-host-friendly" default configuration -- it is configured with a single default virtual host (using the **VirtualHost** directive) which can be modified or used as-is if you have a single site, or used as a template for additional virtual hosts if you have multiple sites.

If left alone, the default virtual host will serve as your default site, or the site users will see if the URL they enter does not match the **ServerName** directive of any of your custom sites. To modify the default virtual host, edit the file `/etc/apache2/sites-available/000-default.conf`.

```{note}
The directives set for a virtual host only apply to that particular virtual host. If a directive is set server-wide and not defined in the virtual host settings, the default setting is used. For example, you can define a Webmaster email address and not define individual email addresses for each virtual host.
```

If you want to configure a new virtual host or site, copy the `000-default.conf` file into the same directory with a name you choose. For example:

```bash
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/mynewsite.conf
```

Edit the new file to configure the new site using some of the directives described below:

### The **ServerAdmin** directive

> Found in `/etc/apache2/sites-available`

Specifies the email address to be advertised for the server's administrator. The default value is `webmaster@localhost`. This should be changed to an email address that is delivered to you (if you are the server's administrator). If your website has a problem, Apache2 will display an error message containing this email address to report the problem to. 

### The **Listen** directive

> Found in `/etc/apache2/ports.conf`

Specifies the port, and optionally the IP address, Apache2 should listen on. If the IP address is not specified, Apache2 will listen on all IP addresses assigned to the machine it runs on. The default value for the **Listen** directive is `80`. Change this to:
  - `127.0.0.1:80` to make Apache2 listen only on your loopback interface so that it will not be available to the Internet,
  - to e.g. `81` to change the port that it listens on,
  - or leave it as is for normal operation.

### The **ServerName** directive (optional)

Specifies what {term}`FQDN` your site should answer to. The default virtual host has no **ServerName** directive specified, so it will respond to all requests that do not match a ServerName directive in another virtual host. If you have just acquired the domain name `mynewsite.com` and wish to host it on your Ubuntu server, the value of the ServerName directive in your virtual host configuration file should be `mynewsite.com`.

  Add this directive to the new virtual host file you created earlier (`/etc/apache2/sites-available/mynewsite.conf`).

### The **ServerAlias** directive

You may also want your site to respond to `www.mynewsite.com`, since many users will assume the www prefix is appropriate -- use the *ServerAlias* directive for this. You may also use wildcards in the ServerAlias directive.
    
  For example, the following configuration will cause your site to respond to any domain request ending in *.mynewsite.com*.

  ```text
  ServerAlias *.mynewsite.com
  ```

### The **DocumentRoot** directive

Specifies where Apache2 should look for the files that make up the site. The default value is `/var/www/html`, as specified in `/etc/apache2/sites-available/000-default.conf`. If desired, change this value in your site's virtual host file, and remember to create that directory if necessary\!

Enable the new *VirtualHost* using the a2ensite utility and restart Apache2:

```bash
sudo a2ensite mynewsite
sudo systemctl restart apache2.service
```

```{note}
Be sure to replace `mynewsite` with a more descriptive name for the VirtualHost. One method is to name the file after the **ServerName** directive of the VirtualHost.
```

Similarly, use the `a2dissite` utility to disable sites. This is can be useful when troubleshooting configuration problems with multiple virtual hosts:

```bash
sudo a2dissite mynewsite
sudo systemctl restart apache2.service
```

## Apache2 server default settings

This section explains configuration of the Apache2 server default settings. For example, if you add a virtual host, the settings you configure for the virtual host take precedence for that virtual host. For a directive not defined within the virtual host settings, the default value is used.

### The **DirectoryIndex**

 The **DirectoryIndex** is the default page served by the server when a user requests an index of a directory by specifying a forward slash (/) at the end of the directory name.
    
For example, when a user requests the page `http://www.example.com/this_directory/`, they will get either the DirectoryIndex page (if it exists), a server-generated directory list (if it does not and the Indexes option is specified), or a Permission Denied page if neither is true. 

The server will try to find one of the files listed in the DirectoryIndex directive and will return the first one it finds. If it does not find any of these files and if **Options Indexes** is set for that directory, the server will generate and return a list, in HTML format, of the subdirectories and files in the directory. The default value, found in `/etc/apache2/mods-available/dir.conf` is "index.html index.cgi index.pl index.php index.xhtml index.htm". Thus, if Apache2 finds a file in a requested directory matching any of these names, the first will be displayed.

### The **ErrorDocument**

The **ErrorDocument** directive allows you to specify a file for Apache2 to use for specific error events. For example, if a user requests a resource that does not exist, a 404 error will occur.

By default, Apache2 will return a HTTP 404 Return code. Read `/etc/apache2/conf-available/localized-error-pages.conf` for detailed instructions on using ErrorDocument, including locations of example files.

### **CustomLog** and **ErrorLog**

By default, the server writes the transfer log to the file `/var/log/apache2/access.log`. You can change this on a per-site basis in your virtual host configuration files with the **CustomLog** directive, or omit it to accept the default, specified in `/etc/apache2/conf-available/other-vhosts-access-log.conf`.

You can also specify the file to which errors are logged, via the **ErrorLog** directive, whose default is `/var/log/apache2/error.log`. These are kept separate from the transfer logs to aid in troubleshooting problems with your Apache2 server. You may also specify the **LogLevel** (the default value is "warn") and the **LogFormat** (see `/etc/apache2/apache2.conf` for the default value).

### The **Options** directive

Some options are specified on a per-directory basis rather than per-server. **Options** is one of these directives. A Directory stanza is enclosed in XML-like tags, like so:

```text
<Directory /var/www/html/mynewsite>
...
</Directory>
```

The Options directive within a Directory stanza accepts one or more of the following values (among others), separated by spaces:

- **ExecCGI**
  Allow CGI scripts to be run. CGI scripts are not run if this option is not chosen.
        
  ```{caution}
  Most files should not be run as CGI scripts. This would be very dangerous. CGI scripts should kept in a directory separate from and outside your **DocumentRoot**, and only this directory should have the ExecCGI option set. This is the default, and the default location for CGI scripts is `/usr/lib/cgi-bin`.
  ```

- **Includes**
  Allow **server-side includes**. Server-side includes allow an HTML file to *include* other files. See [Apache SSI documentation (Ubuntu community)](https://help.ubuntu.com/community/ServerSideIncludes) for more information.
    
- **IncludesNOEXEC**
  Allow server-side includes, but disable the `#exec` and `#include` commands in CGI scripts.
    
- **Indexes**
  Display a formatted list of the directory's contents, if no DirectoryIndex (such as `index.html`) exists in the requested directory.

  ```{caution}
  For security reasons, this should usually not be set, and certainly should not be set on your DocumentRoot directory. Enable this option carefully on a per-directory basis **only** if you are certain you want users to see the entire contents of the directory.
  ```

- **Multiview**
  Support content-negotiated multiviews; this option is disabled by default for security reasons. See the [Apache2 documentation on this option](https://httpd.apache.org/docs/2.4/mod/mod_negotiation.html#multiviews).
    
- **SymLinksIfOwnerMatch**
  Only follow symbolic links if the target file or directory has the same owner as the link.

### Apache2 daemon settings

This section briefly explains some basic Apache2 daemon configuration settings.

- **LockFile**
  The **LockFile** directive sets the path to the lockfile used when the server is compiled with either `USE_FCNTL_SERIALIZED_ACCEPT` or `USE_FLOCK_SERIALIZED_ACCEPT`. It must be stored on the local disk. It should be left to the default value unless the logs directory is located on an NFS share. If this is the case, the default value should be changed to a location on the local disk and to a directory that is readable only by root.

- **PidFile**
  The **PidFile** directive sets the file in which the server records its process ID (`pid`). This file should only be readable by root. In most cases, it should be left to the default value.

- **User**
  The **User** directive sets the user ID used by the server to answer requests. This setting determines the server's access. Any files inaccessible to this user will also be inaccessible to your website's visitors. The default value for User is "www-data".

  ```{warning}
  Unless you know exactly what you are doing, do not set the User directive to root. Using root as the User will create large security holes for your Web server.
  ```
  
- **Group**
  The **Group** directive is similar to the User directive. Group sets the group under which the server will answer requests. The default group is also "www-data".

## Extending Apache2

Now that you know how to configure Apache2, you may also want to know {ref}`how to extend Apache2 <use-apache2-modules>` with modules.

## Further reading

- The [Apache2 Documentation](https://httpd.apache.org/docs/2.4/) contains in depth information on Apache2 configuration directives. Also, see the `apache2-doc` package for the official Apache2 docs.

- O'Reilly's [Apache Cookbook](https://www.oreilly.com/library/view/apache-cookbook-2nd/9780596529949/) is a good resource for accomplishing specific Apache2 configurations.

- For Ubuntu specific Apache2 questions, ask in the `#ubuntu-server` IRC channel on [libera.chat](https://libera.chat/).
