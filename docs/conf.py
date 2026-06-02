import datetime
import os
import textwrap
import requests
import sys
import yaml

"""
Configuration for the Sphinx documentation builder.
All configuration specific to your project should be done in this file.

A complete list of built-in Sphinx configuration values:
https://www.sphinx-doc.org/en/master/usage/configuration.html

The Sphinx Stack uses the Canonical Sphinx theme to keep all documentation consistent and on brand: https://github.com/canonical/canonical-sphinx
"""

# ==============================================================================
# Project information
# ==============================================================================

# Project name
project = "Ubuntu Server"

# Author name; used in the default copyright statement in the page footer
author = "Canonical Ltd."

# The year in the copyright statement
copyright = f"{datetime.date.today().year}"

# Sidebar documentation title
# To disable the title, set it to an empty string.
html_title = project + " documentation"

# Documentation website URL
ogp_site_url = "https://ubuntu.com/server/docs/"

# Preview name of the documentation website
ogp_site_name = project

# Preview image URL
ogp_image = "https://assets.ubuntu.com/v1/cc828679-docs_illustration.svg"

# Tell the Open Graph extension to use the standard HTML meta description
ogp_enable_meta_description = True

# Product favicon; shown in bookmarks, browser tabs, etc.
# html_favicon = ".sphinx/_static/favicon.png"

# Dictionary of values to pass into the Sphinx context for all pages:
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context
html_context = {
    # Product page URL; can be different from product docs URL
    "product_page": "ubuntu.com/server",

    # Product tag image; the orange part of your logo, shown in the page header
    # "product_tag": "_static/tag.png",

    # Your Discourse instance URL
    "discourse": "https://discourse.ubuntu.com/c/server/17",

    # Your Mattermost channel URL
    #"mattermost": "",

    # Your Matrix channel URL
    "matrix": "https://matrix.to/#/#server:ubuntu.com",
    
    # Your documentation GitHub repository URL
    # If set, links for viewing the docs source files and creating GitHub issues are added at the bottom of each page.
    "github_url": "https://github.com/canonical/ubuntu-server-documentation/",

    # Docs branch in the repo; used in links for viewing the source files
    "repo_default_branch": "main",

    # Docs location in the repo; used in links for viewing the source files
    "repo_folder": "docs/",

    # To enable/disable the Previous/Next buttons at the bottom of pages.
    # Valid options: none, prev, next, both
    "sequential_nav": "none",

    # To enable listing contributors on individual pages, set to True
    "display_contributors": True,

    # Required for feedback button    
    "github_issues": "enabled",

    # Passes the top-level 'author' value to the theme
    "author": author,

    # Documentation license information
    "license": {
        # TODO: Specify your project's license.
        # For the name, we recommend using the standard shorthand identifier from
        # https://spdx.org/licenses
        "name": "",
        # TODO: Link directly to your project's license statement.
        "url": "",
    },

    # Links for the "Ubuntu docs" dropdown in the site header
    "ubuntu_docs": [
        {"title": "Ubuntu release notes",  "url": "https://documentation.ubuntu.com/release-notes/"},
        {"title": "Ubuntu security",       "url": "https://documentation.ubuntu.com/security/"},
        {"title": "Ubuntu Desktop",        "url": "https://documentation.ubuntu.com/desktop/"},
        # {"title": "Ubuntu Server",         "url": "https://ubuntu.com/server/docs/"},
        {"title": "Ubuntu on WSL",         "url": "https://documentation.ubuntu.com/wsl/latest/"},
        {"title": "Ubuntu for developers", "url": "https://documentation.ubuntu.com/ubuntu-for-developers/"},
        {"title": "Ubuntu project",        "url": "https://documentation.ubuntu.com/project/"},
        {"title": "Ubuntu Pro",            "url": "https://documentation.ubuntu.com/pro/"},
    ],
}


# TODO: To enable the edit button on pages, uncomment and change the link to a
# public repository on GitHub or Launchpad. Any of the following link domains
# are accepted:
# - https://github.com/example-org/example"
# - https://launchpad.net/example
# - https://git.launchpad.net/example
html_theme_options = {
    "source_edit_link": "https://github.com/canonical/ubuntu-server-documentation",
}


