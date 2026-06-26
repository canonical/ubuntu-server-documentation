# Page completeness checklist

This file is a shared reference, not an auto-applied rule: it intentionally has no `applyTo`
frontmatter. The `/review-page` prompt and `docs-review.instructions.md` pull it in by name
when they run, so it does not need to load automatically on every docs edit. Do not add an
`applyTo` here.

The required structural elements every documentation page must have before it is ready
to merge. This list is the single source of truth shared by the `/review-page` prompt
(self-review before opening a pull request) and the pull-request review checks in
`docs-review.instructions.md`.

These are **objective, presence-based** checks: an element is either there or it is not.
They do not judge the quality of the prose — that is the contributor's work. Where an
element is missing, an empty structural placeholder may be added, but any text that
depends on the author's understanding (for example the `description` wording) must be
left to the contributor, not generated.

## Required on every page

- **Frontmatter `description`.** A MyST `html_meta` `description` is present, is fewer than
  160 characters, and accurately reflects the page's contents (not the scaffold placeholder).
- **Reference anchor.** A `(slug)=` anchor sits immediately above the `#` title and matches
  the filename (without `.md`).
- **Single title.** Exactly one level-1 (`#`) heading.
- **Introduction.** Text follows the title before the first `##` heading, stating what the
  page covers.
- **No leftover scaffold.** No unfilled `<!-- ... -->` scaffold comments or placeholder
  tokens from `/new-page` remain.
- **Further reading.** If the page links to external sources, they are collected under a
  "Further reading" section at the bottom.

## Required by Diátaxis type

Confirm the sections required by the matching template are present and non-empty:

- **Tutorial** (`.github/instructions/tutorial-template.instructions.md`): an intro stating
  what the reader will achieve; descriptive (unnumbered) `##` stage headings; an outcome /
  next-steps close.
- **How-to** (`.github/instructions/how-to-template.instructions.md`): an intro describing
  the task; the task steps; an "Uninstall" section that returns the machine to its
  original state; and a "Further reading" section. New guides should include the Uninstall section;
  many existing guides predate it and are being backfilled, so report it as a suggestion
  to add when missing, not a blocking defect.
- **Explanation** (`.github/instructions/explanation-template.instructions.md`): an intro
  framing why the topic matters; concept sections (no step-by-step procedures).
- **Reference** (`.github/instructions/reference-template.instructions.md`): an intro stating
  what the page specifies; structured, scannable content (tables or definition lists).

## Wiring (checked, not auto-fixed)

- **Toctree.** The new page is referenced from the relevant `toctree` (section `index.md`
  or parent landing page).
- **Redirect.** If the page renames, moves, or replaces an existing one, `docs/redirects.txt`
  (or `redirects` in `docs/conf.py` for external targets) has a matching entry.
