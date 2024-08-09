.. _submit-work:

Submitting your work
********************

You should submit your pull request (PR) to the **Ubuntu Server documentation
repository** (repo), whether you claimed your issue via the ODA repo or the
Ubuntu Server repo.

If you need help with any aspect of the process (forking the repo, committing,
pushing, etc) then refer to the `getting started with git`_ guide on the ODA
repo, which will guide you through those steps as you construct your changes.

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

Submit a pull request
=====================

- Make sure all your proposed changes are committed:

  - ``git status`` will show your uncomitted changes
  - Select the ones you want to add to each commit using ``git add <filename>``
  - Commit your selected changes using ``git commit``.

  .. note::
     Try to group your changes "logically". For example, if you have one set of
     changes that modifies spelling in 10 files, and another set of changes
     that modifies formatting in 10 different files, you can group them into
     two commits (one for spelling, and one for formatting). You don't need a
     separate commit for every file.

- Push the changes to your fork: ``git push <your username> <branch name>``

- `Create a Pull Request`_ against the Ubuntu Server documentation repository.

- `Link your pull request to your issue`_, typically by adding
  ``fixes #<issue-number>`` to your description.

- Give your pull request a description and click on submit!

Read the Docs preview
---------------------

You will be able to see a live preview of your documentation as it will appear
on Read the Docs at the bottom of your pull request's page -- where the checks
appear, click on "Show all checks" and next to the "docs/readthedocs" line,
click on "Details".


Reviews
=======

After you have submitted your PR, one of the Ubuntu Server team maintainers
will be in touch to review it. Depending on time zones, there may be a small
delay in your PR being reviewed. Please be patient!

One or more of the Ubuntu Server team maintainers will review the changes you
have proposed, and they will either "Approve" the changes, or leave some
feedback and suggested changes (with reasons). If you agree with the feedback,
you can make the suggested changes, and the reviewer will approve the PR.

If you disagree with any parts of the review, it's OK to discuss this with the
reviewer -- feedback is made in good faith, and is intended to help strengthen
your contribution. This is a collaboration, after all! It's quite normal to
have some back-and-forth on a PR, but it should be a respectful dialogue on all
sides. 

Once the discussion has concluded, and you have made any agreed changes, the PR
will be approved and then merged. Congratulations (and thank you)! You are now
an open source contributor!

.. _getting started with git: https://github.com/canonical/open-documentation-academy/blob/main/getting-started/using_git.md
.. _Create a Pull Request: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
.. _Link your pull request to your issue: https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