# Project slug
# If your documentation is hosted on https://docs.ubuntu.com/, specify the project slug here.
slug = "server/docs"

# By default, the documentation includes a feedback button at the top. 
# We disable it because we have a custom feedback button that works with our issue template.
disable_feedback_button = True


# ==============================================================================
# Sitemap configuration: https://sphinx-sitemap.readthedocs.io/
# ==============================================================================

# Use RTD canonical URL to ensure duplicate pages have a specific canonical URL
html_baseurl = "https://ubuntu.com/server/docs/"

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

sitemap_filename = "doc-sitemap.xml"

# NOTE: Add more pages to sitemap_excludes if needed. Wildcards are supported.
# For example, to exclude module pages generated by autodoc, add "_modules/*".


# ==============================================================================
# Template and asset locations
# ==============================================================================

html_static_path = ["_static"]

templates_path = ["_templates"]

# ==============================================================================
# Redirects
# ==============================================================================

# To set up redirects to external projects:
# https://documatt.gitlab.io/sphinx-reredirects/usage.html
# For example: "explanation/old-name.html": "../how-to/prettify.html",

# NOTE: If undefined, set to None, or empty, the sphinx_reredirects extension will be disabled.
redirects = {
    "how-to/containers/lxc-containers": "https://linuxcontainers.org/lxc/documentation/",
    "reference/backups/basic-backup-shell-script": "https://discourse.ubuntu.com/t/basic-backup-shell-script/36419"
}

# To set up internal redirects when a page has moved or been renamed, use the redirects.txt file
rediraffe_branch = "main"
rediraffe_redirects = "redirects.txt"

# Strips '/index.html' from destination URLs when building with 'dirhtml'
rediraffe_dir_only = True


# ==============================================================================
# sphinx-llm configuration
# ==============================================================================

# This description is included in llms.txt to provide some initial context for your docs.
# TODO: Add a description in the form "This is the documentation for <product name>,
# <first sentence of home page>".
llms_txt_description = textwrap.dedent(
    """\
    This is the official documentation for Ubuntu Server, a version of the Ubuntu operating system designed and engineered as a backbone for the internet.
    """
)

# The base URL for references built by sphinx-markdown-builder.
if os.environ.get("READTHEDOCS"):
    markdown_http_base = html_baseurl

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
    "https://www.openstack.org/*",
    "https://web.archive.org/web/20241130024605/http://networktimesecurity.org/",
    "https://www.intel.com/*",
    "https://www.packtpub.com/*",
    "https://www.redbooks.ibm.com/*",
    "http://www.gnu.org/software/*",
    "https://github.com./*",
    "https://ubuntu.com/*",
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
    + "/man{section}/{page}.{section}.html"
)


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

# Custom Sphinx extensions; see
# https://www.sphinx-doc.org/en/master/usage/extensions/index.html

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
    "sphinx_llm.txt",
    "sphinx_related_links",
    "sphinx_roles",
    "sphinx_terminal",
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
    ".venv",
]

myst_heading_anchors = 3

#html_extra_path = []

# Adds custom CSS files, located remotely or in 'html_static_path'.
html_css_files = [
    "css/cookie-banner.css",
    "css/custom.css",
    "css/footer.css",
    "css/furo_colors.css",
    "css/github_issue_links.css",
    "css/header.css",
]

# Adds custom JavaScript files, located remotely or in 'html_static_path'.
html_js_files = [
    "js/footer.js",
    "js/github_issue_links.js",
    "js/bundle.js",
    "js/url_overwrite.js",
]

source_suffix = {
    ".md": "markdown",
}
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

# Override canonical_sphinx extension defaults
# The canonical_sphinx extension sets html_copy_source = False by default.
# We need to enable it for "View page source" links to work.
html_copy_source = True
html_show_sourcelink = True


# Force html_copy_source to be True after all extensions have loaded
def force_copy_source(app, config):
    """Override canonical_sphinx's html_copy_source setting."""
    config.html_copy_source = True
    config.html_show_sourcelink = True

def setup(app):
    """Custom setup to ensure source files are copied."""
    app.connect('config-inited', force_copy_source)
