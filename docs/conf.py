import datetime
import os
import requests
import sys
import yaml

# Configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.

# A complete list of built-in Sphinx configuration values:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Our starter pack uses the custom Canonical Sphinx extension
# to keep all documentation based on it consistent and on brand:
# https://github.com/canonical/canonical-sphinx


# ==============================================================================
# Project information
# ==============================================================================

# Project name
project = "Ubuntu Server"
author = "Canonical Group Ltd."


# Sidebar documentation title; best kept reasonably short
# To include a version number, add it here (hardcoded or automated).
# To disable the title, set to an empty string.
html_title = project + " documentation"


# Copyright string; shown at the bottom of the page
# NOTE: For static works, it is common to provide the first publication year.
# Another option is to give the first year and current year for docs that change
# frequently e.g. 2022–2023.
#
# A way to check a repo's creation date is to get a classic GitHub token with
# "repo" permissions; see https://github.com/settings/tokens
# Next, use "curl" and "jq" to extract the date from the API's output:
#     curl -H 'Authorization: token <TOKEN>' \
#      -H 'Accept: application/vnd.github.v3.raw' \
#      https://api.github.com/repos/canonical/<REPO> | jq '.created_at'
copyright = "%s, %s" % (datetime.date.today().year, author)


# Documentation website URL
# NOTE: The Open Graph Protocol (OGP) enhances page display in a social graph
#       and is used by social media platforms; see https://ogp.me/
ogp_site_url = "https://documentation.ubuntu.com/server/"

# Preview name of the documentation website
ogp_site_name = project

# Preview image URL
ogp_image = "https://assets.ubuntu.com/v1/cc828679-docs_illustration.svg"

# Tell the Open Graph extension to use the standard HTML meta description
ogp_enable_meta_description = True

# Product favicon; shown in bookmarks, browser tabs, etc.
html_favicon = ".sphinx/_static/favicon.png"


# Dictionary of values to pass into the Sphinx context for all pages:
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context
html_context = {
    # Product page URL; can be different from product docs URL
    "product_page": "ubuntu.com/server",

    # Product tag image; the orange part of your logo, shown in the page header
    "product_tag": "_static/tag.png",

    # Your Discourse instance URL
    # NOTE: If set, adding ":discourse: 123" to an .rst file will add a link to
    # Discourse topic 123 at the bottom of the page.
    "discourse": "https://discourse.ubuntu.com/c/server/17",

    # Your Mattermost channel URL
    "mattermost": "",

    # Your Matrix channel URL
    "matrix": "https://matrix.to/#/#server:ubuntu.com",
    
    # Your documentation GitHub repository URL
    # NOTE: If set, links for viewing the docs source files and creating GitHub
    # issues are added at the bottom of each page.
    "github_url": "https://github.com/canonical/ubuntu-server-documentation/",

    # Docs branch in the repo; used in links for viewing the source files
    "repo_default_branch": "main",

    # Docs location in the repo; used in links for viewing the source files
    "repo_folder": "docs/",

    # Required for feedback button    
    "github_issues": "enabled",

    # To enable/disable the Previous/Next buttons at the bottom of pages.
    # Valid options: none, prev, next, both
    "sequential_nav": "none",

    # To enable listing contributors on individual pages, set to True
    "display_contributors": True,
}

# Project slug; see https://meta.discourse.org/t/what-is-category-slug/87897
# If your documentation is hosted on https://docs.ubuntu.com/, specify the
# project slug here.
slug = "server"


# Allow opt-in build of the OpenAPI "Hello" example so docs stay clean by default.
#if os.getenv("OPENAPI", ""):
#    tags.add("openapi")
#    html_extra_path.append("how-to/assets/openapi.yaml")


# To enable the edit button on pages, add the link to a public repository.
html_theme_options = {
    "source_edit_link": "https://github.com/canonical/ubuntu-server-documentation",
}


# By default, the documentation includes a feedback button at the top.
# You can disable it by setting the following configuration to True.
# We disable it because we have a custom feedback button with our issue template.
disable_feedback_button = True


# ==============================================================================
# Sitemap configuration: https://sphinx-sitemap.readthedocs.io/
# ==============================================================================

