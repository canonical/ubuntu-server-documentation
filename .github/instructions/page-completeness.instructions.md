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
element is missing, an empty structural placeholder may be added, but any body text that
depends on the author's understanding (section prose, commands, examples) must be left to
the contributor, not generated. The frontmatter `description` is the one exception: because
it is metadata summarizing an already-written page rather than part of the page's argument,
it may be drafted or refined when it is missing, over 160 characters, or does not accurately
reflect the page's contents (see below).

During review, only add empty placeholders for unconditional required structure. Do not add
empty conditional sections or metadata containers whose presence depends on the page's actual
content.

## Required on every page

- **Frontmatter `description`.** A MyST `html_meta` `description` is present, is fewer than
  160 characters, and accurately reflects the page's contents (not the scaffold placeholder).
  On a fully written page (new or existing), if the `description` is missing, too long, or
  does not match what the page actually covers, you may propose a replacement for the
  contributor to accept or adjust.
- **Reference anchor.** A `(slug)=` anchor sits immediately above the `#` title and matches
  the filename (without `.md`).
- **Single title.** Exactly one level-1 (`#`) heading.
- **Introduction.** Text follows the title before the first `##` heading, stating what the
  page covers.
- **No leftover scaffold.** No unfilled `<!-- ... -->` scaffold comments or placeholder
  tokens from `/new-page` remain.
- **Further reading.** This section is required only when the page links to additional sources
  and references of interest to a reader, collected at the bottom under a section named exactly
  "Further reading". When there are no such links, the section can be omitted.
  If a final references-style section exists under another name, it should be renamed to
  "Further reading". During review, do not add this section as an empty placeholder. When
  scaffolding a new page outline, an empty heading may be introduced if the contributor is
  expected to fill it in.

## Required by Diátaxis type

Confirm the sections required by the matching template are present and non-empty:

- **Tutorial** (`.github/instructions/tutorial-template.instructions.md`): an intro stating
  what the reader will achieve; descriptive (unnumbered) `##` stage headings; an outcome /
  next-steps close.
- **How-to** (`.github/instructions/how-to-template.instructions.md`): an intro describing
  the task; the task steps; an "Uninstall" section that returns the machine to its
  original state; and a "Further reading" section if applicable. New guides should include
  the Uninstall section; many existing guides predate it and are being backfilled, so report
  it as a suggestion to add when missing, not a blocking defect.
- **Explanation** (`.github/instructions/explanation-template.instructions.md`): an intro
  framing why the topic matters; concept sections (no step-by-step procedures).
- **Reference** (`.github/instructions/reference-template.instructions.md`): an intro stating
  what the page specifies; structured, scannable content (tables or definition lists).

## Wiring (checked, not auto-fixed)

- **Toctree.** Verify whether the page is referenced from the relevant `toctree` (section
  `index.md` or parent landing page) by searching the repository. Remind the contributor to
  add it only when it is not already referenced.
- **Redirect.** Only when the page actually renames, moves, or replaces an existing one,
  confirm `docs/redirects.txt` (or `redirects` in `docs/conf.py` for external targets) has a
  matching entry. A new page that is not moved or renamed needs no redirect.
