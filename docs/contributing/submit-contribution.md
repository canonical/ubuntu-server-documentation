---
myst:
  html_meta:
    description: "Step-by-step guide for submitting your Ubuntu Server documentation contributions through pull requests."
---

(submit-work)=
# Submitting your work

You should submit your pull request (PR) to the **Ubuntu Server documentation
repository**, whether you claimed your issue via the ODA repository or the
Ubuntu Server repository.

If you need help with any aspect of the process (forking the repository, committing,
pushing, etc) then refer to the [getting started with git](https://documentation.academy/docs/howto/get-started/using_git/) guide on the ODA
repository, which will guide you through those steps as you construct your changes.

(doc-testing)=
## Testing your changes

Before pushing your changes or creating a pull request, you should first test
the documentation to catch any spelling errors, broken links, or similar. 
This allows the reviewers to focus on the main changes you are proposing and
makes the review process more efficient.

You can run:

```bash
make spelling
make linkcheck
```
   
To perform a full spelling and link check. You can also run `make` by itself
to see a list of all the possible `make` targets.

## Check if you need redirects

If you rename, move or delete an existing file, a corresponding redirect must
be created to ensure users don't run into 404 errors when clicking links in the
published documentation.

### Internal redirects

To set up a redirect from one file path to another, add a line to the end of the
redirects.txt` file in the root directory, in the following format:

```text
redirect/path/from/ redirect/path/to/
```

Note that since we use `dirhtml` to build, the built documentation is in the
format `path/to/file/index.html` where `file` corresponds to the file name
you are redirecting. This means that you only need a trailing slash at the end
of the file name, without the file extension. See the
[Sphinx Rediraffe docs](https://sphinxext-rediraffe.readthedocs.io/en/latest/)
for more guidance, or reach out to us for help.

### External redirects

Rediraffe doesn't currently handle redirects from a page to an external website.
To redirect outside of the Server documentation, you will need to set up a
redirect in the `custom_conf.py` file in the root directory. 

Under the Redirects section, you can add the source page and the target page as
follows:

```python
redirects = {
    "example/source": "https://exampletarget.org",
    "how-to/containers/lxc-containers": "https://linuxcontainers.org/lxc/documentation/"
}
```

When you set up a redirect in this way, the path of the source file you're redirecting
from should include everything *after* the base URL (https://documentation.ubuntu.com/server).

## Manual testing

If your contribution contains any code or process steps, it's a good idea to do
a final run-through of your guide from start to finish in a clean environment,
just to make sure everything works as you expected.

Particularly check the code snippets -- does the output in your terminal match
what you've presented in the guide?

## Submit a pull request

- Make sure all your proposed changes are committed:

  - `git status` will show your not-yet committed changes
  - Select the ones you want to add to each commit using `git add <filename>`
  - Commit your selected changes using `git commit`.

  ```{note}
  Try to group your changes "logically". For example, if you have one set of
  changes that modifies spelling in 10 files, and another set of changes
  that modifies formatting in 10 different files, you can group them into
  two commits (one for spelling, and one for formatting). You don't need a
  separate commit for every file.
  ```

- Push the changes to your fork: `git push <your username> <branch name>`

- [Create a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) against the Ubuntu Server documentation repository.

- [Link your pull request to your issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue), typically by adding
  `fixes #<issue-number>` to your description.

- Give your pull request a description and click on submit!

### Read the Docs preview

You will be able to see a live preview of your documentation as it will appear
on Read the Docs at the bottom of your pull request's page -- where the checks
appear, click on "Show all checks" and next to the "docs/readthedocs" line,
click on "Details".


## Reviews

After you have submitted your PR, one of the Ubuntu Server team maintainers
will be in touch to review it. Depending on time zones, there may be a delay
in your PR being reviewed. Please be patient!

One or more of the Ubuntu Server team maintainers will review the changes you
have proposed, and they will either "Approve" the changes, or leave some
feedback and suggested changes (with reasons). If you agree with the feedback,
you can make the suggested changes, and the reviewer will approve the PR.

```{note}
The team has adopted the [Conventional Comments](https://conventionalcomments.org/)
approach with the intention of making feedback easier to parse.
```

If you disagree with any parts of the review, it's OK to discuss this with the
reviewer -- feedback is made in good faith, and is intended to help strengthen
your contribution. This is a collaboration, after all! It's quite normal to
have some back-and-forth on a PR, but it should be a respectful dialogue on all
sides. 

Once the discussion has concluded, and you have made any agreed changes, the PR
will be approved and then merged. Congratulations (and thank you)! You are now
an open source contributor!
