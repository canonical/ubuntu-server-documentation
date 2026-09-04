---
myst:
  html_meta:
    description: Set up Ruby on Rails web framework on Ubuntu with Apache2 and MySQL for database-backed application development.
---

(install-ruby-on-rails)=
# How to install and configure Ruby on Rails

[Ruby on Rails](https://rubyonrails.org/) is an open source web framework for developing database-backed web applications. It is optimized for sustainable productivity of the programmer since it lets the programmer to write code by favoring convention over configuration. This guide explains how to install and configure Ruby on Rails for an Ubuntu system with Apache2 and MySQL.

## Prerequisites

Before installing Rails you should install Apache (or a preferred web server) and a database service such as MySQL.

* To install the Apache package, please refer to {ref}`our Apache guide <install-apache2>`.
* To install and configure a MySQL database service, refer to {ref}`our MySQL guide <install-mysql>`.

## Install `rails`

Once you have a web server and a database service installed and configured, you are ready to install the Ruby on Rails package, `rails`, by entering the following in the terminal prompt.

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install rails ruby-dev build-essential
```

This will install both the Ruby base packages, and Ruby on Rails. `ruby-dev` and `build-essential` are required because a Rails application resolves its own dependencies with {manpage}`bundler(1)`, and several of those gems build C extensions during installation. Without the compiler and the Ruby development headers, `bundle install` can't handle those extensions.

Alternatively, you may want to install it with the `--no-install-recommends` flag to skip pulling in browser related dependencies, which may require additional steps in certain containerized environments.

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install --no-install-recommends rails ruby-dev build-essential
```

If your application uses MySQL, install the client development headers as well, so that Bundler can build the `mysql2` gem:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install libmysqlclient-dev
```

## Create a new application (optional)

If you don't have an application yet, generate one to follow the rest of this guide. Run the generator as a regular user (not `root`) from the directory where you want the application to live:

```{terminal}
:copy:
:user:
:host:
:dir:
rails new blog --database=mysql --skip-bundle
```

Then install the application dependencies. A per-application gem path keeps the gems inside the project directory, so `bundle install` does not need write access to the system gem directory, and you do not need to run it with `sudo`:

```{terminal}
:copy:
:user:
:host:
:dir:
cd blog
bundle config set --local path vendor/bundle
bundle install
```

The application is now in the `blog` directory. Use its absolute path wherever the sections below refer to `/path/to/rails/application`.

## Configure the web server

You will need to modify the `/etc/apache2/sites-available/000-default.conf` configuration file to set up your domains.

The first thing to change is the {term}`DocumentRoot` directive:

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

```{terminal}
:copy:
:user:
:host:
:dir:
sudo a2enmod rewrite
```

Finally, you will need to change the ownership of the `/path/to/rails/application/public` and `/path/to/rails/application/tmp` directories to the user that will be used to run the Apache process:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo chown -R www-data:www-data /path/to/rails/application/public
```
```{terminal}
:copy:
:user:
:host:
:dir:
sudo chown -R www-data:www-data /path/to/rails/application/tmp
```

If you need to compile your application assets run the following command in
your application directory:

```{terminal}
:copy:
:user:
:host:
:dir:
RAILS_ENV=production bundle exec rake assets:precompile
```

## Configure the database

With your database service in place, you need to make sure your app database configuration is also correct. For example, if you are using MySQL, replace the `production` block of your `config/database.yml` so that it looks like this:

```yaml
# Mysql
production:
  adapter: mysql2
  username: user
  password: password
  host: 127.0.0.1
  database: app
```

The database user (`user` in this example) must already exist in MySQL and have permission to create the database. Refer to {ref}`our MySQL guide <install-mysql>` to create one.

To finally create your application database and apply its migrations you can run the following commands from your app directory:

```{terminal}
:copy:
:user:
:host:
:dir:
RAILS_ENV=production bundle exec rake db:create
RAILS_ENV=production bundle exec rake db:migrate
```

That's it! Now your Server is ready for your Ruby on Rails application. You can {term}`daemonize` your application as you want.

## Further reading

- See the [Ruby on Rails](https://rubyonrails.org/) website for more information.

- [Agile Development with Rails](https://pragprog.com/titles/rails7/agile-web-development-with-rails-7/) is also a great resource.