# Use RTD canonical URL to ensure duplicate pages have a specific canonical URL
html_baseurl = "https://documentation.ubuntu.com/server/"

# URL scheme. Add language and version scheme elements.
sitemap_url_scheme = "{link}"

# Include `lastmod` dates in the sitemap:
sitemap_show_lastmod = True

# Exclude generated pages from the sitemap:
sitemap_excludes = [
    "404/",
    "genindex/",
    "search/",
]

# NOTE: Add more pages to sitemap_excludes if needed. Wildcards are supported.
# For example, to exclude module pages generated by autodoc, add "_modules/*".


# ==============================================================================
# Template and asset locations
# ==============================================================================

html_static_path = [".sphinx/_static/"]

templates_path = [".sphinx/_templates/"]

#html_extra_path = []

# Add custom CSS files (located under "html_static_path")
html_css_files = [
    "css/cookie-banner.css",
    "css/custom.css",
    "css/footer.css",
    "css/furo_colors.css",
    "css/github_issue_links.css",
    "css/header.css",
]

# Add custom JavaScript files (located under "html_static_path")
html_js_files = [
    "js/footer.js",
    "js/header-nav.js",
    "js/github_issue_links.js",
    "js/bundle.js",
    "js/hoverxref-dark-mode.js",
]

source_suffix = {
#    ".rst": "restructuredtext",
    ".md": "markdown",
}


# ==============================================================================
# Redirects
# ==============================================================================

# To set up redirects to external projects:
# https://documatt.gitlab.io/sphinx-reredirects/usage.html
# For example: "explanation/old-name.html": "../how-to/prettify.html",

# NOTE: If undefined, set to None, or empty, the sphinx_reredirects extension
# will be disabled.
redirects = {
    "how-to/containers/lxc-containers": "https://linuxcontainers.org/lxc/documentation/",
    "reference/backups/basic-backup-shell-script": "https://discourse.ubuntu.com/t/basic-backup-shell-script/36419"
}

# To set up internal redirects when a page has moved or been renamed, use
# the redirects.txt file
rediraffe_branch = "main"
rediraffe_redirects = "redirects.txt"


# ==============================================================================
# Link checker exceptions
# ==============================================================================

# A regex list of URLs that are ignored by "make linkcheck"
linkcheck_ignore = [
    "http://127.0.0.1:8000",
    "https://manpages.ubuntu.com/*",
    "https://calendar.google.com/*",
    "http://localhost:3000",
    "http://prometheus:9090",
    "http://dnssec-failed.org",
    "https://dev.mysql.com/*",
    "https://en.wikipedia.org/*",
    "https://en.wikibooks.org/",
    "https://matrix.to/#/*",
    "https://linux.die.net/*",
    "https://www.mysql.com/*",
    "https://www.youtube.com/*",
    "https://www.icann.org/*",
    "https://www.java.com/*",
    "https://wiki.samba.org/*",
    "https://github.com/*",
    "https://gitlab.com/*",
    "https://www.samba.org/*",
    "https://www.freedesktop.org/*",
    "https://community.openvpn.net/*",
    "https://openvpn.net/*",
    "https://krbdev.mit.edu/*",
    "https://www.cyberciti.biz/*",
    "https://nfs.sourceforge.net/*",
    "https://sourceforge.net/*",
    "https://ubuntu.com/blog/*",
    "https://help.ubuntu.com/*",
    "https://git.launchpad.net/*",
    "https://linuxcontainers.org/*",
    "https://wiki.syslinux.org/*",
    # Rate-limited domains that cause delays
    r"http://www\.gnu\.org/software/.*",
    r"https://github\.com/.*/blob/.*",
]

# A regex list of URLs where anchors are ignored by "make linkcheck"
linkcheck_anchors_ignore_for_url = [r"https://github\.com/.*"]

# Give linkcheck multiple tries on failure
linkcheck_timeout = 15
linkcheck_retries = 2

# Number of parallel workers for linkcheck (default is 5)
# Higher values work well for network I/O-bound tasks
linkcheck_workers = 20


# ==============================================================================
# Manpages auto-linking
# ==============================================================================

