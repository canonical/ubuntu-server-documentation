.. _how-to-backups-and-version-control:

Backups and version control
****************************

On Ubuntu, two primary ways of backing up your system are **backup utilities**
and **shell scripts**. For additional protection, you can combine backup
methods.

Backup utilities
================

* :ref:`Bacula <install-bacula>` has advanced features and customization support,
  which makes it a good choice for enterprise systems or complex setups.
* :ref:`rsnapshot <install-rsnapshot>` is a simple and efficient solution, well
  suited to individual users or small-scale organizations. 

.. toctree::
   :hidden:

   Install Bacula <backups/install-bacula>
   Install rsnapshot <backups/install-rsnapshot>

Shell scripts
=============

If you are looking for full flexibility and customization, another option is
to use shell scripts.

.. toctree::
   :titlesonly:

   Backup with shell scripts <backups/back-up-using-shell-scripts>

Version control
===============

* :ref:`install-etckeeper` stores the contents of ``/etc`` in a Version Control
  System (VCS) repository
* :ref:`Install gitolite <install-gitolite>` for a traditional source control
  management server for git, including multiple users and access rights
  management

.. toctree::
   :hidden:

   etckeeper <backups/install-etckeeper>
   Install gitolite <backups/install-gitolite>

See also
========

* Explanation: :ref:`introduction-to-backups`
