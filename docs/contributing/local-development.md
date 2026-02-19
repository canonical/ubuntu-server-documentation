---
myst:
  html_meta:
    description: "Learn how to set up your local environment, build the docs, then test and submit contributions to Ubuntu Server documentation."
---

(local-development)=
# Local development

This page outlines the different ways in which you can contribute to the Server
documentation. Please take the time to become familiar with the contents of this
page before you begin contributing.

## Prerequisites

**Code of Conduct**
: You will need to read and agree to the Ubuntu [Code of Conduct](https://ubuntu.com/community/docs/ethos/code-of-conduct). By participating, you implicitly agree to abide by the Code of Conduct. 

**GitHub account**
: You need a free [GitHub account](https://github.com/) to create issues, comment, reply, or submit contributions.
: You don't need to know `git` before you start. For many small contributions, especially where only one page is being changed, you can edit pages directly through GitHub's web interface.

## Workflow overview

- {ref}`Find an issue to work on <finding-issues>`
- {ref}`Pick your workflow <choose-workflow>`
- Work on the issue ({ref}`get help <get-help>` if you need it!)
- {ref}`Test your contribution <doc-testing>`
- {ref}`Submit it for review <submit-work>`

(finding-issues)=
## Find issues to work on

We use GitHub issues to track documentation tasks. Start by
[checking our issues list](https://github.com/canonical/ubuntu-server-documentation/issues)
to see if there are any tasks you'd like to work on.

You can see which issues are unassigned by selecting
"Assigned to nobody" from the "Assignee" drop-down menu (or [use this link](https://github.com/canonical/ubuntu-server-documentation/issues?q=is%3Aissue+is%3Aopen+no%3Aassignee) as
a shortcut).

### Claim an issue

If you find a task you want to work on, leave a comment on the issue to let us
know. A maintainer will respond and assign that issue to you.

You can claim one open issue at a time.

### Create a new issue

If you have an idea that isn't covered by an existing open issue, create one
with an outline of what you want to do. A maintainer will review your idea and
either:
- Agree the change is within the project's scope and assign it to you so you can begin working on it
- Discuss and offer suggestions to improve your outline
- Close the issue if it is out of scope of the project or does not meet our contribution guidelines

(choose-workflow)=
## Choose your workflow

After you have found an issue you want to work on, and have been assigned the
issue, you have two options:

* **Direct edits via GitHub web interface**: For simple changes like typos or
  minor corrections using the GitHub web interface, see
  {ref}`quickstart guide <small-changes-in-gh>`.

* **Local development**: For more substantial or complex changes, for example to
  multiple pages, continue with {ref}`local-setup`.

(small-changes-in-gh)=
### Small changes directly in GitHub

For small and straightforward contributions that don't need local testing, such
as typos or minor corrections, it can be easier to edit pages directly through
[GitHub's web interface](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files).
This approach is valid whether you are fixing a single typo, or making multiple
changes to a single file.

1. Navigate to the page you want to edit [in the documentation](https://documentation.ubuntu.com/server)
1. Click the "Edit on GitHub" button (pencil icon) at the top of the page (you will be prompted to create a GitHub account if you don't already have one)
1. Make your changes in the GitHub web editor and save them
1. Select "Create a new branch for this commit and start a pull request"
1. Fill in the pull request template, including a description of why the change is needed
1. Submit the pull request, and you're done!

(local-setup)=
## Local setup

For more substantial changes, e.g. where you're changing multiple pages, you
may prefer to work locally so you can build and test your changes while you work.

### Create a fork

Create your own fork of the [Ubuntu Server GitHub repository](https://github.com/canonical/ubuntu-server-documentation).

If you're not sure what this means or need some help getting started, check out
the [working with git](https://documentation.academy/docs/howto/get-started/using_git/)
guide from the Open Documentation Academy which walks through the process and
explains all this terminology.

Just remember to change all instances of `open-documentation-academy` in the
commands to `ubuntu-server-documentation`!

### Get the documentation

In your terminal, clone the Ubuntu Server documentation repository by running:

```bash
git clone git@github.com:canonical/ubuntu-server-documentation.git
```

This creates a new folder on your machine called
`ubuntu-server-documentation` containing the contents of this repository.

Navigate to this folder:

```bash
cd ubuntu-server-documentation
```

### Create a new branch

Before making any changes, ensure the `main` branch on your machine is
up-to-date with any recent changes made to the remote repository:

```bash
git pull
```

```{note}
This won't have any effect if you have only just cloned the repository
(since you're already up-to-date).
```

Now, create a branch and switch to it:

```bash
git checkout -b my-new-branch
```

It's a good idea to give your branch a descriptive name (something more useful
than `my-new-branch`). Then, even if you are working on multiple branches, you
will know at a glance what each of them is for.

## Build and preview

You're now ready to start working on the docs! Run the following command to
build a live preview:

```bash
make run
```

This builds **and serves** the documentation at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
It watches the folder so that whenever you save changes to a file, the page gets
rebuilt. In this way, you can see the effect of your changes (or be warned if
something got broken!).

If you are building locally on an Ubuntu Cloud VM or a container, you may
experience issues accessing the page from your host's browser. To resolve this,
add the export variable to your shell by running the following command:

```bash
export SPHINX_HOST=0.0.0.0
```

The `make run` command should then work as expected.

```{note}
If you have problems getting the documentation to run on your machine,
reach out to the team or leave a comment on your issue to get additional
support.
```

### Other build commands

You can also use these commands for different purposes:

- `make html` -- Build the documentation only (without serving)
- `make serve` -- Serve previously built documentation without rebuilding
- `make clean-doc` -- Clean all built files to start fresh

Run `make` by itself to see a list of all available commands.

### Writing guidance

Once your environment is set up and you have got your local copy running without
any build errors, check out our {ref}`guidance for writing <writing-guidance>`
section to find out about our style guide and other important information.

(doc-testing)=
## Test your changes

Once you think you are ready to submit your changes, test the documentation
to catch any spelling errors, broken links, or similar issues.
This allows reviewers to focus on the main changes you are proposing and
makes the review process more efficient.

### Automatic testing

Always run these commands before submitting a pull request:

```bash
make spelling
make linkcheck
```

The `spelling` command checks for spelling errors. If it flags a technical term
that is correctly spelled, add the term to `.custom_wordlist.txt` in the root
of the repository (in alphabetical order please!).

The `linkcheck` command verifies all links in the documentation are working.

These checks are run on pull requests when they are submitted, but if the checks
flag problems it will delay the review process.

### Manual testing

If your contribution contains any code or process steps, do a final run-through
of your guide from start to finish in a clean environment. This ensures
everything works as expected.

Particularly check code snippets -- does the output in your terminal match
what you've presented in the guide?

## Creating redirects

If you rename, move or delete an existing file, you *must* create a redirect for
that page to ensure users don't run into 404 errors when clicking links in the
published documentation.

### Internal redirects

To set up a redirect from one file path to another, add a line to the end of
`redirects.txt` file in the `docs/` directory, in the following format:

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
redirect in the `conf.py` file in the root directory.

Under the Redirects section, add the source page and the target page as follows:

```python
redirects = {
    "example/source": "https://exampletarget.org",
    "how-to/containers/lxc-containers": "https://linuxcontainers.org/lxc/documentation/",
}
```

When you set up a redirect in this way, the path of the source file you're
redirecting from should include everything *after* the base URL
(https://documentation.ubuntu.com/server).

(submit-work)=
## Submitting your pull request

Once you've completed and tested your changes, you're ready to submit them
for review.

### Commit your changes

Make sure all your proposed changes are committed:

- `git status` will show your not-yet committed changes
- Select the ones you want to add to each commit using `git add <filename>`
- Commit your selected changes using `git commit`

```{note}
Try to group your changes logically. For example, if you have one set of
changes that modifies spelling in 10 files, and another set of changes
that modifies formatting in 10 different files, you can group them into
two commits (one for spelling, and one for formatting). You don't need a
separate commit for every file.
```

### Push and create a pull request

Push the changes to your fork:

```bash
git push <your username> <branch name>
```

Then [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
against the Ubuntu Server documentation repository and fill in the pull request
template.

Click submit when you're ready!

### Read the Docs preview

You will be able to see a live preview of your documentation as it will appear
on Read the Docs at the bottom of your pull request's page. Where the checks
appear, click on "Show all checks" and next to the "docs/readthedocs" line,
click on "Details".

## Reviews

After you have submitted your PR, one of the Ubuntu Server docs maintainers
will review it. Depending on time zones and where we are in the development
cycle, there may be a delay before your PR is reviewed. Please be patient!

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
