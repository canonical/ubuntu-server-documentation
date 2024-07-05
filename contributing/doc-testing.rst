.. _doc-testing:

Testing your changes
====================

Before pushing your changes or creating a pull request, you should first test
the documentation to catch any spelling errors, broken links, or similar. 
This allows the reviewers to focus on the main changes you are proposing and
makes the review process more efficient.

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
just to make sure everything works as you expected.

Particularly check the code snippets -- does the output in your terminal match
what you've presented in the guide?
