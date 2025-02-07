(install-ruby-on-rails)=
# How to install and configure Ruby on Rails

[Ruby on Rails](https://rubyonrails.org/) is an open source web framework for developing database-backed web applications. It is optimised for sustainable productivity of the programmer since it lets the programmer to write code by favouring convention over configuration. This guide explains how to install and configure Ruby on Rails for an Ubuntu system with Apache2 and MySQL.

## Prerequisites

Before installing Rails you should install Apache (or a preferred web server) and a database service such as MySQL.

* To install the Apache package, please refer to {ref}`our Apache guide <install-apache2>`.
* To install and configure a MySQL database service, refer to {ref}`our MySQL guide <install-mysql>`.

## Install `rails`

Once you have a web server and a database service installed and configured, you are ready to install the Ruby on Rails package, `rails`, by entering the following in the terminal prompt.

```bash
sudo apt install rails
```

This will install both the Ruby base packages, and Ruby on Rails.

## Configure the web server

You will need to modify the `/etc/apache2/sites-available/000-default.conf` configuration file to set up your domains.

The first thing to change is the [`DocumentRoot`](https://documentation.ubuntu.com/server/reference/glossary/#term-DocumentRoot) directive:

```text
DocumentRoot /path/to/rails/application/public
```

Next, change the `<Directory "/path/to/rails/application/public">` directive:

```text
<Directory "/path/to/rails/application/public">
        Options Indexes FollowSymLinks MultiViews ExecCGI
        AllowOverride All
        Order allow,deny
        allow from all
        AddHandler cgi-script .cgi
</Directory>
```

You should also enable the `mod_rewrite` module for Apache. To enable the `mod_rewrite` module, enter the following command into a terminal prompt:

```bash
sudo a2enmod rewrite
```

Finally, you will need to change the ownership of the `/path/to/rails/application/public` and `/path/to/rails/application/tmp` directories to the user that will be used to run the Apache process:

```bash
sudo chown -R www-data:www-data /path/to/rails/application/public
sudo chown -R www-data:www-data /path/to/rails/application/tmp
```

If you need to compile your application assets run the following command in
your application directory:

```bash
RAILS_ENV=production rake assets:precompile
```

## Configure the database

With your database service in place, you need to make sure your app database configuration is also correct. For example, if you are using MySQL the your `config/database.yml` should look like this:

```text
# Mysql 
production:
  adapter: mysql2
  username: user
  password: password
  host: 127.0.0.1 
  database: app
```

To finally create your application database and apply its migrations you can run the following commands from your app directory:

```bash
RAILS_ENV=production rake db:create
RAILS_ENV=production rake db:migrate
```

That's it! Now your Server is ready for your Ruby on Rails application. You can [daemonize](https://documentation.ubuntu.com/server/reference/glossary/#term-daemonize) your application as you want.

## Further reading

- See the [Ruby on Rails](http://rubyonrails.org/) website for more information.

- [Agile Development with Rails](https://pragprog.com/book/rails4/agile-web-development-with-rails-4) is also a great resource.
