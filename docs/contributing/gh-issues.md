---
myst:
  html_meta:
    description: "Learn how to find and select GitHub issues to work on for Ubuntu Server documentation contributions."
---

(finding-issues)=
# Find issues to work on

We use GitHub issues to track documentation tasks. Start by checking out
[the issues list](https://github.com/canonical/ubuntu-server-documentation/issues) to see if there are any tasks you'd like to work on. We
use labels to help filter the tasks that need to be done and to show whether
they're assigned to someone or not.

## Get an issue assigned

When you find a task you want to work on, leave a comment on the issue saying
you'd like to be assigned the task, with an estimated date for when you hope to
complete it. One of the documentation maintainers will respond and assign
that task to you.

```{note}
There is no time limit for completing a task, but if you need more time,
need help, or won't be able to complete the issue after all, make sure to
comment on the issue to let us know. It's quite normal for plans to change,
and handing an issue back won't prevent you from picking up more issues in
the future!

Issues that have no work being done on them, with no updates from the
author, will be considered stale after one month and will be unassigned to
allow others a chance to pick them up.
```

Each issue can be worked on by a single person, and each person can work on one
issue at a time. You can see which issues are unassigned by selecting
"Assigned to nobody" from the "Assignee" drop-down menu (or [use this link](https://github.com/canonical/ubuntu-server-documentation/issues?q=is%3Aissue+is%3Aopen+no%3Aassignee) as
a shortcut).

```{include} issue-labels.txt

```

## After you find an issue

After you have found an issue you want to work on, and have been assigned the
issue, you will want to either use the [GitHub web interface](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files) to create a
quick pull request, or fetch the documentation to your own machine so you can
{ref}`build the documentation locally <build-locally>` and work on your own
local copy.
