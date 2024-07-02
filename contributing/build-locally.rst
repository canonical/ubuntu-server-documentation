.. _build-locally:

Build the documentation locally
*******************************

We use the "fork and pull" method, which means that you should create your own
fork of the repository. If you're not sure what this means or need some help
getting started, check out the `working with git`_ guide from the Open
Documentation Academy which will walk you through the process. Just remember
to change all instances of ``open-documentation-academy`` to
``ubuntu-server-documentation``!

If you're already familiar with the process, then use the steps below to clone
the repository and build the documentation. Don't forget to set up your own
fork!

Fetch the docs
==============

Before you can start working on an issue, first you will need to download the
documentation. To do this, you can run:

.. code-block:: bash

   git clone git@github.com:canonical/ubuntu-server-documentation.git

This will create a new folder on your machine called
"ubuntu-server-documentation", containing the contents of this repository.

You can then navigate to this folder using:

.. code-block:: bash

   cd ubuntu-server-documentation

Install required software
=========================

Before you start, make sure you have ``make``, ``python3``, ``python3-venv``,
and ``python3-pip`` installed on your system:

.. code-block:: bash

   sudo apt update
   sudo apt install make python3 python3-venv python3-pip
   make install

The first time you run this command it will install all the dependencies
required to build the documentation. 

When working on documentation
=============================

If you are actively working on a change to the documentation, we recommend you
use the command:

.. code-block:: bash

   make run

This will build **and serve** the documentation at
`http://127.0.0.1:8000/ <http://127.0.0.1:8000/>`_.
It will watch the folder, and whenever you save changes to a file, this URL
will give you a live preview of your changes (or warn you if something has gone
horribly wrong!).

.. note::
   If you have problems getting the documentation to run on your machine,
   reach out to the team or leave a comment on your issue to get additional
   support.

Create a new branch
-------------------

For any set of changes you want to make, you should create a branch on your own
fork of the repository. 

.. code-block:: bash

   git pull
   git checkout -b my-new-branch

Whenever you are on the main branch and want to create a new branch, it's a
good idea to run ``git pull`` first, so that any recent changes are sync'ed
to your machine.

Writing guidance
----------------

Once your environment is set up and you have been able to get your local copy
running without any build errors, you can check out our
:ref:`guidance for writing <writing-guidance>` section to find out about our
style guide and other important information.

Submit your changes
-------------------

Once you have made your changes and are happy with them, you can
:ref:`find out how to submit them <submit-work>`.

.. _Diátaxis: https://diataxis.fr/
.. _working with git: https://github.com/canonical/open-documentation-academy/blob/main/getting-started/using_git.md
