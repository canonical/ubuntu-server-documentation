(writing-guidance)=
# Guidance for writing

If you get stuck at all -- please don't hesitate to reach out for help!

## Files and structure

The documentation pages are all written in standard Markdown (`.md`
file types) with [MyST support](https://myst-parser.readthedocs.io/en/latest/intro.html) for more advanced elements if you want them.
All the documentation pages are in the `docs/` folder, then split into a
subfolder for the [Diátaxis](https://diataxis.fr/) section it belongs in.

The structural elements, such as landing pages, are also written in Markdown.
Each documentation page is only called once, by the landing page (or index) for that
section.

```{tip}
For example, if a page appears in the How-to section about Virtualisation,
the landing page you need will be `how-to/virtualisation.md`.
```

## Versioning policy

Ubuntu Server is relatively stable from one LTS to the next, which means the
documentation is not substantially re-written between releases. Due to this,
we opt not to have separate branches for each Ubuntu release. Instead, we call
out any changes or behaviour particular to a specific release.

### Versioning by admonition

Small, specific changes can be expressed in a "note" admonition block:

```
:::{note}
For Ubuntu 24.04 LTS (Noble) onwards, the recommended method for ...
:::
```

Any content not called out as belong to a specific release (or set of releases)
is assumed to be valid for all supported releases.

### Versioning by tabs

For large changes, where whole sets of commands may be different between
releases, we can split the instructions using tabs. 

The MyST documentation has a
[helpful demonstration](https://mystmd.org/guide/dropdowns-cards-and-tabs#tabs)
of the syntax and how tabs work.

It's good to include a "sync" keyword, so that if users are on a particular
release, they only need to choose their release one time. Default to the release
number, e.g. `24.04` or `21.10`.

In all cases, order the tabs and content from "most recent" to "oldest" release
-- this ensures that the most recent release is always shown in the left-most
tab and provides a more consistent experience.

If you would like to see an example of this in the live documentation,
{ref}`the QEMU page <qemu>` uses three tabs in the section about using 1024
vCPUs.

## Style guide

Consistency of writing style in documentation is vital for a good user
experience. In the Server Guide, we use the
[Canonical documentation style guide](https://docs.ubuntu.com/styleguide/en).

### Language

We use US English. It's a good idea to set your spellchecker to
`en-US`. We use an automated spelling checker that sometimes throws errors
about terms we would like it to ignore:

- If it complains about a file name or a command, enclose the word in backticks
  (\`) to render it as inline code.

- If the word is a valid acronym or a well-known technical term (that should
  not be rendered as code), add it to the spelling exception list,
  `.custom_wordlist.txt` (terms should be added in alphabetical order).

Both methods are valid, depending on whether you want the term to be rendered
as normal font, or as inline code (monospaced).

### Acronyms

Acronyms should always be capitalised.

They should always be expanded the first time they appear on a page, and then
can be used as acronyms after that. E.g. YAML should be shown as Yet Another
Markup Language (YAML), and then can be referred to as YAML for the rest of the
page.

All acronyms should also be in our glossary -- you can add the term to the
glossary if it is not present.

### Links

The first time you refer to a package or other product, you should make it a
link to either that product's website, or its documentation, or its manpage.

Links should be from reputable sources (such as official upstream docs). Try
not to include blog posts as references if possible.

Try to use links sparingly in the page. If you have a lot of useful references
you think the reader might be interested in, feel free to include a "Further
reading" section at the end of the page.

### Writing style

Try to be concise and to-the-point in your writing.

It's OK to be a bit light-hearted and playful in your writing, but please keep
it respectful, and don't use emoji (they don't render well in documentation).

It's also good practice not to assume that your reader will have the same
knowledge as you. If you're covering a new topic (or something complicated)
then try to briefly explain, or link to supporting explanations of, the things
the typical reader may not know, but needs to.

## Markdown elements

### Sections and headings

Avoid skipping header levels in your document structure, i.e., a level 2 header
(`##`) should be followed by a level 3 sub-header (`###`) not level 4.

```text
# Heading level 1
## Heading level 2
### Heading level 3
#### Heading level 4
```

Always include some text between headers if you can. You can see this
demonstrated between this section's heading and the one above it (Markdown
elements). It looks quite odd without text to break the headers apart!

### Semantic markup

We encourage (but do not mandate) the use of semantic mark-up where possible.
See [MyST Roles](https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html)
in the MyST documentation for an overview of inline semantic roles available
by default. The most helpful ones for this project are:

```
Keyboard keys: {kbd}`Ctrl`, {kbd}`C`
```

Rendered as {kbd}`Ctrl`, {kbd}`C`

```
Manpages: {manpage}`package-name(section)` (e.g. {manpage}`dpkg(1)`)
```

Rendered as {manpage}`dpkg(1)`

It is not necessary to provide the hardcoded URL to a manpage - they are
generated when Sphinx rebuilds the documentation so that they are always up
to date.

### Lists

For a numbered list, use `1.` in front of each item. The numbering will be
automatically rendered, so it makes it easier for you to insert new items in
the list without having to re-number them all:

```text
1. This is the first item
1. This is the second
1. This is the third
```
  
Unless a list item includes punctuation, don't end it with a full stop. If
one item in a list needs a full stop, add one to all the items in that list.

### Code blocks

Enclose a code block with three backticks:

````text
```yaml
Some code block here
```
````

Use separate command input blocks from command output blocks. We do this
because we have a "copy code" feature in the documentation, and it's more
convenient for the reader to copy the code if it only contains the input.

Avoid using a command line prompt (e.g. `$` or `#`) in an input block if
possible, and precede the output block with some kind of text that explains
what's happening. For example:
  
```bash
uname -r
```

Produces the following output:

```text
4.14.151
```

It can also be helpful to orient the reader with what they *should* be seeing
if you can include examples (although this is optional).

Use a single backtick to mark inline commands and other string literals, like
`paths/to/files`.
