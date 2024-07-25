(introduction-to-web-servers)=
# Introduction to web servers

Web servers are used to serve web pages requested by client computers. Clients typically request and view web pages using web browser applications such as Firefox, Opera, Chromium, or Internet Explorer.

If you're new to web servers, see this page for more information [on the key concepts](about-web-servers.md).

## Squid proxy server

Squid is a popular, open-source, proxy caching server that can help optimise network efficiency and improve response times by saving local copies of frequently accessed content. Read more [about Squid proxy servers](about-squid-proxy-servers.md) and what they can do, or find out [how to install a Squid server](../how-to/how-to-install-a-squid-server.md).

### Web server

Apache is the most commonly used web server on Linux systems, and the current version is Apache2. It is robust, reliable, and highly configurable. This set of guides will show you:

- [How to install and configure Apache2](../how-to/how-to-install-apache2.md)
- [How to configure Apache2 for your needs](../how-to/how-to-configure-apache2-settings.md)
- [How to extend Apache2's functionality with modules](../how-to/how-to-use-apache2-modules.md)

Nginx is a popular alternative web server also widely used on Linux, with a focus on static file serving performance, ease of configuration, and use as both a web server and reverse proxy server.

- [How to install Nginx](../how-to.rst)
- [How to configure Nginx](../how-to/how-to-configure-nginx.md)
- [How to use Nginx modules](../how-to/how-to-use-nginx-modules.md)

### Database server

The database server, when included in the LAMP stack, allows data for web applications to be stored and managed. MySQL is one of the most popular open source Relational Database Management Systems (RDBMS) available, and you can find out in this guide [how to install MySQL](../how-to/install-and-configure-a-mysql-server.md) -- or [PostgreSQL](../how-to/install-and-configure-postgresql.md), as another popular alternative.

### Scripting languages

Server-side scripting languages allow for the creation of dynamic web content, processing of web forms, and interacting with databases (amongst other crucial tasks). PHP is most often used, and we can show you [how to install PHP](../how-to/how-to-install-and-configure-php.md), or if you prefer, we can show you [how to install Ruby on Rails](../how-to/how-to-install-and-configure-ruby-on-rails.md).

Whichever scripting language you choose, you will need to have installed and configured your web and database servers beforehand.
