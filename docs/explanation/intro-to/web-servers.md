(introduction-to-web-servers)=
# Introduction to web servers

Web servers are used to serve web pages requested by client computers. Clients typically request and view web pages using web browser applications such as Firefox, Opera, Chromium, or Internet Explorer.

If you're new to web servers, see this page for more information {ref}`on the key concepts <about-web-servers>`.

## Squid proxy server

Squid is a popular, open-source, proxy caching server that can help optimize network efficiency and improve response times by saving local copies of frequently accessed content. Read more {ref}`about Squid proxy servers <about-squid-proxy-servers>` and what they can do, or find out {ref}`how to install a Squid server <install-a-squid-server>`.

### Web server

Apache is the most commonly used web server on Linux systems, and the current version is Apache2. It is robust, reliable, and highly configurable. This set of guides will show you:

- {ref}`How to install and configure Apache2 <install-apache2>`
- {ref}`How to configure Apache2 for your needs <configure-apache2-settings>`
- {ref}`How to extend Apache2's functionality with modules <use-apache2-modules>`

Nginx is a popular alternative web server also widely used on Linux, with a focus on static file serving performance, ease of configuration, and use as both a web server and reverse proxy server.

- {ref}`How to install Nginx <install-nginx>`
- {ref}`How to configure Nginx <configure-nginx>`
- {ref}`How to use Nginx modules <use-nginx-modules>`

### Database server

The database server, when included in the LAMP stack, allows data for web applications to be stored and managed. MySQL is one of the most popular open source Relational Database Management Systems (RDBMS) available, and you can find out in this guide {ref}`how to install MySQL <install-mysql>` -- or {ref}`PostgreSQL <install-postgresql>`, as another popular alternative.

### Scripting languages

Server-side scripting languages allow for the creation of dynamic web content, processing of web forms, and interacting with databases (amongst other crucial tasks). PHP is most often used, and we can show you {ref}`how to install PHP <install-php>`, or if you prefer, we can show you {ref}`how to install Ruby on Rails <install-ruby-on-rails>`.

Whichever scripting language you choose, you will need to have installed and configured your web and database servers beforehand.
