import datetime

# Custom configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.
#
# The file is included in the common conf.py configuration file.
# You can modify any of the settings below or add any configuration that
# is not covered by the common conf.py file.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# If you're not familiar with Sphinx and don't want to use advanced
# features, it is sufficient to update the settings in the "Project
# information" section.

############################################################
### Project information
############################################################

# Product name
project = 'Ubuntu Server'
author = 'Canonical Group Ltd'

# The title you want to display for the documentation in the sidebar.
# You might want to include a version number here.
# To not display any title, set this option to an empty string.
html_title = project + ' documentation'

# The default value uses the current year as the copyright year.
#
# For static works, it is common to provide the year of first publication.
# Another option is to give the first year and the current year
# for documentation that is often changed, e.g. 2022–2023 (note the en-dash).
#
# A way to check a GitHub repo's creation date is to obtain a classic GitHub
# token with 'repo' permissions here: https://github.com/settings/tokens
# Next, use 'curl' and 'jq' to extract the date from the GitHub API's output:
#
# curl -H 'Authorization: token <TOKEN>' \
#   -H 'Accept: application/vnd.github.v3.raw' \
#   https://api.github.com/repos/canonical/<REPO> | jq '.created_at'

copyright = '%s, %s' % (datetime.date.today().year, author)

## Open Graph configuration - defines what is displayed as a link preview
## when linking to the documentation from another website (see https://ogp.me/)
# The URL where the documentation will be hosted (leave empty if you
# don't know yet)
# NOTE: If no ogp_* variable is defined (e.g. if you remove this section) the
# sphinxext.opengraph extension will be disabled.
ogp_site_url = 'https://documentation.ubuntu.com/server/'
# The documentation website name (usually the same as the product name)
ogp_site_name = project
# The URL of an image or logo that is used in the preview
ogp_image = 'https://assets.ubuntu.com/v1/253da317-image-document-ubuntudocs.svg'

# Update with the local path to the favicon for your product
# (default is the circle of friends)
html_favicon = '.sphinx/_static/favicon.png'

# (Some settings must be part of the html_context dictionary, while others
#  are on root level. Don't move the settings.)
html_context = {

    # Change to the link to the website of your product (without "https://")
    # For example: "ubuntu.com/lxd" or "microcloud.is"
    # If there is no product website, edit the header template to remove the
    # link (see the readme for instructions).
    'product_page': 'ubuntu.com/server',

    # Add your product tag (the orange part of your logo, will be used in the
    # header) to ".sphinx/_static" and change the path here (start with "_static")
    # (default is the circle of friends)
    'product_tag': '_static/tag.png',

    # Change to the discourse instance you want to be able to link to
    # using the :discourse: metadata at the top of a file
    # (use an empty value if you don't want to link)
    'discourse': 'https://discourse.ubuntu.com/c/server/17',

    # Change to the Mattermost channel you want to link to
    # (use an empty value if you don't want to link)
    'mattermost': 'https://chat.canonical.com/canonical/channels/server',

    # Change to the Matrix channel you want to link to
    # (use an empty value if you don't want to link)
    'IRC': 'https://kiwiirc.com/nextclient/irc.libera.chat/ubuntu-server',

    # Change to the GitHub URL for your project
    # This is used, for example, to link to the source files and allow creating GitHub issues directly from the documentation.
    'github_url': 'https://github.com/canonical/ubuntu-server-documentation',

    # Change to the branch for this version of the documentation
    'github_version': 'main',

    # Change to the folder that contains the documentation
    # (usually "/" or "/docs/")
    'github_folder': '/',

    # Change to an empty value if your GitHub repo doesn't have issues enabled.
    # This will disable the feedback button and the issue link in the footer.
    'github_issues': 'enabled',

    # Controls the existence of Previous / Next buttons at the bottom of pages
    # Valid options: none, prev, next, both
    'sequential_nav': "none", 
    
    # Controls if to display the contributors of a file or not
    "display_contributors": True,
    
    # Controls time frame for showing the contributors
    "display_contributors_since": ""
}

# If your project is on documentation.ubuntu.com, specify the project
# slug (for example, "lxd") here.
slug = "server"

############################################################
### Redirects
############################################################

# Set up redirects (https://documatt.gitlab.io/sphinx-reredirects/usage.html)
# For example: 'explanation/old-name.html': '../how-to/prettify.html',
# You can also configure redirects in the Read the Docs project dashboard
# (see https://docs.readthedocs.io/en/stable/guides/redirects.html).
# NOTE: If this variable is not defined, set to None, or the dictionary is empty,
# the sphinx_reredirects extension will be disabled.
redirects = {
    "how-to/containers/lxc-containers": "https://linuxcontainers.org/lxc/documentation/",
    "reference/backups/basic-backup-shell-script": "https://discourse.ubuntu.com/t/basic-backup-shell-script/36419"
}

############################################################
### Link checker exceptions
############################################################

# Links to ignore when checking links
linkcheck_ignore = [
    'http://127.0.0.1:8000'
    'https://manpages.ubuntu.com'
    ]