# To enable manpage links, uncomment and replace {codename} with required
# release, preferably an LTS release (e.g. noble). Do *not* substitute
# {section} or {page}; these will be replaced by sphinx at build time.

# NOTE: If set, adding "{manpage}" to an .md file adds a link to the
# corresponding man section at the bottom of the page.

stable_distro = "resolute"

manpages_url = (
    "https://manpages.ubuntu.com/manpages/"
    + stable_distro
    + "/en/man{section}/{page}.{section}.html"
)


# ==============================================================================
# MyST configuration extras
# ==============================================================================

# Custom Sphinx extensions; see
# https://www.sphinx-doc.org/en/master/usage/extensions/index.html

# Custom MyST syntax extensions; see
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html

# NOTE: By default, the following MyST extensions are enabled:
# - substitution
# - deflist
# - linkify
myst_enable_extensions = {
    "colon_fence",
    "dollarmath",
    "tasklist",
    "fieldlist",
    "substitution",
    "html_admonition",
}


# NOTE: The canonical_sphinx extension is required for the starter pack.
# It automatically enables the following extensions:
# - custom-rst-roles
# - myst_parser
# - notfound.extension
# - related-links
# - sphinx_copybutton
# - sphinx_design
# - sphinx_reredirects
# - sphinx_tabs.tabs
# - sphinxcontrib.jquery
# - sphinxext.opengraph
# - terminal-output
# - youtube-links

extensions = [
# Included in the Starter Pack
# ----------------------------
    "canonical_sphinx", # REQUIRED for the Starter Pack
    "notfound.extension",
    "sphinx_design",
    "sphinx_reredirects",
#    "sphinx_tabs.tabs",
    "sphinxcontrib.jquery",
    "sphinxext.opengraph",
    "sphinx_config_options",
    "sphinx_contributor_listing",
    "sphinx_filtered_toctree",
    "sphinx_related_links",
    "sphinx_roles",
#    "sphinx_terminal",
    "sphinx_ubuntu_images",
#    "sphinx_youtube_links",
    "sphinxcontrib.cairosvgconverter",
    "sphinx_last_updated_by_git",
    "sphinx.ext.intersphinx",
    "sphinx_sitemap",
# Custom extensions in this project
# ---------------------------------
    "myst_parser",
    "sphinx.ext.extlinks",
    "hoverxref.extension",
    "sphinxext.rediraffe",
    "sphinxcontrib.mermaid",
    "sphinx_copybutton",
]


myst_heading_anchors = 3


# Suppress specific warnings
suppress_warnings = [
    'myst.glossary',  # Suppress glossary-related warnings from MyST parser
]


# Configure hoverxref options
hoverxref_role_types = {
    "term": "tooltip",
}
hoverxref_roles = ["term",]


# Allow for use of link substitutions
extlinks = {
    "lpsrc": ("https://launchpad.net/ubuntu/+source/%s", "%s"),
    "lpbug": ("https://bugs.launchpad.net/bugs/%s", "LP: #%s"),
    "matrix": ("https://matrix.to/#/#%s:ubuntu.com", "#%s:ubuntu.com"),
}


# Excludes files or directories from processing
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".sphinx",
    "cheatsheets/",
    "doc-templates/*",
    "doc-cheat-sheet*",
    "readme.md",
    "legacy/*.md",
    ".github/*.md",
]


# Add tags that you want to use for conditional inclusion of text
# (https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#tags)
custom_tags = []


# Workaround for https://github.com/canonical/canonical-sphinx/issues/34
if "discourse_prefix" not in html_context and "discourse" in html_context:
    html_context["discourse_prefix"] = html_context["discourse"] + "/t/"

# Workaround for substitutions.yaml
if os.path.exists("./reuse/substitutions.yaml"):
    with open("./reuse/substitutions.yaml", "r") as fd:
        myst_substitutions = yaml.safe_load(fd.read())

# Add configuration for intersphinx mapping
intersphinx_mapping = {
    "starter-pack": ("https://canonical-example-product-documentation.readthedocs-hosted.com/en/latest", None),
    "sphinxcontrib-mermaid": ("https://sphinxcontrib-mermaid-demo.readthedocs.io/en/latest", None)
}
