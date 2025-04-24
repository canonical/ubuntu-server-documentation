.. _how-to:

Ubuntu Server how-to guides
***************************

If you have a specific goal, but are already familiar with Ubuntu Server, our
how-to guides have more in-depth detail than our tutorials and can be applied
to a broader set of applications. They’ll help you achieve an end result but
may require you to understand and adapt the steps to fit your specific
requirements.

Server installation
===================

.. toctree::
    :hidden:
    :titlesonly:

    installation.rst

Our list of :ref:`installation guides <how-to-server-installation>` contains
installation instructions for a variety of architecture-specific and advanced
setups. For a general installation, or if you're just getting started with
Ubuntu, you may prefer to use our :ref:`basic installation <basic-installation>`
tutorial.

Security
========

.. toctree::
    :hidden:
    :titlesonly:

    security.rst

:ref:`System security <how-to-security>` is a crucial topic for any Ubuntu user.
In addition to general security topics such as setting up a firewall, AppArmor
profiles and user/group management, you will also find how-to guides on:

* **Authentication** with Kerberos, network user authentication with SSSD and
  physical authentication with smart cards
* **Cryptography** with OpenSSH
* **Virtual Private Networks** OpenVPN and WireGuard VPN

Networking
==========

.. toctree::
   :hidden:
   :titlesonly:

   networking.rst

:ref:`Our networking section <how-to-networking>` is where you will find how-to
guides on a broad range of networking topics, such as:

* **Network tooling and configuration** including time synchronisation, DHCP
  for IP address assignment, Domain Name Service (DNS) (and more!)
* **Network shares** for sharing resources (files, services, directories)
  across networks, including integration with Windows

Managing software
=================

.. toctree::
   :hidden:
   :titlesonly:

   software.rst

:ref:`Managing software <how-to-managing-software>` provides guides on topics
including:

* **Software updates** and configuration
* **Upgrading your Ubuntu release**
* **Bug reporting**

Data and storage
================

.. toctree::
   :hidden:
   :titlesonly:

   data-and-storage.rst

:ref:`The data and storage section <how-to-data-and-storage>` covers the
following:

* **Managing data** in the OpenLDAP and databases topics
* **Storage and backups**, including partitioning (with LVM), backup utilities,
  and version control

Mail services
=============

Our :ref:`how-to-mail-services` section shows you how to set up:

* **Mail User Agents** (Thunderbird)
* **Mail Transfer Agents** (Postfix and Exim4)
* **Mail Delivery Agents** (Dovecot)

.. toctree::
   :hidden:
   :titlesonly:

   mail-services.rst

Web services
============

Our :ref:`Web services section <how-to-web-services>` shows how to set up the
different components of web servers, including:

* **Apache2** and **nginx**
* **Squid proxy servers**
* **Web programming** (PHP and Ruby)

.. toctree::
   :hidden:
   :titlesonly:

   web-services.rst

Graphics
========

The :ref:`how-to-graphics` section contains guides on how to set up both
on-system and virtual GPU.

.. toctree::
   :hidden:
   :titlesonly:

   graphics.rst

Virtualisation
==============

Our :ref:`Virtualisation <how-to-virtualisation>` section contains installation
and usage guides for common virtualization tools available in Ubuntu, across
various layers of abstraction, from Multipass to QEMU.

.. toctree::
   :hidden:
   :titlesonly:

   virtualisation.rst

Containers
==========

Our :ref:`Containers <how-to-containers>` section includes installation and
usage guides for the most popular container tooling available in Ubuntu:

* **LXD**, which can also now be used to create virtual machines
* **Docker** and **rocks**

.. toctree::
   :hidden:
   :titlesonly:

   containers.rst

High Availability
=================

:ref:`High Availability <how-to-high-availability>` is a method for clustering
resources to ensure minimal downtime if a particular component fails. This
section shows how to set up various components of a High Availability setup.

.. toctree::
   :hidden:
   :titlesonly:

   high-availability.rst

Observability
=============

:ref:`Observability <how-to-observability>` is a name given to the collection
of tools used to monitor your infrastructure. In Ubuntu, you can use the classic
Logging, Monitoring, and Alerting (LMA) stack, or the newer
`Canonical Observability Stack <https://charmhub.io/topics/canonical-observability-stack>`_.

This section focuses on the classic LMA stack.

.. toctree::
   :hidden:
   :titlesonly:

   observability.rst

