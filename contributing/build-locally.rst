.. _build-locally:

How to build the documentation locally
**************************************

First, you will need to download the documentation. To do this, you can run:

.. code-block::

   git clone git@github.com:canonical/ubuntu-server-documentation.git

This will create a new folder on your machine called
"ubuntu-server-documentation", containing the contents of this repository.

You can then navigate to this folder: ``cd ubuntu-server-documentation``

Install required software
=========================

Before you start, make sure you have ``make``, ``python3``, ``python3-venv``,
and ``python3-pip`` installed on your system:

.. code-block::

   sudo apt update
   sudo apt install make python3 python3-venv python3-pip
   make install



The first time you run this command it will install all the dependencies
required to build the documentation. The ``html`` option will generate the
HTML pages inside the ``_build`` folder. Use your web browser to open
``index.html`` to preview the site.

When working on documentation
=============================

If you are actively working on a change to the documentation, we recommend you
use the command:

.. code-block:: bash

   make run

This will build **and serve** the documentation at http://127.0.0.1:8000/ --
this will rebuild the documentation whenever you make and save changes to a
file, giving you a live preview of your documentation.
