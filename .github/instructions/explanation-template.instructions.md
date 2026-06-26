---
applyTo: "docs/explanation/**/*.md"
---

# Explanation template

Explanation pages are **understanding-oriented**: they clarify and illuminate a topic,
giving background, context, and reasoning. They are for reading and reflection, not for
doing — so they contain **no step-by-step instructions** (link to a how-to or tutorial
for those). Discuss *why* and *how it works*, including alternatives, trade-offs, and
history where useful. For general conventions (anchors, headings, MyST roles, US English)
follow `AGENTS.md`; this file covers only the explanation-specific shape.

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
- Follow the title with a short intro framing the topic and **why it matters** to the reader.

## Concept sections

Organize the body into `##` sections that build understanding, for example:

- An introduction to the concept and the problem it addresses.
- How it works, and how the pieces fit together.
- Available options or approaches, with their trade-offs.
- Background or context (history, related standards) where it aids understanding.
- Relevant, illustrative examples

Use prose and diagrams over command listings. If you must show configuration, keep it
illustrative rather than a procedure to follow.

## See also

Cross-reference the related how-to guides, tutorials, and reference pages with `{ref}`,
so readers can act on what they have just understood.

## Further reading

Include this section only when the page links to external resources; omit it entirely when
there are none. When present, name it exactly "Further reading" and link to reputable
upstream resources for deeper background:

```markdown
* [Link label](https://example.com)
```
