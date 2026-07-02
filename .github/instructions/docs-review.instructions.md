---
applyTo: "docs/**/*.md"
excludeAgent: "cloud-agent"
---

# Documentation review checks

Formatting and prose style (whitespace, blank lines, list markers, heading levels,
passive voice, filler words, US spelling) are enforced by Vale and markdownlint in CI.
Do **not** repeat those checks. Focus your review on the semantic rules below, which a
linter cannot catch. Flag a line only when it clearly violates one of these rules, and
give a one-line reason. Treat these as non-blocking suggestions unless they are factual
errors.

## Check for these

- **Nonexistent glossary term.** `{term}`X`` is used but `X` is not defined in
  `docs/reference/glossary.rst`. Suggest using plain text or adding the glossary entry.
- **Wrong admonition fence.** An admonition uses a backtick fence (` ```{note} `) instead
  of a colon fence. Change to `:::{note}` … `:::`.
- **Tab order.** A MyST tab set lists Ubuntu releases oldest-first. Suggest reordering to newest LTS first
  (e.g. `24.04` before `22.04`).
- **Missing redirect.** A page is renamed, moved, or deleted in this PR but `docs/redirects.txt`
  (or `redirects` in `docs/conf.py` for external targets) has no matching entry.
- **Blog link over upstream.** A link points to a blog post where official upstream
  documentation or a manpage exists. Suggest the authoritative source.
- **Unsupported-release / support-policy claim.** Text implies support for an obsolete release,
  or states that third-party/unsupported software is supported by Ubuntu. Flag for accuracy.
- **Legacy releases.** The maintainers support releases up to 10 years old in the documentation:
  flag references to releases older than 10 years for deprecation. Where such very old releases
  are referenced (for example "14.04 Trusty"), the page should make clear that support
  is only available through the Ubuntu Pro Legacy add-on.
- **Hard-coded role URL.** A manpage, Launchpad, or Matrix link is hard-coded instead of using
  the role (`{manpage}`, `{lpsrc}`, `{lpbug}`, `{matrix}`), which auto-generates the URL. Suggest the role instead.
- **Wrong cross-reference style.** An internal link uses a Markdown/`.md` link or `{doc}` instead of
  `{ref}`label``. Suggest the `{ref}` alternative.

## Required page elements

For a newly added page, also confirm it has the required structural elements listed in
`.github/instructions/page-completeness.instructions.md` (frontmatter `description`, a
`(slug)=` anchor matching the filename, a single `#` title, an introduction, the sections
its Diátaxis type requires, and no leftover scaffold comments). Flag any that are missing.

For any how-to page under review (new or existing), also check for an "Uninstall" section
that returns the machine to its original state. If it is missing, highlight it as a
suggestion for the contributor to consider adding — not a blocking issue. Many existing
guides are still being backfilled, so frame it as a recommendation, not a defect.
