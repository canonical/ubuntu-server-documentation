# Landing page documentation standards

This file is a shared reference, not an auto-applied rule: it intentionally has no `applyTo`
frontmatter. The `/new-page` prompt pulls it in by name when it runs, so it applies to every
landing page (not only the top-level `index.md` pages) without loading automatically on every
docs edit.

Use these rules when creating or updating section landing pages — the `index.md` pages at the
root of each Diátaxis type, and the section landing pages they link to (for example
`docs/explanation/software.md`). Landing pages guide users through a section's content by
organizing links into logical groups with explanatory text.

## Minimal template

A new section landing page should start minimal — one group, one entry, with room to grow.
Add further groups and `toctree` blocks only as the section gains pages:

````markdown
---
myst:
  html_meta:
    description: A summary of the section in fewer than 160 characters.
---

(section-slug)=
# Section title

One sentence explaining what this section contains and its purpose.

## Group heading

One to three sentences explaining what this group covers and when users need it.

* {ref}`Page title <page-slug>` shows you how to ...

```{toctree}
:hidden:

Page title <section/page-filename>
```
````

## Landing page structure

### Bad pattern (never do this)

```markdown
# How-to guides

* {ref}`Install <install>`
* {ref}`Deploy to ABC <deploy-to-abc>`
* {ref}`Deploy to PQR <deploy-to-pqr>`
* {ref}`Deploy to XYZ <deploy-to-xyz>`
* {ref}`Manage resources <manage-resources>`
* {ref}`Add instances <add-instances>`
* {ref}`Monitor performance <monitor-performance>`
* {ref}`Diagnose performance issues <diagnose-performance-issues>`
* {ref}`Configure and manage logging <configure-and-manage-logging>`
* {ref}`Troubleshooting <troubleshooting>`
```

**Problems**:

- Flat list with no organization
- No context or explanation
- User must guess relationships between topics
- Doesn't convey workflow or lifecycle

### Good pattern (always do this)

```markdown
# How-to guides

These guides accompany you through the complete [Product] operations lifecycle.

## Installation and deployment

Installation follows a broadly similar pattern on all platforms, but due to
differences in the platforms, configuration and deployment must be approached
differently in each case.

* {ref}`Install <install>`
* {ref}`Deploy to ABC <deploy-to-abc>`
* {ref}`Deploy to PQR <deploy-to-pqr>`
* {ref}`Deploy to XYZ <deploy-to-xyz>`

## Scaling

As your needs grow, a deployment can be scaled to meet increased traffic needs,
either by allocating additional resources (CPU, RAM, etc) or by adding entire
application instances. See {ref}`Approaches to scaling <approaches-to-scaling>` for more
discussion of which strategy to adopt.

* {ref}`Manage resources <manage-resources>`
* {ref}`Add instances <add-instances>`

## Monitoring and troubleshooting

* {ref}`Monitor performance <monitor-performance>`
* {ref}`Diagnose performance issues <diagnose-performance-issues>`
* {ref}`Configure and manage logging <configure-and-manage-logging>`
* {ref}`Troubleshooting <troubleshooting>`
```

**What makes this good**:

- Opening sentence establishes section purpose
- Content grouped by lifecycle stage or workflow
- Each group has explanatory text providing context
- Cross-references to related conceptual content where helpful
- Shows relationships between topics
- Guides user through logical progression

### Landing page rules

1. **Start with orientation**: One sentence explaining what this section contains and its purpose
1. **Group by workflow/lifecycle**: Not alphabetically or by topic in isolation
1. **Add explanatory text**: Each group needs 1-3 sentences explaining:
   - What this group of topics covers
   - When/why users need these guides
   - How topics relate to each other
   - Links to related conceptual material (Explanation section)
1. **Show progression**: Order groups to reflect user journey or operational lifecycle
1. **Cross-reference thoughtfully**: Link to Explanation topics that provide context for decisions
1. **Keep scannable**: Use clear headings, bullets, and whitespace

### Section-specific guidance

**Tutorial landing pages** (`docs/tutorial/index.md`) should group and explain content flow:

- Organize by learning progression (beginner to advanced)
- Explain prerequisites and what each tutorial teaches
- Indicate estimated time or difficulty

**How-to landing pages** (`docs/how-to/index.md`) should organize by lifecycle/workflow:

- Organize by operational lifecycle or workflow stages
- Group related operations together
- Link to conceptual content that helps users choose between approaches

**Reference landing pages** (`docs/reference/index.md`) should organize by logical groupings:

- Organize by logical categories (API types, command groups, etc.)
- Provide brief explanation of each category's purpose
- Can be more list-like than other sections, but still grouped

**Explanation landing pages** (`docs/explanation/index.md`) should group related conceptual topics:

- Organize by theme or architectural layer
- Group related conceptual topics
- Indicate which topics are foundational vs. advanced

## Quality checklist

Before committing landing page changes:

- [ ] Landing pages group content logically (not alphabetically)
- [ ] Each group has explanatory text (not just a heading)
- [ ] Cross-references to related content where helpful
- [ ] Content follows user journey or lifecycle progression
- [ ] Tone is welcoming and informative
- [ ] No flat lists without context
