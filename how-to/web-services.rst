.. _how-to-web-services:

Web services
*************

Web servers are used to serve content over a network (or the Internet). If you
want more of an introduction to the different types of web servers available in
Ubuntu, check out our :ref:`introduction-to-web-servers`.

Proxy servers
=============

This section shows how to set up a Squid proxy caching server.

.. toctree::
   :titlesonly:

   Install a Squid server <web-services/install-a-squid-server>

Web servers
===========

Two of the most popular web servers in Ubuntu are Apache2 and nginx. This
section covers the installation, configuration and extension of both.

Apache2
-------

.. toctree::
   :hidden:

   Install Apache2 <web-services/install-apache2>
   Apache2 settings <web-services/configure-apache2-settings>
   Apache2 modules <web-services/use-apache2-modules>

* :ref:`Install Apache2 <install-apache2>`
* :ref:`Configure Apache2 <configure-apache2-settings>`
* :ref:`Extend Apache2 with modules <use-apache2-modules>`

Nginx
-----

.. toctree::
   :hidden:

   Install nginx <web-services/install-nginx>
   nginx settings <web-services/configure-nginx>
   nginx modules <web-services/use-nginx-modules>

* :ref:`Install nginx <install-nginx>`
* :ref:`Configure nginx <configure-nginx>`
* :ref:`Extend nginx with modules <use-nginx-modules>`

Web programming
===============

It is common to set up server-side scripting languages to support the creation
of dynamic web content. Whichever scripting language you choose, you will need
to have installed and configured your web and database servers beforehand.

.. toctree::
   :titlesonly:

   Install PHP <web-services/install-php>
   Install Ruby on Rails <web-services/install-ruby-on-rails>

See also
========

* Explanation: :ref:`explanation-web-services`
