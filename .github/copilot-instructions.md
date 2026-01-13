# Ubuntu Server Documentation - Copilot Instructions

## Project Overview

This is the **Ubuntu Server documentation** - a Sphinx-based documentation project using the [Canonical Sphinx Docs Starter Pack](https://github.com/canonical/sphinx-docs-starter-pack). Documentation targets the latest Ubuntu LTS release, calling out version-specific differences when they exist.

## Architecture & Structure

### Diátaxis Framework

Content is organized using the [Diátaxis framework](https://diataxis.fr/):
- `tutorial/` - Getting started guides (e.g., `basic-installation.md`)
- `how-to/` - Task-oriented guides organized by topic (installation, security, networking, virtualisation, etc.)
- `explanation/` - Conceptual overviews and background information
- `reference/` - Technical specifications, glossaries, system requirements
- `contributing/` - Contributor documentation

### File Types

- **Markdown (`.md`)** - Primary format for content pages with MyST syntax support
- **reStructuredText (`.rst`)** - Landing pages, index files, and structural elements
- Mixed content: Both formats coexist and are processed by Sphinx

### Key Configuration Files

- `conf.py` - Project-specific settings (edit here for customization)
- `Makefile` / `Makefile.sp` - Build system (starter pack targets prefixed with `sp-`)
- `.readthedocs.yaml` - Read the Docs build configuration

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

For remote/VM development, set `export SPHINX_HOST=0.0.0.0` before running `make run`.

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
- Add technical terms to `reference/glossary.rst` and spell exceptions to `.custom_wordlist.txt`

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
- Order tabs from **newest to oldest** release

### Cross-References

- Use reference labels in `.rst` files: `.. _my-label:`
- Link with `:ref:\`my-label\``
- First mentions of packages/tools should link to official docs or manpages
- Use semantic markup: `{kbd}\`Ctrl\``, `{manpage}\`dpkg(1)\``, `{term}\`DAC\``
- Manpage links auto-generate URLs (no hardcoding needed)

### Markdown Elements

- **Headings**: Use proper hierarchy (`#`, `##`, `###`, `####`); don't skip levels
- **Lists**: Use `1.` for all numbered items (auto-renumbers)
- **Code blocks**: Specify language for syntax highlighting
- **MyST extensions**: `colon_fence`, `deflist`, `linkify`, `substitution`

### File Structure

- Content pages only referenced once (via their section's landing page)
- Landing pages in `how-to/`, `tutorial/`, etc. organize navigation
- Images stored in `<section>/images/` directories
- Shared links defined in `reuse/links.txt` and auto-included via `rst_epilog`

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
3. Add to corresponding `index.rst` or section landing page
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
