---
myst:
  html_meta:
    description: "Learn how to contribute to Ubuntu Server documentation, including guidelines for writing, submitting, and reviewing content."
---

(contribute)=
# Contribute to this documentation

Contributing to documentation can be a fantastic way to get started as a
contributor to open source projects, no matter your level of experience!

The Ubuntu Server documentation is
[hosted in GitHub](https://github.com/canonical/ubuntu-server-documentation) and
[rendered on Read the Docs](https://documentation.ubuntu.com/server/). It is a
collaborative effort between Canonical and the Ubuntu community. There are many
ways to contribute to the Ubuntu Server documentation, including many {ref}`options
that don't require any coding <contrib-types>`.

We hope to make it as easy as possible to contribute. If you need help at all
with the contribution process, {ref}`please let us know <get-help>`!

## The Open Documentation Academy

Ubuntu Server is a proud member of the
[Canonical Open Documentation Academy](https://github.com/canonical/open-documentation-academy)
(CODA). If you are new to making open source contributions, or new to technical
writing and want to boost your skills -- or both! -- we will be glad to help.

## Contributions we accept

We especially value contributions that improve the documentation's clarity,
accuracy, and usefulness. If you spot a problem, you can report it to us using
the "Give feedback" button at the top of every documentation page. Please give
us as much information as you can to help us address the problem.

If the issue is one of the following very small issues, and you want to fix it
yourself, you can submit a pull request (PR) with your changes
{ref}`directly in the GitHub web interface <small-changes-in-gh>`:

- Typo corrections
- Minor technical corrections
- Broken link fixes
- Small clarifications

For changes larger than those, we require contributor PRs to be tied to an issue.
Examples of changes that require an issue are things like:

- Adding new sections or pages
- Restructuring existing pages
- Extensive rewording
- Significant technical corrections or updates
- Feature additions or enhancements

For the full description of the contribution workflow, see {ref}`local-development`.

## Contributions we don't accept

We reserve the right to reject any contribution at our own discretion where:

**The outline of proposed work has not already been agreed by a maintainer.**
: To protect maintainers' limited time, we do not accept unsolicited contributions. A PR must be tied to a valid and agreed issue unless it only makes a small change. Submitting an issue after a PR doesn't *guarantee* that we will then accept the PR. To save yourself time, effort, and frustration, please {ref}`follow the outlined procedures <local-development>`.

**The pull request far exceeds the scope of what was agreed.**
: "Scope creep" makes it much harder to review and accept changes. If a pull request becomes too large, we may ask you to break it into multiple smaller PRs. Stick to the scope of the original issue as much as you can -- if you discover more changes need to be made, discuss them in the PR or the original issue. A new PR can be submitted with the extra fixes.

**The contribution makes changes without value.**
: To have value, changes must be a *specific and concrete improvement* over what already exists. We don't accept generic "polishing" (e.g. substituting synonyms, rewording without adding clarity). If your contribution contains *some* of these, we will ask you to undo them -- but will gladly accept the remaining parts of your pull request that are real improvements. If your contribution *only* contains low-value changes, it will be rejected.

**We deem the contribution to be AI generated.**
: We don't want any part of the Server documentation to look or feel like it was produced by AI. Therefore, if what you submitted cannot be easily distinguished from AI output, it does not meet our contribution requirements. See our {ref}`acceptable-use-of-ai` policy.

**The issue the pull request is addressing was assigned to someone else.**
: We want to make this a safe place for contributors to work on issues in their own time and without pressure. Please treat others as you'd want to be treated. If you like an issue someone else is working on, let us know and we'll create a similar one for you.

## AI policy

The Ubuntu Server documentation has been created by humans, for humans. The occasional "jagged edges" you might find (typos, slightly unconventional wording, humour) represent the very human voices of the people who collaborated
to create it. We don't want to average those away by passing the documentation through LLMs.

This policy exists to protect our readers, our community of contributors, and the project maintainers.
As AI continues to evolve, we will update these guidelines accordingly.

(acceptable-use-of-ai)=
### Acceptable use of AI

We don't ban our contributors from using AI. However, we do expect anyone contributing to this project to use it responsibly, as a helper, and not as something that replaces them. Some examples of acceptable usage include:

- Using AI as a spellchecker or grammar helper
- Using it to help with translation into English
- Using it to help outline and organize a draft
- Using it adversarially, to point out missing sections
- Ensuring formatting adheres to our style guide

We want to be open and transparent with our users about the way in which AI is or is not used in the Server documentation. We (the maintainers) have been experimenting with the ways in which AI can be used to improve the experience for our readers, and we don't object to contributors doing the same -- with the following caveats:

1. **Agreement**: Any such work you do *must* be tied to an issue, and be agreed as valid and necessary with the maintainers *before* you start. Only maintainers are exempt from this rule, since they are most familiar with the project and its scope.

2. **Honesty**: If you use an "AI assist" when making a contribution, you *must* disclose that you used it, and how you used it in the pull request description.

3. **Accessibility**: Issues marked as "good first issues" and "Open Documentation Academy" are *specifically* created and intended for people new to Open Source to get started in a safe place. These issues are easy to complete, well-described, and self-contained for new contributors to learn from. These issues are not for AI.

4. **Responsibility**: Make sure that even if you use AI, you are still adding value based on your own personal skills and competency. You must understand what you're submitting, even if you used an LLM to help you.

## Thank you!

Lastly, we would like to thank you for spending your time to help make the
Ubuntu Server documentation better. Every step in the right direction is a step
worth taking, no matter how large or small.

Check out what {ref}`our contributors <contributors>` have been working on!

```{toctree}
:maxdepth: 1
:hidden:

self
contrib-types
local-development
writing-guidance
get-help
contributors
```
