(how-to-install-and-configure-phpmyadmin-legacy)=
# How to install and configure phpMyAdmin (legacy)

> **Note**:
> This section is flagged as *legacy* because today there are numerous MySQL administrative tools and Ubuntu Server no longer promotes one tool over others.

[phpMyAdmin](https://www.phpmyadmin.net/) is a LAMP application specifically written for administering MySQL servers. Written in PHP, and accessed through a web browser, phpMyAdmin provides a graphical interface for database administration tasks.

## Prerequisites

Before you can install phpMyAdmin, you will need access to a MySQL database -- either on the same host as phpMyAdmin will be installed on, or on a host accessible over the network. For instructions on how to install a MySQL database service, see [our MySQL guide](install-and-configure-a-mysql-server.md).

You will also need a web server. In this guide we use Apache2, although you can use another if you prefer. If you would like instructions on how to install Apache2, see [our Apache guide](../explanation/introduction-to-web-servers.md).

## Install `phpmyadmin`

Once your MySQL database is set up, you can install `phpmyadmin` via the terminal:

```bash
sudo apt install phpmyadmin
```

At the prompt, choose which web server to configure for phpMyAdmin. Here, we are using Apache2 for the web server.

In a browser, go to `http://servername/phpmyadmin` (replace `servername` with the server's actual hostname). 

At the login, page enter **root** for the username. Or, if you have a MySQL user already set up, enter the MySQL user's password.

Once logged in, you can reset the root password if needed, create users, create or destroy databases and tables, etc.

## Configure `phpmyadmin`

The configuration files for phpMyAdmin are located in `/etc/phpmyadmin`. The main configuration file is `/etc/phpmyadmin/config.inc.php`. This file contains configuration options that apply globally to phpMyAdmin.

To use phpMyAdmin to administer a MySQL database hosted on another server, adjust the following in `/etc/phpmyadmin/config.inc.php`:

```
$cfg['Servers'][$i]['host'] = 'db_server';
```

> **Note**:
> Replace `db_server` with the actual remote database server name or IP address. Also, be sure that the phpMyAdmin host has permissions to access the remote database.

Once configured, log out of phpMyAdmin then back in again, and you should be accessing the new server.

### Configuration files

The `config.header.inc.php` and `config.footer.inc.php` files in the `/etc/phpmyadmin` directory are used to add a HTML header and footer, respectively, to phpMyAdmin.

Another important configuration file is `/etc/phpmyadmin/apache.conf`. This file is symlinked to `/etc/apache2/conf-available/phpmyadmin.conf`, and once enabled, is used to configure Apache2 to serve the phpMyAdmin site. The file contains directives for loading PHP, directory permissions, etc. From a terminal type:

```bash
sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
sudo a2enconf phpmyadmin.conf
sudo systemctl reload apache2.service
```

## Further reading

- The phpMyAdmin documentation comes installed with the package and can be accessed from the **phpMyAdmin Documentation** link (a question mark with a box around it) under the phpMyAdmin logo. The official docs can also be access on [the phpMyAdmin website](http://www.phpmyadmin.net/home_page/docs.php).

- Another resource is the [phpMyAdmin Ubuntu Wiki](https://help.ubuntu.com/community/phpMyAdmin) page.

- If you need more information on configuring Apache2, refer to [our guide on Apache2](https://discourse.ubuntu.com/t/web-servers-apache/11510).
