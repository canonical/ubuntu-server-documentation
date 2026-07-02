# Ubuntu Server Documentation – agent guide

Canonical source of authoring conventions for AI agents (GitHub Copilot, Cursor,
Claude Code, Codex, etc.) working in this repository. Keep edits aligned with these
rules. Formatting and prose style are enforced automatically by Vale and markdownlint
in CI — do not restate or second-guess those mechanical rules here.

## What this project is

Sphinx-based documentation for **Ubuntu Server**, built with the [Canonical Sphinx Stack](https://github.com/canonical/sphinx-stack). Content targets the latest Ubuntu LTS release and calls out version-specific
differences in-page (this project does **not** use per-release branches). Pages are
Markdown (`.md`) with MyST syntax. Source lives under `docs/`.

## Layout

Content follows the [Diátaxis](https://diataxis.fr/) framework:

- `docs/tutorial/` – learning-oriented getting-started guides
- `docs/how-to/` – task-oriented guides, grouped by topic
- `docs/explanation/` – concept and background material
- `docs/reference/` – specifications, glossary, system requirements
- `docs/contributing/` – contributor documentation

Key files: `docs/conf.py` (Sphinx config), `docs/redirects.txt` (internal redirects),
`docs/.custom_wordlist.txt` (spelling exceptions), `docs/reference/glossary.rst` (terms).

## Build and check (run from `docs/`)

```bash
make install      # set up the virtualenv
make run          # build, watch, and serve at http://127.0.0.1:8000
make html         # build only
make spelling     # spell check (exceptions in .custom_wordlist.txt)
make linkcheck    # verify links
make woke         # inclusive language check
make vale         # Canonical style guide check
make lint-md      # Markdown lint
```

## Writing conventions

### Language

- Use US English (`en-US`): "initialize" not "initialise", "color" not "colour".
- Expand acronyms on first use, e.g. "Yet Another Markup Language (YAML)".
- Use active voice and second person ("you"). "We" is acceptable in tutorials.
- Use descriptive link text that names the destination — never "click here" or "see this page".
- Avoid filler words: "simply", "just", "easy/easily", "actually", "basically", "obviously".
- Never use emojis.

### Structure

- Name files in kebab-case (lowercase words separated by hyphens), wherever possible.
- Use sentence case for headings (capitalize the first word and proper nouns only).
- One level-1 heading (`#`) per page. Don't skip heading levels; put text between consecutive headings.
- Every page must have a reference anchor `(slug)=` immediately above the `#` title, and that anchor
  must match the filename (without `.md`). Anchors above other headings are optional but recommended
  to ease cross-referencing. All anchors must be unique.
- Numbered lists: use `1.` for every item (Sphinx auto-renumbers).
- Don't end list items with a full stop unless an item contains a sentence — if one item in a
  list needs a full stop, add one to every item in that list.
- Use lists only where they aid the reader, and avoid nesting them more than two levels deep.
  If a list item needs more than one or two sentences, use a
  [definition list](https://mystmd.org/guide/typography#definition-lists) instead.
- Where a page has optional closing sections, prefer this order: "Next steps" (penultimate),
  then "Further reading" (last). Either or both may be omitted when they don't add value.
- For how-to guides specifically, use `.github/instructions/how-to-template.instructions.md`.

### Markup and roles

Use MyST roles so URLs auto-generate on rebuild — don't hard-code these links:

- {manpage}`tool(1)` for command-line tools (first mention).
- {term}`term` only for entries that exist in `docs/reference/glossary.rst`.
- {ref}`label` for internal cross-references. Don't use `{doc}` or bare Markdown/`.md` links —
  `{ref}` is more robust and accessible.
- {matrix}`channel`, {lpsrc}`package`, {lpbug}`number` for Matrix/Launchpad references.
- UI roles are encouraged where they apply: {guilabel}, {kbd} (keyboard keys), {menuselection},
  {command}, {file}. Don't use raw HTML (for example for keystrokes) when a role exists.
- Commands: use the `{terminal}` directive for command input and output, reflecting what the user
  sees on the command line.
- Code blocks: use triple backticks with a language for actual code, log files, and configuration.
  Use `{code}` or `{code-block}` only when you need extra features such as line numbers or captions.
  Inline commands and paths go in single backticks.
- Admonitions: use colon fences (`:::{note}` … `:::`), not backtick fences, and use them sparingly.
  Allowed types: `note`, `warning`, `tip`, `important`, `caution`, `seealso`, `attention`, and
  `admonition` (for a freeform title).
- Images: use Markdown syntax `![alt text](path)` where possible, and always include alternative
  text. Use the `{image}` directive only when you need extra functionality.
- Tables: use standard Markdown tables; use the `{list-table}` directive only for complex tables.
- Tabs: use the `{tab-set}` and `{tab-item}` directives.
- Reuse content with the `{include}` directive where it aids maintainability; keep each included
  snippet in its own `.txt` file.

### Versioning

- Default content applies to all supported LTS releases.
- Flag version-specific behavior with a `:::{note}` admonition.
- For larger differences, use MyST tabs ordered newest LTS first (e.g. `24.04` before `22.04`).

## When you move, rename, or delete a page

Always add a redirect, or links will break:

- Internal moves → add a line to `docs/redirects.txt`: `old/path/ new/path/`
- Redirecting to an external site → add an entry to `redirects` in `docs/conf.py`.

## Spelling exceptions

Add valid technical terms/acronyms to `docs/.custom_wordlist.txt` (alphabetically sorted)
rather than wrapping them in backticks — unless you specifically want monospaced rendering.

## Links and sources

- Prefer official upstream documentation and manpages over blog posts.
- First mention of a package or tool should link to its docs or manpage.
- Put supplementary links under a "Further reading" section at the bottom of the page.

## Scope policy

Do not perform cosmetic rewording, synonym substitution, or stylistic "polishing" of
existing prose unless the request identifies a specific clarity or accuracy problem.
The maintainers have chosen not to have LLMs polish documentation wording.

## Continuous improvement

When a session establishes a genuine, concrete improvement to how agents should work in
this repository — a clearer convention, a corrected rule, or a real loophole in this
scaffolding — proactively offer to capture it by following
`.github/prompts/capture-learnings.prompt.md`. Only offer when the change would measurably
improve performance, rule adherence, or close a genuine gap; do not suggest changes for
their own sake, and never capture anything the contributor does not want recorded.
