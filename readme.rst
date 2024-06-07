:orphan:

Discourse PDF/versioning
########################

This content provides the means to download documentation from Discourse and 
convert it to Sphinx, so that it can be built in ReadTheDocs, which in turn 
provides a PDF/epub mechanism. 

If your documentation has branches for different versions, it will allow you 
to provide versioned documentation via a PDF or ePub, even if you are using 
Discourse to provide your documentation. 

No API keys are required, since everything is pulled in from the public/raw 
markdown.

It assumes that your documentation pages are in standard markdown. 

The scaffolding required by Sphinx/RTD is created automatically by the same
script that downloads the markdown content. 


Clone the repo
==============

.. code-block::

    git clone git@github.com:s-makin/discourse-offline-helper <your-new-repository-name>
    cd <your-new-repository-name>


In this repo...
================

All of the contents of the root directory are related to the starter pack,
with the exception of the ``index.rst`` file and the ``docs/`` folder. 

The Documentation starter pack includes:

* a bundled Sphinx_ theme, configuration, and extensions
* support for both reStructuredText (reST) and Markdown
* build checks for links, spelling, and inclusive language
* customisation support layered above a core configuration

The bits you will be interested in is:

In the root dir:
- ``index.rst`` file
- ``custom_conf.py``: this is where you can set URLs and other info for your project, which controls how it's shown on the rendered docs. See the `starter pack readme <https://github.com/canonical/sphinx-docs-starter-pack/blob/main/readme.rst>`_ for further instructions.

In the ``docs`` dir:

- ``extract-files.py``: Creates the ``file-list.csv`` file needed to download all the docs. It is not present in the repo by default as you need to generate the one for your own docs.
- ``download-docs.py``: Downloads all your Discourse docs and creates the rst scaffolding Sphinx needs.
- Four plain text files for correctly inserting the relevant intro text on your Diataxis landing pages.


Set up your static bits
=======================

Index page
----------

You will want to convert the contents of the current markdown index page into
restructuredtext, since this is what Sphinx prefers. This page is largely
static and unlikely to change much, so use the current index page as an example
and drop in the appropriate text for your product.

Landing page text
-----------------

The landing page text is also unlikely to change much, if ever, once it's been
set. Replace the text in the following files to match your Diataxis landing
page content (as it exists in Discourse):

- intro_tutorial.txt
- intro_how-to.txt
- intro_explanation.txt
- intro_reference.txt


Get a file-list.csv file
========================

You can either create this manually, or have the ``docs/extract-files.py``
script generate it from the index page navigation table from Discourse. 

To use this script, you will need to know the Discourse post number of the
page (e.g. the Server index is ``11322``) and you'll need to specify the name
of the project (e.g. ``"Ubuntu Server Documentation"`` - with the quotation marks). You can call the script
by navigating to the ``docs/`` folder and running it as follows:

.. code-block::

    cd docs
    python3 extract-files.py <index number> <Project name>

In my example:

.. code-block::

    cd docs
    python3 extract-files.py 11322 "Ubuntu Server Documentation"

If you want to create it manually from a spreadsheet you're already using to
track your Discourse docs, you should fill in the columns in this order:

* slug (from the post header)
* Page name (will be used to insert the H1 header on the page)
* Discourse post number
* page type ("landing page", "tutorial", "how-to", "explanation", "reference")
* Discourse url (must be in the format "/t/-/<number>" - the discourse hyperlinks in your docs should also be in this format)
* Section (The header of any second-level navigation)
* Sub-section (if there is one, this will insert mini-headers on the landing pages)


Fetching the docs
=================

Once you have the file list, you can run the download script. If you're not
in the docs folder, ``cd`` to it first:

.. code-block::

    cd docs
    python3 download-docs.py

Set up Read the Docs
-----------------------

See the `Read the Docs at Canonical <https://library.canonical.com/documentation/read-the-docs>`_ and
`How to publish documentation on Read the Docs <https://library.canonical.com/documentation/publish-on-read-the-docs>`_ guides for
instructions on how to get started with Sphinx documentation.

Build the docs locally
----------------------

As with the starter pack, make sure you're in whatever directory contains your
index file and the Make targets (root, in the default case of this repo), then
run the following:

.. code-block::

    make install
    make html


Additional info
===============

It's likely that the spelling checks and link checks will throw a LOT of errors.
I used the ``.custom_wordlist.txt`` file to avoid having to deal with them while
trying to get the docs to build. Remember to fix them later!

(Same with broken links)
