---
applyTo: "docs/reference/**/*.md"
---

# Reference template

Reference pages are **information-oriented**: they describe the machinery accurately and
completely so readers can look things up. They are consulted, not read through. Keep them
terse, neutral, and consistent — describe *what is*, not how to use it or why (link to
how-to and explanation pages for those). For general conventions (anchors, headings, MyST
roles, US English) follow `AGENTS.md`; this file covers only the reference-specific shape.

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
- Follow the title with a one- or two-sentence intro stating exactly what the page lists
  or specifies, and pointing to `man <command>` or upstream docs for full detail.

## Structured content

Present the information in a predictable, scannable structure, for example:

- Tables for commands, options, parameters, ports, or values.
- Definition or bullet lists for terms and their meanings.
- `##` and `###` sections that group related entries logically.

Be complete within the page's scope and keep entries parallel in wording. Use `{manpage}`
roles on the first mention of a tool and `{term}` only for entries in the glossary.

## Further reading

Include this section only when the page links to external resources; omit it entirely when
there are none. When present, name it exactly "Further reading" and link to the
authoritative upstream specifications or manual pages:

```markdown
* [Link label](https://example.com)
```
