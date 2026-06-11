---
applyTo: "docs/how-to/**/*.md"
---

# How-to guide template

When creating or editing how-to guides in this repository, follow the structure below. All sections are required unless marked optional.

## Frontmatter

Every page must begin with MyST frontmatter. Use this block exactly, replacing only the description value:

```yaml
---
myst:
  html_meta:
    description: A summary of the page's content in fewer than 160 characters.
---
```

## Page anchor and title

Immediately after the frontmatter, add a page anchor and a single level-1 heading:

```
(page-anchor)=
# Page title
```

- Use only one `#` heading per page.
- The anchor must match the filename (without the `.md` extension) so cross-references are consistent.
- Additional anchors can be added above subsequent headings to allow direct cross-referencing to sections.

Follow the title with a brief introduction describing what the guide covers (and, if useful, what it does not cover).

## Prerequisites

List anything the reader must do or know before starting:

- Suggested pre-reading or related pages they should consult first.
- Hardware or software requirements.

Omit this section if there are no prerequisites.

## Install \<package\>

Provide the steps needed to install the package or software being documented.

## Configure \<package\>

Describe the configuration options. For long sections, use level-3 (`###`) subheadings to break content into logical chunks so readers can navigate using the in-page table of contents.

Highlight any security considerations the reader should be aware of during configuration.

## Information on using the package (optional)

Include best practices, worked examples, or other information that helps the reader get value from the software. This section is optional but encouraged.

## Further reading

Link to reputable external resources (official upstream documentation, books, RFCs, etc.) that help the reader learn more:

```markdown
* [Link label](https://example.com)
```
