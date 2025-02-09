.. _build-locally:

Build the documentation locally
*******************************

To contribute to the Ubuntu Server documentation you will first need to create
your own fork of the repository, then clone that fork to your machine. If
you're not sure what this means or need some help getting started, check out
the `working with git`_ guide from the Open Documentation Academy which will
walk you through the process and explain this terminology. Just remember to
change all instances of ``open-documentation-academy`` in the commands to
``ubuntu-server-documentation``!

If you're already familiar with the process, then use the steps below to clone
the repository and build the documentation. Don't forget to set up your own
fork!

Get the docs
============

Before you can start working on an issue, first you will need to download the
documentation. To do this, you can run:

.. code-block:: bash

   git clone git@github.com:canonical/ubuntu-server-documentation.git

This will create a new folder on your machine called
``ubuntu-server-documentation`` that contains the contents of this repository.

You can then navigate to this folder using:

.. code-block:: bash

   cd ubuntu-server-documentation

Install required software
=========================

To build the documentation, you will first need to install some necessary
dependencies on your system with the following commands:

.. code-block:: bash

   sudo apt update
   sudo apt install make python3 python3-venv python3-pip
   make install

Create a new branch
===================

Before making any changes, ensure the ``main`` branch on your machine is
up-to-date with any recent changes made to the remote repository:

.. code-block:: bash

   git pull

Now, create a branch and switch to it with the following:

.. code-block:: bash

   git checkout -b my-new-branch

Remember to give your branch a more descriptive name than ``my-new-branch``.
In this way, even if you are working on multiple branches, you will know at a
glance what each of them is for.

Work on the docs
================

You're now ready to start working on the docs! You should run the following
command before you start, to build a live preview:

.. code-block:: bash

   make run

This will build **and serve** the documentation at
`http://127.0.0.1:8000/ <http://127.0.0.1:8000/>`_.
It will watch the folder, and whenever you save changes to a file, this URL
will give update the preview to show your changes (or warn you if something has
gone horribly wrong!).

If you are building locally on an Ubuntu Cloud VM or a container, you may experience issues accessing the page from a browser. To 
resolve this, include `--host 0.0.0.0` in the `sp-run` section of the `Makefile.sp` file.

.. code-block:: sp

   sp-run: sp-install
	. $(VENV); sphinx-autobuild -b dirhtml "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) --host 0.0.0.0

.. note::
   If you have problems getting the documentation to run on your machine,
   reach out to the team or leave a comment on your issue to get additional
   support.
   
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
