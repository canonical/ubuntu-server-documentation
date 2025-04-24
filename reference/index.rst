.. _reference:

Ubuntu Server reference
***********************

Our reference section is used for quickly checking what software and commands
are available, and how to interact with various tools.

* Our :ref:`reference-glossary` contains definitions for common terminology
  used in this documentation.

.. toctree::
   :hidden:
   :titlesonly:

   glossary.rst

Server installation
===================

Although Ubuntu Server is flexible and designed to run on a wide range of 
hardware, you can refer to the following requirements page to see the
various architectures Ubuntu Server can be run on, and suggested minimal values
for memory and storage.

.. toctree::
   :titlesonly:

   installation/system-requirements.md

Data and storage
================

This section provides details on storing and backing up your data.

* :ref:`Backups and version control <reference-backups-and-version-control>`

.. toctree::
   :hidden:
   :titlesonly:

   Data and storage <backups.rst>

High Availability
=================

The recommended tool for managing High Availability Pacemaker clusters is now
`pcs`, as of 23.04 (Lunar). Here we provide a reference guide to help you
migrate from `crmsh` to `pcs`.

.. toctree::
   :titlesonly:

   high-availability.rst

Other tools
===========

This section contains suggestions of other useful tools for system
administrators.

.. toctree::
   :titlesonly:

   other-tools.rst


