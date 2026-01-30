# Ubuntu Server Documentation – Copilot Instructions

## Project Overview

This is the **Ubuntu Server documentation** – a Sphinx-based documentation project using the [Canonical Sphinx Docs Starter Pack](https://github.com/canonical/sphinx-docs-starter-pack). Documentation targets the latest Ubuntu LTS release, calling out version-specific differences when they exist.

## Architecture & Structure

### Diátaxis Framework

Content is organized using the [Diátaxis framework](https://diataxis.fr/):
- Tutorials (`tutorial/`) – Getting started guides (e.g., `basic-installation.md`)
- How-to Guides (`how-to/`) – Task-oriented guides organized by topic (installation, security, networking, virtualisation, etc.)
- Explanations (`explanation/`) – Conceptual overviews and background information
- Reference (`reference/`) – Technical specifications, glossaries, system requirements
- `contributing/` – Contributor documentation

### File Types

- **Markdown (`.md`)** – Primary format for content pages with MyST syntax support

### Key Configuration Files

- `conf.py` – Project-specific settings (edit here for customization)
- `Makefile` – Build system
- `.readthedocs.yaml` – Read the Docs build configuration

## Development Workflow

### Local Setup

```bash
git clone git@github.com:canonical/ubuntu-server-documentation.git
cd ubuntu-server-documentation
sudo apt update
sudo apt install make python3 python3-venv python3-pip
make install
```

### Build & Preview

```bash
make run          # Build, watch, and serve at http://127.0.0.1:8000
make html         # Build only
make serve        # Serve only
make clean-doc    # Clean built files
```

### Testing & Quality Checks

```bash
make spelling     # Spell check (uses .custom_wordlist.txt for exceptions)
make linkcheck    # Verify all links
make woke         # Check inclusive language
make pa11y        # Accessibility testing
```

Always run `make spelling` and `make linkcheck` before submitting PRs.

## Writing Conventions

### Style & Language

- Follow the [Canonical documentation style guide](https://docs.ubuntu.com/styleguide/en)
- Use **US English** (`en-US`)
- Acronyms: Expand on first use, e.g., "Yet Another Markup Language (YAML)"
- Add technical terms to `reference/glossary.rst` and spelling exceptions to `.custom_wordlist.txt`

### Versioning Strategy

This project does **not** use separate branches per Ubuntu release. Instead:
- Default content applies to all supported LTS releases
- Version-specific content uses **note admonitions**:
  ```markdown
  :::{note}
  For Ubuntu 24.04 LTS (Noble) onwards, use the new method...
  :::
  ```
- Major version differences use **MyST tabs** with sync keywords (e.g., `24.04`, `22.04`)
- Order tabs from **newest to oldest** Ubuntu release

### Cross-References

- Use reference labels in `.md` files: `(slug-name)=`
- Link with `{ref}`my-label``
- First mentions of packages/tools should link to official docs or manpages
- Use semantic markup: `{kbd}`Ctrl``, `{manpage}`dpkg(1)``, `{term}`DAC``
- Manpage links auto-generate URLs (no hardcoding needed)

### Markdown Elements

- **Headings**: Use proper hierarchy (`#`, `##`, `###`, `####`); don't skip levels
- **Lists**: Use `1.` for all numbered items (auto-renumbers)
- **Code blocks**: Specify language for syntax highlighting
- **MyST extensions**: `colon_fence`, `deflist`, `linkify`, `substitution`

### Sphinx Roles & Semantic Markup

Every technical entity must use a specific MyST role:
- **Keyboard keys:** Must use {kbd}`Key` (e.g., {kbd}`Enter`).
- **Command-line tools:** Use {manpage}`tool(section)` for the first mention (e.g., {manpage}`ls(1)`).
- **Glossary terms:** Use {term}`term` for items defined in the glossary.
- **Internal Links:** Use {ref}`label-name` instead of standard markdown links for internal cross-references.

## Critical Patterns

### Redirects

When renaming/moving/deleting files, **always add redirects**:

**Internal redirects** (in `redirects.txt`):
```
old/path/to/file/ new/path/to/file/
```

**External redirects** (in `conf.py` under `redirects = {}`):
```python
redirects = {
    "how-to/containers/lxc-containers": "https://linuxcontainers.org/lxc/documentation/"
}
```

### Custom Wordlist

Add valid technical terms/acronyms to `.custom_wordlist.txt` (alphabetically sorted) rather than wrapping in backticks, unless you want monospaced rendering.

### PR Requirements

- Link PRs to issues with `Fixes #<issue-number>` in description
- Use [Conventional Comments](https://conventionalcomments.org/) for feedback
- Include manual testing for code/commands
- Preview builds available via Read the Docs check on PR

## Common Tasks

### Adding New Content

1. Determine Diátaxis category (tutorial/how-to/explanation/reference)
2. Create `.md` file in appropriate subdirectory
3. Add to corresponding `index.md` or section landing page
4. Use reference labels: `(my-label)=` at top of Markdown files
5. Test: `make run` and verify navigation

### Updating Links

- Prefer reputable sources (official upstream docs, not blog posts)
- Use "Further reading" sections for supplementary links
- First package mention should link to docs/manpages

### Handling Errors

- **Spelling errors**: Add to `.custom_wordlist.txt` or wrap in backticks
- **Link errors**: Check `linkcheck_ignore` in `conf.py`
- **Build errors**: Check `.sphinx/venv/pip_install.log` for dependency issues

## Don't Do This

- Don't use emojis in documentation
- Don't skip heading levels in document structure
- Don't assume reader knowledge without explanation/links
- Don't link to blog posts when official docs exist
- Don't create version branches (use in-page version callouts)

### Language & Quality Standards
Flag the following "obvious" language errors that degrade documentation quality:

#### 1. Prohibited "Filler" Words
Flag any use of "weak" or "subjective" adverbs that diminish technical authority:
* "simply", "just", "easy/easily", "actually", "basically", "obviously".
* Example: "Just run this command" should be changed to "Run this command".

#### 2. Voice and Perspective
* **Active Voice:** Flag passive phrasing. Change "The package is installed" to "Install the package".
* **Person:** Use second person ("You"). "We" can be used in tutorials.
* **Descriptive Links:** Flag links like "click here" or "see this page". Link text must describe the destination (e.g., "See the [Installation Guide](link)").

#### 3. Technical Consistency
* **US English:** Ensure US spelling (e.g., "initialize" not "initialise", "color" not "colour").
* **Acronyms:** Flag any acronym used for the first time that isn't expanded, e.g., "Advanced Package Tool (APT)".
* **Placeholders:** Ensure command-line placeholders are clear (e.g., `<ip_address>` or `<username>`).

### Repository Integrity
* **Redirects:** If the PR modifies a filename, flag it if a corresponding entry is missing from `redirects.txt`.
* **Wordlist:** If a technical term is flagged as a typo but is correct, suggest adding it to `.custom_wordlist.txt`.
* **Lists:** Ensure all numbered lists use `1.` for every item (allowing for auto-numbering).

---

## Copilot Documentation Review Guidance

To improve Copilot's effectiveness as a documentation reviewer, follow the additional rules below (drawn from common PR feedback and Canonical team practices):

### Clarity and Precision
- **Only accept word/phrase changes that clearly improve clarity, precision, or accuracy.** Reject or flag synonym substitutions and rewording that offer no tangible improvement or are for personal preference only.
- **Prefer active voice over passive.** Avoid changes that introduce passive language unless necessary. Flag uses of the passive that can be rewritten in active voice, especially in procedures or explanations.

### Policy Accuracy
- **Factual correctness and project policy:** Do not introduce or approve statements that inaccurately represent Ubuntu’s support policies, such as implying 3rd-party/unsupported software is supported.
- **Focus on supported LTS versions.** When discussing features or changes, prioritize LTS releases unless context requires otherwise, and flag references to unsupported or obsolete releases.

### Conciseness and Redundancy
- **Promote concise, focused writing.** Where redundancy or repetition is found, suggest merging or streamlining for clarity and snappiness.

### Formatting, Sphinx, and Style Enforcement
- **Trim unnecessary whitespace.** Remove trailing spaces and excess blank lines, and enforce correct indentation in lists/code blocks as per Sphinx/MyST parser requirements.
- **Glossary/term references:** Use `{term}` syntax only for glossary terms that exist. Remove or comment on `{term}` tags referencing nonexistent entries, recommending their addition as follow-up work if beneficial.
- **Version/tab ordering:** Ensure MyST tab sets and similar versioned structures always list from the newest LTS at left/top to oldest right/bottom, following Ubuntu documentation conventions.

### Technical and Content Accuracy
- **Validate all code and configuration snippets for syntax accuracy.** For example, Netplan YAML must match formatting as found in the official documentation.
- **Check links and cross-references:** Flag any broken (404) or invalid links, both internal and external, and ensure references to in-repo docs resolve and point correctly.

### Review Rationale, Collaboration, and Tone
- **Provide rationale for each suggestion.** Always explain _why_ changes are recommended, with reference to project style or best practices.
- **Distinguish between required and optional suggestions.** When subjective or stylistic, clarify that suggestions are non-blocking and the contributor may choose whether or not to adopt them.

### Integrate With Existing PR Feedback
These reviewer guidelines are based on active review and feedback patterns in this repository. Review previous PRs and discussion threads for style and decision precedents.

---

By following these instructions, Copilot can serve as a more effective and context-aware reviewer, delivering feedback that aligns with Ubuntu Server Documentation’s technical, stylistic, and collaborative standards.