# Pages on which to ignore anchors
# (This list will be appended to linkcheck_anchors_ignore_for_url)
custom_linkcheck_anchors_ignore_for_url = []

############################################################
### Manpages auto-linking
############################################################

# To enable manpage links, uncomment and replace {codename} with required
# release, preferably an LTS release (e.g. noble). Do *not* substitute
# {section} or {page}; these will be replaced by sphinx at build time
#
# NOTE: If set, adding '{manpage}' to an .md file adds a link to the
# corresponding man section at the bottom of the page.
#
# manpages_url = 'https://manpages.ubuntu.com/manpages/{codename}/en/' + \
#     'man{section}/{page}.{section}.html'

stable_distro = "plucky"

manpages_url = (
    "https://manpages.ubuntu.com/manpages/"
    + stable_distro
    + "/en/man{section}/{page}.{section}.html"
)



############################################################
### Additions to default configuration
############################################################

# Uncomment to overwrite Ubuntu manpages URL template for :manpage: directives:
# custom_manpages_url = "https://customurl/man{section}/{page}.{section}.html"

## The following settings are appended to the default configuration.
## Use them to extend the default functionality.
# NOTE: Remove this variable to disable the MyST parser extensions.
custom_myst_extensions = ["colon_fence"]

myst_heading_anchors = 3

# Add custom Sphinx extensions as needed.
# This array contains recommended extensions that should be used.
# NOTE: The following extensions are handled automatically and do
# not need to be added here: myst_parser, sphinx_copybutton, sphinx_design,
# sphinx_reredirects, sphinxcontrib.jquery, sphinxext.opengraph
custom_extensions = [
#    'sphinx_tabs.tabs',
    'myst_parser',
    'sphinxcontrib.jquery',
    'sphinxcontrib.mermaid',
    'sphinxext.rediraffe',
    'hoverxref.extension',
    'sphinx_sitemap',
#    'canonical.youtube-links',
#    'canonical.related-links',
#    'canonical.custom-rst-roles',
#    'canonical.terminal-output',
#    'notfound.extension'
]

# Add custom required Python modules that must be added to the
# .sphinx/requirements.txt file.
# NOTE: The following modules are handled automatically and do not need to be
# added here: canonical-sphinx-extensions, furo, linkify-it-py, myst-parser,
# pyspelling, sphinx, sphinx-autobuild, sphinx-copybutton, sphinx-design,
# sphinx-notfound-page, sphinx-reredirects, sphinx-tabs, sphinxcontrib-jquery,
# sphinxext-opengraph
custom_required_modules = [
    'sphinxcontrib-mermaid',
    'sphinxext-rediraffe',
    'sphinx-hoverxref',
    'sphinx-sitemap',
    'distro_info',
]

# Configure hoverxref options
hoverxref_role_types = {
    'term': 'tooltip',
}
hoverxref_roles = ['term',]

# Add redirects, so they can be updated here to land with docs being moved
rediraffe_branch = "main"
rediraffe_redirects = "redirects.txt"

# Add files or directories that should be excluded from processing.
custom_excludes = [
    'cheatsheets/',
    'doc-templates/*',
    'doc-cheat-sheet*',
    'readme.rst',
    'legacy/*.md',
    '.github/pull_request_template.md',
]

# Allow Sphinx to use both rst and md
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Add CSS files (located in .sphinx/_static/)
custom_html_css_files = [
    'cookie-banner.css'
]

# Add JavaScript files (located in .sphinx/_static/)
custom_html_js_files = [
    'js/bundle.js',
]

## The following settings override the default configuration.

# Specify a reST string that is included at the end of each file.
# If commented out, use the default (which pulls the reuse/links.txt
# file into each reST file).
# custom_rst_epilog = ''

# By default, the documentation includes a feedback button at the top.
# You can disable it by setting the following configuration to True.
disable_feedback_button = False

# Add tags that you want to use for conditional inclusion of text
# (https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#tags)
custom_tags = []

############################################################
### Additional configuration
############################################################

## Add any configuration that is not covered by the common conf.py file.

# Define a :center: role that can be used to center the content of table cells.
#rst_prolog = '''
#.. role:: center
#   :class: align-center
#'''

suppress_warnings = ['orphan']

## Sitemap configuration

html_baseurl = 'https://documentation.ubuntu.com/server/'
sitemap_url_scheme = "{link}"

############################################################
### PDF configuration
############################################################

pdf_subtitle = ''

