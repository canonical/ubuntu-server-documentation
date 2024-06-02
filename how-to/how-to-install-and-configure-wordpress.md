(how-to-install-and-configure-wordpress)=
# How to install and configure WordPress

[Wordpress](https://wordpress.com/) is a blog tool, publishing platform and content management system (CMS) implemented in PHP and licensed under the [GNU General Public License (GPL) v2 or later](https://en-gb.wordpress.org/about/license/).

In this guide, we show you how to install and configure WordPress in an Ubuntu system with Apache2 and MySQL.

## Prerequisites

Before installing WordPress you should install Apache2 (or a preferred web server) and a database service such as MySQL.

* To install the Apache package, refer to [our Apache guide](../explanation/introduction-to-web-servers.md).
* To install and configure a MySQL database service, refer to [our MySQL guide](install-and-configure-a-mysql-server.md).

## Install WordPress

To install WordPress, run the following comand in the command prompt:

```bash
sudo apt install wordpress
```

## Configure WordPress

To configure your first WordPress application, you need to configure your Apache web server. To do this, open `/etc/apache2/sites-available/wordpress.conf` and write the following lines:

```text
Alias /blog /usr/share/wordpress
<Directory /usr/share/wordpress>
    Options FollowSymLinks
    AllowOverride Limit Options FileInfo
    DirectoryIndex index.php
    Order allow,deny
    Allow from all
</Directory>
<Directory /usr/share/wordpress/wp-content>
    Options FollowSymLinks
    Order allow,deny
    Allow from all
</Directory>
```

Now you can enable this new WordPress site:

```bash
sudo a2ensite wordpress
```

Once you configure the Apache2 web server (and make it ready for your WordPress application), you will need to restart it. You can run the following command to restart the Apache2 web server:

```bash
sudo systemctl reload apache2.service
```

### The configuration file

To facilitate having multiple WordPress installations, the name of the configuration file is based on the **Host header** of the HTTP request.

This means you can have a configuration per **Virtual Host** by matching the hostname portion of this configuration with your Apache Virtual Host, e.g. `/etc/wordpress/config-10.211.55.50.php`, `/etc/wordpress/config-hostalias1.php`, etc.

These instructions assume you can access Apache via the **localhost** hostname (perhaps by using an SSH tunnel) if not, replace `/etc/wordpress/config-localhost.php` with `/etc/wordpress/config-NAME_OF_YOUR_VIRTUAL_HOST.php`.

Once the configuration file is written, it is up to you to choose a convention for username and password to MySQL for each WordPress database instance. This documentation shows only one, localhost, to act as an example.

### Configure the MySQL database

Now we need to configure WordPress to use a MySQL database. Open the `/etc/wordpress/config-localhost.php` file and write the following lines:

```php
<?php
define('DB_NAME', 'wordpress');
define('DB_USER', 'wordpress');
define('DB_PASSWORD', 'yourpasswordhere');
define('DB_HOST', 'localhost');
define('WP_CONTENT_DIR', '/usr/share/wordpress/wp-content');
?>
```

## Create the MySQL database

Now create the mySQL database you've just configured. Open a temporary file with MySQL command `wordpress.sql` and write the following lines:

```
CREATE DATABASE wordpress;
CREATE USER 'wordpress'@'localhost'
IDENTIFIED BY 'yourpasswordhere';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER
ON wordpress.*
TO wordpress@localhost;
FLUSH PRIVILEGES;
```

Then, run the following commands:

```bash
cat wordpress.sql | sudo mysql --defaults-extra-file=/etc/mysql/debian.cnf
```

Your new WordPress installation can now be configured by visiting `http://localhost/blog/wp-admin/install.php` (or `http://NAME_OF_YOUR_VIRTUAL_HOST/blog/wp-admin/install.php` if your server has no GUI and you are completing WordPress configuration via a web browser running on another computer). Fill out the Site Title, username, password, and E-mail and click "Install WordPress".

Note the generated password (if applicable) and click the login password. Your WordPress is now ready for use!

## Further reading

- [WordPress.org Codex](https://codex.wordpress.org/)

- [Ubuntu Wiki WordPress](https://help.ubuntu.com/community/WordPress)
