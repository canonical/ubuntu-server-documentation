(how-to-install-and-configure-php)=
# How to install and configure PHP

[PHP](https://www.php.net/) is a general-purpose scripting language well-suited for Web development since PHP scripts can be embedded into HTML. This guide explains how to install and configure PHP in an Ubuntu System with Apache2 and MySQL.

## Prerequisites

Before installing PHP you should install Apache (or a preferred web server) and a database service such as MySQL.

* To install the Apache package, please refer to [our Apache guide](../explanation/introduction-to-web-servers.md).
* To install and configure a MySQL database service, refer to [our MySQL guide](install-and-configure-a-mysql-server.md).

## Install PHP

PHP is available on Ubuntu Linux, but unlike Python (which comes pre-installed), must be manually installed.

To install PHP -- and the Apache PHP module -- you can enter the following command into a terminal prompt:

```bash
sudo apt install php libapache2-mod-php
```

## Install optional packages

The following packages are optional, and can be installed if you need them for your setup. 

* **PHP-CLI**
  You can run PHP scripts via the Command Line Interface (CLI). To do this, you must first install the `php-cli` package. You can install it by running the following command:

  ```bash
  sudo apt install php-cli
  ```

* **PHP-CGI**
  You can also execute PHP scripts without installing the Apache PHP module. To accomplish this, you should install the `php-cgi` package via this command:

  ```bash
  sudo apt install php-cgi
  ```

* **PHP-MySQL**
  To use MySQL with PHP you should install the `php-mysql` package, like so:

  ```bash
  sudo apt install php-mysql
  ```

* **PHP-PgSQL**
  Similarly, to use PostgreSQL with PHP you should install the `php-pgsql` package:

  ```bash
  sudo apt install php-pgsql
  ```

## Configure PHP

If you have installed the `libapache2-mod-php` or `php-cgi` packages, you can run PHP scripts from your web browser. If you have installed the `php-cli` package, you can run PHP scripts at a terminal prompt.

By default, when `libapache2-mod-php` is installed, the Apache2 web server is configured to run PHP scripts using this module. First, verify if the files `/etc/apache2/mods-enabled/php8.*.conf` and `/etc/apache2/mods-enabled/php8.*.load` exist. If they do not exist, you can enable the module using the `a2enmod` command.

Once you have installed the PHP-related packages and enabled the Apache PHP module, you should restart the Apache2 web server to run PHP scripts, by running the following command:

```bash
sudo systemctl restart apache2.service 
```

## Test your setup

To verify your installation, you can run the following PHP `phpinfo` script:

```php
<?php
  phpinfo();
?>
```

You can save the content in a file -- `phpinfo.php` for example -- and place it under the `DocumentRoot` directory of the Apache2 web server. Pointing your browser to `http://hostname/phpinfo.php` will display the values of various PHP configuration parameters.

## Further reading

- For more in depth information see [the php.net documentation](http://www.php.net/docs.php).

- There are a plethora of books on PHP 7 and PHP 8. A good book from O'Reilly is "Learning PHP", which includes an exploration of PHP 7's enhancements to the language.

- Also, see the [Apache MySQL PHP Ubuntu Wiki](https://help.ubuntu.com/community/ApacheMySQLPHP) page for more information.