latex_engine = 'xelatex'
# This whole thing is a hack and a half, but it works.
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'fncychap': '',
    'preamble': r'''
%\usepackage{charter}
%\usepackage[defaultsans]{lato}
%\usepackage{inconsolata}
\setmainfont[Path = ../../.sphinx/fonts/, UprightFont = *-R, BoldFont = *-B, ItalicFont=*-RI]{Ubuntu}
\setmonofont[Path = ../../.sphinx/fonts/, UprightFont = *-R]{UbuntuMono}
\usepackage[most]{tcolorbox}
\tcbuselibrary{breakable}
\usepackage{lastpage}
\usepackage{tabto}
\usepackage{ifthen}
\usepackage{etoolbox}
\usepackage{fancyhdr}
\usepackage{graphicx}
\usepackage{titlesec}
\usepackage{fontspec}
\usepackage{tikz}
\usepackage{changepage}
\usepackage{array}
\usepackage{tabularx}
\graphicspath{ {../../.sphinx/images/} }
\definecolor{yellowgreen}{RGB}{154, 205, 50}
\definecolor{title}{RGB}{76, 17, 48}
\definecolor{subtitle}{RGB}{116, 27, 71}
\definecolor{label}{RGB}{119, 41, 100}
\definecolor{copyright}{RGB}{174, 167, 159}
\makeatletter
\def\tcb@finalize@environment{%
  \color{.}% hack for xelatex
  \tcb@layer@dec%
}
\makeatother
\newenvironment{sphinxclassprompt}{\color{yellowgreen}\setmonofont[Color = 9ACD32, Path = ../../.sphinx/fonts/, UprightFont = *-R]{UbuntuMono}}{}
\tcbset{enhanced jigsaw, colback=black, fontupper=\color{white}}
\newtcolorbox{termbox}{use color stack, breakable, colupper=white, halign=flush left}
\newenvironment{sphinxclassterminal}{\setmonofont[Color = white, Path = ../../.sphinx/fonts/, UprightFont = *-R]{UbuntuMono}\sphinxsetup{VerbatimColor={black}}\begin{termbox}}{\end{termbox}}
\newcommand{\dimtorightedge}{%
  \dimexpr\paperwidth-1in-\hoffset-\oddsidemargin\relax}
\newcommand{\dimtotop}{%
  \dimexpr\height-1in-\voffset-\topmargin-\headheight-\headsep\relax}
\newtoggle{tpage}
\AtBeginEnvironment{titlepage}{\global\toggletrue{tpage}}
\fancypagestyle{plain}{
    \fancyhf{}
    \fancyfoot[R]{\thepage\ of \pageref*{LastPage}}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
}
\fancypagestyle{normal}{
    \fancyhf{}
    \fancyfoot[R]{\thepage\ of \pageref*{LastPage}}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
}
\fancypagestyle{titlepage}{%
    \fancyhf{}
    \fancyfoot[L]{\footnotesize \textcolor{copyright}{© 2024 Canonical Ltd. All rights reserved.}}
}
\newcommand\sphinxbackoftitlepage{\thispagestyle{titlepage}}
\titleformat{\chapter}[block]{\Huge \color{title} \bfseries\filright}{\thechapter .}{1.5ex}{}
\titlespacing{\chapter}{0pt}{0pt}{0pt}
\titleformat{\section}[block]{\huge \bfseries\filright}{\thesection .}{1.5ex}{} 
\titlespacing{\section}{0pt}{0pt}{0pt}
\titleformat{\subsection}[block]{\Large \bfseries\filright}{\thesubsection .}{1.5ex}{} 
\titlespacing{\subsection}{0pt}{0pt}{0pt}
\setcounter{tocdepth}{1}
\renewcommand\pagenumbering[1]{}
''',
    'sphinxsetup': 'verbatimwithframe=false, pre_border-radius=0pt, verbatimvisiblespace=\\phantom{}, verbatimcontinued=\\phantom{}',
    'extraclassoptions': 'openany,oneside',
    'maketitle': r'''
\begin{titlepage}
\begin{flushleft}
    \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=south east, inner sep=0] at (current page.south east) {
    \includegraphics[width=\paperwidth, height=\paperheight]{front-page-light}
    };
    \end{tikzpicture}
\end{flushleft}

\vspace*{3cm}

\begin{adjustwidth}{8cm}{0pt}
\begin{flushleft}
    \huge \textcolor{black}{\textbf{}{\raggedright{''' + project + r'''}}}
\end{flushleft}
\end{adjustwidth}

\vfill

\begin{adjustwidth}{8cm}{0pt}
\begin{tabularx}{0.5\textwidth}{ l l }
    \hspace{3cm}  & \textcolor{lightgray}{© 2024 Canonical Ltd.}  \\
    \hspace{3cm}  & \textcolor{lightgray}{All rights reserved.}   \\
    \hspace{3cm}  &                                               \\
    \hspace{3cm}  &                                               \\
                                 
\end{tabularx}
\end{adjustwidth}

\end{titlepage}
\RemoveFromHook{shipout/background}
\AddToHook{shipout/background}{
      \begin{tikzpicture}[remember picture,overlay]
      \node[anchor=south west, align=left, inner sep=0] at (current page.south west) {
        \includegraphics[width=\paperwidth]{normal-page-footer}
      };
      \end{tikzpicture}
      \begin{tikzpicture}[remember picture,overlay]
      \node[anchor=north east, opacity=0.5, inner sep=35] at (current page.north east) {
        \includegraphics[width=4cm]{Canonical-logo-4x}
      };
      \end{tikzpicture}
    }
''',
}
