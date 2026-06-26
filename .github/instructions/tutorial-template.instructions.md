---
applyTo: "docs/tutorial/**/*.md"
---

# Tutorial template

Tutorials are **learning-oriented**: they take a beginner through a single, complete,
successful experience by doing. The reader follows along; you guarantee the outcome.
Keep the scope small and the path linear — no branching, options, or alternatives.
For general conventions (anchors, headings, MyST roles, US English) follow `AGENTS.md`;
this file covers only the tutorial-specific shape. "We" is preferred over "you" in tutorials.

## Frontmatter

Begin with MyST frontmatter, replacing only the description (fewer than 160 characters):

```yaml
---
myst:
  html_meta:
    description: A summary of the page's content in fewer than 160 characters.
---
```

## Page anchor and title

```
(page-anchor)=
# Page title
```

- One `#` heading per page; the anchor must match the filename (without `.md`).
- Follow the title with a short intro stating **what the reader will build or achieve**
  and what they will have learned by the end.

## What you'll need (optional)

A short bullet list of prerequisites: prior pages to read, hardware, software, or accounts.
Omit if there are none.

## The guided path

The body of a tutorial is a guided journey, not a checklist. Use descriptive `##` headings
that name what the reader is doing at each stage (for example `## Install the package` or
`## Start the service`) — **never number the headings.** A tutorial is a single linear path
the reader walks with you, not a numbered list of tasks to tick off. Order the stages
logically so each one builds on the last: never ask the reader to do something that depends
on a stage they have not reached yet (for example, running a command from a package they
have not installed). Each stage:

- Is concrete and produces a visible, verifiable result the reader can confirm.
- Uses the `{terminal}` directive for command input and output.
- May include short paragraphs at key points giving the reader the context they need to follow along.
  Keep it brief — a sentence or two that helps the moment make sense. Move any longer
  discussion of *why* to a separate explanation page and link to it.

## Outcome and next steps

Close by confirming what the reader has accomplished, then point to logical next pages
(related how-to guides or explanations) using `{ref}` cross-references.

## Further reading

Include this section only when the page links to external resources; omit it entirely when
there are none. When present, name it exactly "Further reading" and link to reputable
upstream resources that help the reader go further:

```markdown
* [Link label](https://example.com)
```
