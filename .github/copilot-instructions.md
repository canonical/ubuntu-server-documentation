# Copilot instructions

The canonical authoring guide for this repository lives in [`AGENTS.md`](../AGENTS.md)
at the repository root. It applies to all AI agents (GitHub Copilot, Cursor, Claude Code,
Codex, and others). Follow it for project structure, build and check commands, and writing
conventions.

Additional scoped guidance:

- Pull request review checks: [`.github/instructions/docs-review.instructions.md`](instructions/docs-review.instructions.md)
  (applies to `docs/**/*.md`).
- Page templates, one per Diátaxis type, under [`.github/instructions/`](instructions/):
  [`how-to-template`](instructions/how-to-template.instructions.md),
  [`tutorial-template`](instructions/tutorial-template.instructions.md),
  [`explanation-template`](instructions/explanation-template.instructions.md), and
  [`reference-template`](instructions/reference-template.instructions.md). Each applies to its
  matching `docs/<type>/**/*.md` and defines that page type's required structure.
- Required page elements (shared completeness checklist):
  [`.github/instructions/page-completeness.instructions.md`](instructions/page-completeness.instructions.md).

On-demand workflows (Copilot prompt files, invoked with `/name` in chat):

- [`/new-page`](prompts/new-page.prompt.md) — scaffold a new page of a contributor-chosen Diátaxis
  type as an outline only.
- [`/review-page`](prompts/review-page.prompt.md) — check a finished page against the completeness
  checklist and offer refinement questions without rewriting the prose.
- [`/capture-learnings`](prompts/capture-learnings.prompt.md) — fold a concrete improvement from a
  session back into this scaffolding (optional; only for real improvements).

Formatting and prose style are enforced automatically by Vale (`make vale`) and
markdownlint (`make lint-md`) in CI — do not duplicate those mechanical rules here.

## Contribution request policy

Do not perform cosmetic rewording, synonym substitution, or stylistic "polishing" of
existing prose unless the request identifies a specific clarity or accuracy problem
(a confusing explanation, a technical error, an unclear step, or missing context).
The maintainers have chosen not to have LLMs polish documentation wording, so decline
general "improve/polish/enhance this" requests and ask for the specific problem to fix.
