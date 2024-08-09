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

The following installation guides are more advanced than our getting started
tutorial, but can be applied to specific scenarios. If you are looking for a
more straightforward installation, refer to our
:ref:`basic installation <basic-installation>` tutorial.

.. include:: installation.rst
    :start-line: 4
    :end-before: .. toctree::

**The Server installer**

The Ubuntu installer now has its own documentation for automatic (or
"hands-off" installations). For more guidance on auto-installing Ubuntu with
the installer, refer to these guides from the Ubuntu installer documentation
(note: these pages will redirect you outside of the Server documentation).

* `Introduction to Automated Server installer`_
* `Autoinstall quickstart`_
* `Autoinstall quickstart on s390x`_

Virtualisation
==============

.. include:: virtualisation.rst
    :start-line: 4
    :end-before: .. toctree::

Containers
==========

.. include:: containers.rst
    :start-line: 4
    :end-before: .. toctree::

Networking
==========

.. include:: networking.rst
    :start-line: 4
    :end-before: .. toctree::

Samba
=====

.. include:: samba.rst
    :start-line: 4
    :end-before: .. toctree::

Authentication and access
=========================

Kerberos
--------

.. include:: kerberos.rst
    :start-line: 4
    :end-before: .. toctree::

Network user authentication with SSSD
-------------------------------------

.. include:: sssd.rst
    :start-line: 4
    :end-before: .. toctree::

OpenLDAP
--------

.. include:: openldap.rst
    :start-line: 4
    :end-before: .. toctree::

Active Directory integration
----------------------------

.. include:: active-directory.rst
    :start-line: 4
    :end-before: .. toctree::
    
Databases
=========

.. include:: databases.rst
    :start-line: 4
    :end-before: .. toctree::

Mail services
=============

.. include:: mail-services.rst
    :start-line: 4
    :end-before: .. toctree::

Backups and version control
===========================

.. include:: backups.rst
    :start-line: 4
    :end-before: .. toctree::

Web services
============

.. include:: web-services.rst
    :start-line: 4
    :end-before: .. toctree::

Storage
=======

.. include:: storage.rst
    :start-line: 4
    :end-before: .. toctree::

Graphics
========

.. include:: graphics.rst
    :start-line: 4
    :end-before: .. toctree::

Managing software
=================

.. include:: software.rst
    :start-line: 4
    :end-before: .. toctree::

Security
========

.. include:: security.rst
    :start-line: 4
    :end-before: .. toctree::

WireGuard VPN
=============

.. include:: wireguard-vpn.rst
    :start-line: 4
    :end-before: .. toctree::

High Availability
=================

.. include:: high-availability.rst
    :start-line: 4
    :end-before: .. toctree::

Observability
=============

.. include:: observability.rst
    :start-line: 4
    :end-before: .. toctree::

.. LINKS
.. _Introduction to Automated Server installer: https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html
.. _Autoinstall quickstart: https://canonical-subiquity.readthedocs-hosted.com/en/latest/howto/autoinstall-quickstart.html
.. _Autoinstall quickstart on s390x: https://canonical-subiquity.readthedocs-hosted.com/en/latest/howto/autoinstall-quickstart-s390x.html

.. toctree::
    :hidden:
    :titlesonly:

    installation.rst
    virtualisation.rst
    containers.rst
    networking.rst
    samba.rst
    active-directory.rst
    kerberos.rst
    sssd.rst
    openldap.rst
    databases.rst
    mail-services.rst
    backups.rst
    web-services.rst
    storage.rst
    graphics.rst
    software.rst
    security.rst
    wireguard-vpn.rst
    high-availability.rst
    observability.rst
