---
agent: agent
description: Capture a concrete learning from this session as a proposed update to the documentation scaffolding (AGENTS.md, instruction files, or prompts).
---

# Capture learnings into the scaffolding

Use this at the end of a session to fold a genuine improvement back into the repository's
agent scaffolding, so future agents and contributors benefit. Capturing is **optional** —
if the contributor does not want to record anything, stop without making changes.

## The bar: only capture real improvements

Propose a change **only** when this session produced a concrete learning that will lead to
one of the following:

- **Better performance** — a clearer instruction that helps agents produce better results.
- **Better rule adherence** — a rule that was ambiguous, missing, or easy to misread, now
  pinned down.
- **A closed loophole** — a genuine gap or edge case the existing scaffolding did not cover.
- **A correction** — an existing instruction that proved wrong, outdated, or contradictory.

Do **not** propose changes for their own sake. Rewording for style, restating something the
files already cover, or speculative "nice to have" additions are out of scope. If nothing in
this session clears this bar, say so plainly and make no changes.

## Where each kind of learning belongs

Route the proposed edit to the correct file, and keep it consistent with the existing structure:

- **Writing or convention rule** (applies to all pages) → `AGENTS.md`.
- **Page-type structural rule** → the matching template in `.github/instructions/`
  (`tutorial-`, `how-to-`, `explanation-`, or `reference-template.instructions.md`).
- **Required page element** → `.github/instructions/page-completeness.instructions.md`.
- **Review judgement check** (semantic, not a linter rule) → `.github/instructions/docs-review.instructions.md`.
- **Workflow behavior** (`/new-page`, `/review-page`, or this prompt) → the relevant file in
  `.github/prompts/`.

If a learning touches a rule that is enumerated in more than one place (for example the list
of page templates appears in both `AGENTS.md` and `.github/copilot-instructions.md`), call out
every file that must change so the cross-references stay correct.

Never duplicate a mechanical rule that Vale or markdownlint already enforces — those stay in CI.

## How to propose

1. State the learning in one or two sentences, and which of the bars above it meets.
1. Name the exact file(s) to change and show the specific edit for each.
1. Ask the contributor to confirm before writing anything. If they decline, make no changes.

Keep proposals small and concrete. One clear improvement beats a sweeping rewrite.
