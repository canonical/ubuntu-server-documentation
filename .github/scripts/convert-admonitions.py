#!/usr/bin/env python3
"""Convert backtick-fenced MyST admonitions to colon-fenced admonitions.

This script rewrites admonition directives that use backtick code fences
(for example ```` ```{note} ````) into the colon-fenced form (``:::{note}``)
that is preferred in this documentation set.

Behaviour and safety guarantees:

* Only admonition-type directives are converted (see ``ADMONITIONS``).
  Structural or literal directives such as ``{toctree}``, ``{terminal}``,
  ``{mermaid}`` and ``{include}`` are left untouched, as are ordinary
  language-tagged code blocks (```` ```bash ````, ```` ```text ````, ...).
* The fence is parsed with a small state machine that tracks nesting, so the
  matching *closing* fence of each converted admonition is rewritten too.
* The fence length is preserved: ```` ````{note} ```` becomes ``::::{note}``,
  which keeps nested code blocks valid.
* Content inside literal (non-directive) code fences is never modified, so an
  admonition example shown *inside* a code block is left as-is.

Run from the repository root:

    python3 .github/prompts/convert-admonitions.py
"""

import glob
import re

fence_re = re.compile(r'^(\s*)([`:]{3,})(.*)$')
name_re = re.compile(r'^\{([a-zA-Z0-9_-]+)\}')

# Directive names treated as admonitions and therefore converted.
ADMONITIONS = {
    'note', 'warning', 'tip', 'seealso', 'important', 'caution',
    'admonition', 'hint', 'attention', 'danger', 'error',
}

# Files to process, relative to the repository root.
GLOB_PATTERN = 'docs/**/*.md'


def directive_name(info):
    """Return the directive name in an info string, or None if there is none."""
    m = name_re.match(info.strip())
    return m.group(1) if m else None


def process(text):
    """Convert admonition fences in ``text``.

    Returns a tuple of ``(new_text, changed)``.
    """
    lines = text.split('\n')
    out = list(lines)
    stack = []  # dicts: orig_char, length, is_dir, convert
    changed = False
    for idx, line in enumerate(lines):
        m = fence_re.match(line)
        if not m:
            continue
        indent, fence, info = m.group(1), m.group(2), m.group(3)
        char = fence[0]
        length = len(fence)

        # Inside a literal (non-directive) code fence: only a matching close
        # matters; everything else is opaque content.
        if stack and not stack[-1]['is_dir']:
            top = stack[-1]
            if (char == top['orig_char'] and length >= top['length']
                    and info.strip() == ''):
                stack.pop()
            continue

        if info.strip() == '':
            # Closing-fence candidate in a parsed (directive) context.
            if (stack and stack[-1]['orig_char'] == char
                    and length >= stack[-1]['length']):
                top = stack.pop()
                if top['convert']:
                    out[idx] = indent + (':' * top['length'])
                    changed = True
            continue

        # Opening fence with an info string.
        name = directive_name(info)
        is_dir = name is not None
        convert = is_dir and char == '`' and name in ADMONITIONS
        if convert:
            out[idx] = indent + (':' * length) + info
            changed = True
        stack.append({
            'orig_char': char,
            'length': length,
            'is_dir': is_dir,
            'convert': convert,
        })

    return '\n'.join(out), changed


def main():
    total = 0
    for path in glob.glob(GLOB_PATTERN, recursive=True):
        with open(path, encoding='utf-8') as f:
            text = f.read()
        new, changed = process(text)
        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new)
            total += 1
            print(f'updated: {path}')
    print(f'\n{total} files updated')


if __name__ == '__main__':
    main()
