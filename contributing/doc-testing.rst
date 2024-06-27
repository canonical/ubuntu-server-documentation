.. _doc-testing:

Testing your documentation
**************************

Before pushing your changes, it's a good idea to test the documentation to
ensure you don't have any spelling errors, broken links, or similar. 

Some of the testing/validation tools aren't installed by default, so you will
need to install ``npm`` and ``snap`` as well:

.. code-block::

   sudo apt install npm snapd
   make woke-install
   make pa11y-install
