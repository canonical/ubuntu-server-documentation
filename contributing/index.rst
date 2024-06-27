.. _contribute:

Contribute to this documentation
********************************

Contributing to documentation can be a fantastic way to get started as a
contributor to open source projects, no matter your level of experience!

The Ubuntu Server Guide is a collaborative effort between Canonical and the
Ubuntu community, and ALL types of contributions are welcome; whether you're
new to Ubuntu Server and want to highlight something you found confusing, or
you're an expert and want to create guides to help others.

We hope to make it as easy as possible to contribute. If you find any part of
our process doesn't work well for you, please let us know!

The Open Documentation Academy
==============================

Ubuntu Server is a proud member of the Canonical
`Open Documentation Academy`_ (ODA). If you are a newcomer to making open
source contributions, or new to technical writing and want to boost your
skills -- or both! -- we will be glad to offer the help and support you need.

Check out the ODA repository for guidance and useful resources on getting
started.

Prerequisites
=============

There are some prerequisites to contributing to Ubuntu Server documentation.

- **Code of Conduct**
  You need to read, and agree to, the Ubuntu `Code of Conduct`_. By
  participating, you implicitly agree to abide by the Code of Conduct. 

- **GitHub account**
  You need a `GitHub account`_ to create issues, comment, reply, or submit
  contributions.

  You don't need to know ``git`` before you start, and you definitely don't
  need to work on the command line if you don't want to. Many documentation
  tasks can be done using `GitHub's web interface`_. On the command line, we
  use the standard "fork and pull" process.

- **Licensing**
  The first time you contribute to a Canonical project, you will need to sign
  the Canonical License agreement (CLA). If you have already signed it, e.g.
  when contributing to another Canonical project, you do not need to sign it
  again.
  
  This license protects your copyright over your contributions, including the
  right to use them elsewhere, but grants us (Canonical) permission to use
  them in our project. You can read `more about the CLA`_ before you
  `sign the CLA`_.

The Ubuntu Server docs overview
===============================

This documentation is `hosted in GitHub`_ and rendered on Read the Docs. You
need to create a `GitHub account`_ to participate, but you do not need a Read
the Docs account.

Contribution types
==================

There are many different ways to contribute to the Ubuntu Server documentation,
including options that don't require any coding knowledge. To find out more,
check out the :ref:`contrib-types` page.








1) :ref:`Find an issue to work on <finding-issues>`

General workflow
----------------


Files and structure
===================

The structural elements, such as landing pages, are written in reStructuredText
(``.rst`` file types).

The documentation pages themselves are written in standard Markdown (``.md``
file types) with MyST support for more advanced elements if you want it.



Graphics
========

You can use Mermaid to create diagrams and flow charts if you wish. Mermaid
has an `online generator`_ tool to help you become familiar with the syntax.



Workshops and getting help
==========================

Each issue should contain a description of the task to be completed, and some
suggestions for how you might want to tackle it if there are several options.


For questions specific to each task, add a comment on the issue you’ve been assigned:

https://github.com/canonical/open-documentation-academy/issues 117

If you’ve not been able to work on the task for a while, please also leave a comment to let us know. This helps us know you intend to complete a task, and to keep our task list status up-to-date.

For more general questions, we recommend creating a post on our forum here, but you’re also welcome to ask on our Matrix group:

https://matrix.to/#/#documentation:ubuntu.com 12

Submitting your work
====================

Submissions should be through the Open Documentation Academy GitHub repository. We will provide help and documentation to do this, but an overview of the process is as follows:

    Fork the Open Documentation Academy GitHub repository 15 to your own GitHub account. https://github.com/canonical/open-documentation-academy
    Write or edit the document for your issue. See the issue details for how this needs to be formatted and structured.
    Add then commit your work file or files to your repository.
    Create a Pull Request https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request in your repository against our Open Documentation Academy repository. Link your pull request to your issue https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue 2, typically be adding fixes #<issue-number to your description.

The Open Documentation Academy team will be in touch to review your work. This is where the collaboration begins!

See Resources https://discourse.ubuntu.com/t/resources/42770/ for our communication channels, and for further reading.

Testing your changes
====================

Reviews
=======

Get some guidance
=================

.. toctree::
   :maxdepth: 1
   
   self
   gh-issues.rst
   contrib-types.rst
   writing-guidance


.. _Code of Conduct: https://ubuntu.com/community/ethos/code-of-conduct
.. _GitHub account: https://github.com/
.. _hosted in GitHub: https://github.com/canonical/ubuntu-server-documentation
.. _GitHub's web interface: https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
.. _online generator: https://mermaid.live/
.. _Open Documentation Academy: https://github.com/canonical/open-documentation-academy
.. _use this link: https://github.com/canonical/ubuntu-server-documentation/issues?q=is%3Aissue+is%3Aopen+no%3Aassignee
.. _more about the CLA: https://ubuntu.com/legal/contributors
.. _sign the CLA: https://ubuntu.com/legal/contributors/agreement
.. _the issues list: https://github.com/canonical/ubuntu-server-documentation/issues
