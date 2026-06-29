---
agent: agent
description: Scaffold a new Ubuntu Server documentation page for a chosen Diátaxis type (outline only).
---

# New documentation page

Help the contributor scaffold a new page. Produce a **structural outline only** — headings,
frontmatter, anchors, and one-line guidance placeholders. Do **not** write the body prose:
per this repository's scope policy, the maintainers want contributors (not LLMs) to author
the documentation wording. Your job is to set up a correct, empty skeleton and explain what
goes where.

## Step 1 — Confirm the inputs

The contributor decides the Diátaxis type; **you must not choose or change it for them.**
Gather these inputs, asking only for the ones they have not already provided:

1. **Diátaxis type** — exactly one of: `tutorial`, `how-to`, `explanation`, or `reference`.
   This is the contributor's decision. If they have not stated a type, ask them to pick one
   and stop — do not infer it from their topic or notes, and do not recommend a type. If they
   ask for the definitions, you may quote the descriptions below, but the choice remains theirs:
   - **Tutorial** — a beginner learns by following a guaranteed, end-to-end exercise.
   - **How-to** — an existing user accomplishes a specific real-world task.
   - **Explanation** — a reader wants to understand a concept, with background and reasoning.
   - **Reference** — a reader looks up accurate, complete, factual detail.
1. **Topic / title** of the page.
1. **Target file path** under `docs/<diataxis-type>/` (and the parent directory if grouped by topic).
1. **Parent landing page / toctree file** — the `index.md` or section landing page that should
   list the new page in its `toctree`. This must be an explicit path (e.g.
   `docs/how-to/software.md`). Do not guess; ask if the contributor has not stated it.

The chosen type fully determines the shape of the outline (see Step 2). The same type must
always produce the same skeleton, regardless of which model runs this prompt.

## Step 1b — If the section does not exist yet

If the landing page the contributor named does not exist, the section is new. Do not force
the page into an unrelated existing section. Instead:

- Create the new section folder under `docs/<diataxis-type>/`, a new landing page with its
  own `(slug)=` anchor and `toctree`, and wire that landing page into the parent Diátaxis
  `index.md`, following the structure of the existing landing pages and index.
- Follow `.github/instructions/landing-pages.instructions.md` for the landing page's shape:
  start from its minimal template, and group entries with explanatory text rather than a flat
  list of links.
- The new page becomes the first entry in the new section's `toctree`.

When an existing section clearly fits the proposed content (for example, a Valkey page when a
`databases` section already exists), you may point this out as **non-prescriptive guidance** and
offer the alternative — but the section is the contributor's decision. Do not override it.
Mismatches are picked up at review time. Many possible topics and sections are undocumented,
so the absence of a section is not by itself a reason to refuse.

## Step 2 — Follow the matching template

Apply the template instructions for the chosen type, which are the single source of truth
for that page's shape:

- `tutorial` → `.github/instructions/tutorial-template.instructions.md`
- `how-to` → `.github/instructions/how-to-template.instructions.md`
- `explanation` → `.github/instructions/explanation-template.instructions.md`
- `reference` → `.github/instructions/reference-template.instructions.md`

Also apply the general conventions in `AGENTS.md` (US English, single `#` heading, MyST
roles, anchor matching the filename, etc.).

## Step 3 — Emit the skeleton

Create the new file at the agreed path containing **only**:

- The MyST frontmatter block with a placeholder `description` (note the < 160-character limit).
- A `(slug)=` anchor that matches the filename, immediately above the `#` title.
- The section headings the template requires, in order.
- Under each heading, a short HTML comment (`<!-- ... -->`) describing what the contributor
  should write there. Do not fill in real content, commands, or prose.
- The template's "Further reading" heading as a placeholder, with an HTML comment noting that
  this section is only for external links and should be removed if the finished page links to
  none.

If the contributor pasted rough notes, slot each note under the heading it belongs to as a
bullet inside that section's HTML comment, kept close to their original wording. Do not
expand notes into finished prose — the contributor writes the actual content.

## Step 4 — Wire up the toctree

After creating the skeleton file, add the new page to the `toctree` in the landing page
confirmed in Step 1. Do this yourself — do not ask the contributor to do it.

- Open the landing page file.
- Add an entry in the appropriate `toctree` block, for example:
  `Page title <type/filename>`
- Add a matching bullet in the prose list below the `toctree` (if the landing page follows
  that pattern), using a `{ref}` role and a one-line description of what the page covers.
- Add a redirect to `docs/redirects.txt` only if this page replaces or moves an existing one.

## Step 5 — Give the contributor their next steps

After creating the file and wiring the toctree, do not run lint, tests or other validation commands.
Tell the contributor:

- The skeleton has been created at the agreed path and wired into the toctree.
- Suggest to the contributor that they can view their rendered page locally, by running:
  ```
  make clean && make run
  ```
  Then they can open <http://127.0.0.1:8000> in a browser.
- Once they have written their content, suggest that they run the following checks from the `docs/` directory:
  ```
  make spelling
  make vale
  make lint-md
  ```

Keep the skeleton minimal and correct; leave the writing to the contributor.
