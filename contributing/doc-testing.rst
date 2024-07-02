.. _doc-testing:

Testing your changes
====================

Before pushing your changes or creating a pull request, it's a good idea to
first test the documentation to ensure you don't have any spelling errors,
broken links, or similar. 

We run automatic checks on the documentation for these things, so you will see
a summary of any errors when you submit your pull request, but it will help us
to review your PR more efficiently if these checks are run (and passing) before
you submit.

You can run:

.. code-block:: bash

   make spelling
   make linkcheck
   
To perform a full spelling and link check. You can also run ``make`` by itself
to see a list of all the possible ``make`` targets. 

Manual testing
==============

If your contribution contains any code or process steps, it's a good idea to do
a final run-through of your guide from start to finish in a clean environment,
just to make sure the experience is as you expected.

Particularly check the code snippets -- does the output in your terminal match
what you've presented in the guide?
