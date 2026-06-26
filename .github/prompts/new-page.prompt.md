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
1. **Target file path** under `docs/<type>/` (and the parent directory if grouped by topic).

The chosen type fully determines the shape of the outline (see Step 2). The same type must
always produce the same skeleton, regardless of which model runs this prompt.

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

If the contributor pasted rough notes, slot each note under the heading it belongs to as a
bullet inside that section's HTML comment, kept close to their original wording. Do not
expand notes into finished prose — the contributor writes the actual content.

## Step 4 — Remind about wiring up the page

After creating the file, tell the contributor to:

- Add the page to the relevant `toctree` (usually the section `index.md` or parent landing page).
- Add a redirect to `docs/redirects.txt` only if this page replaces or moves an existing one.
- Run `make spelling`, `make vale`, and `make lint-md` from `docs/` once they have written content.

Keep the skeleton minimal and correct; leave the writing to the contributor.
