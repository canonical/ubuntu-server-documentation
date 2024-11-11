# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXDIR     = .sphinx
SPHINXOPTS    ?= -c . -d $(SPHINXDIR)/.doctrees
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
VENVDIR       = $(SPHINXDIR)/venv
PA11Y         = $(SPHINXDIR)/node_modules/pa11y/bin/pa11y.js --config $(SPHINXDIR)/pa11y.json
VENV          = $(VENVDIR)/bin/activate

.PHONY: sp-full-help sp-woke-install sp-pa11y-install sp-install sp-run sp-html \
        sp-epub sp-serve sp-clean sp-clean-doc sp-spelling sp-linkcheck sp-woke \
        sp-pa11y sp-pdf sp-pdf-prep sp-pdf-prep-force Makefile.sp

sp-full-help: $(VENVDIR)
	@. $(VENV); $(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "\n\033[1;31mNOTE: This help texts shows unsupported targets!\033[0m"
	@echo "Run 'make help' to see supported targets."

# Shouldn't assume that venv is available on Ubuntu by default; discussion here:
# https://bugs.launchpad.net/ubuntu/+source/python3.4/+bug/1290847
$(SPHINXDIR)/requirements.txt:
	python3 $(SPHINXDIR)/build_requirements.py
	python3 -c "import venv" || sudo apt install python3-venv

# If requirements are updated, venv should be rebuilt and timestamped.
$(VENVDIR): $(SPHINXDIR)/requirements.txt
	@echo "... setting up virtualenv"
	python3 -m venv $(VENVDIR)
	. $(VENV); pip install --require-virtualenv \
	    --upgrade -r $(SPHINXDIR)/requirements.txt \
            --log $(VENVDIR)/pip_install.log
	@test ! -f $(VENVDIR)/pip_list.txt || \
            mv $(VENVDIR)/pip_list.txt $(VENVDIR)/pip_list.txt.bak
	@. $(VENV); pip list --local --format=freeze > $(VENVDIR)/pip_list.txt
	@touch $(VENVDIR)

sp-woke-install:
	@type woke >/dev/null 2>&1 || \
            { echo "Installing \"woke\" snap... \n"; sudo snap install woke; }

sp-pa11y-install:
	@type $(PA11Y) >/dev/null 2>&1 || { \
			echo "Installing \"pa11y\" from npm... \n"; \
			mkdir -p $(SPHINXDIR)/node_modules/ ; \
			npm install --prefix $(SPHINXDIR) pa11y; \
		}

sp-install: $(VENVDIR)
	command -v distro-info || (sudo apt-get update; sudo apt-get install --assume-yes distro-info)

sp-run: sp-install
	. $(VENV); sphinx-autobuild -b dirhtml "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Doesn't depend on $(BUILDDIR) to rebuild properly at every run.
sp-html: sp-install
	. $(VENV); $(SPHINXBUILD) -W --keep-going -b dirhtml "$(SOURCEDIR)" "$(BUILDDIR)" -w $(SPHINXDIR)/warnings.txt $(SPHINXOPTS)

sp-epub: sp-install
	. $(VENV); $(SPHINXBUILD) -b epub "$(SOURCEDIR)" "$(BUILDDIR)" -w $(SPHINXDIR)/warnings.txt $(SPHINXOPTS)

sp-serve: sp-html
	cd "$(BUILDDIR)"; python3 -m http.server 8000

sp-clean: sp-clean-doc
	@test ! -e "$(VENVDIR)" -o -d "$(VENVDIR)" -a "$(abspath $(VENVDIR))" != "$(VENVDIR)"
	rm -rf $(VENVDIR)
	rm -f $(SPHINXDIR)/requirements.txt
	rm -rf $(SPHINXDIR)/node_modules/

sp-clean-doc:
	git clean -fx "$(BUILDDIR)"
	rm -rf $(SPHINXDIR)/.doctrees

sp-spelling: sp-html
	. $(VENV) ; python3 -m pyspelling -c $(SPHINXDIR)/spellingcheck.yaml -j $(shell nproc) >> spellcheck.txt

sp-linkcheck: sp-install
	. $(VENV) ; $(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) >> linkcheck.txt

sp-woke: sp-woke-install
	woke *.rst **/*.rst --exit-1-on-failure \
	    -c https://github.com/canonical/Inclusive-naming/raw/main/config.yml

sp-pa11y: sp-pa11y-install sp-html
	find $(BUILDDIR) -name *.html -print0 | xargs -n 1 -0 $(PA11Y)

sp-pdf-prep: sp-install
	@. $(VENV); (dpkg-query -W -f='$${Status}' latexmk 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package latexmk is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' fonts-freefont-otf 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package fonts-freefont-otf is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' fonts-ibm-plex 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package fonts-ibm-plex is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' texlive-latex-recommended 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package texlive-latex-recommended is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' texlive-latex-extra 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package texlive-latex-extra is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' texlive-fonts-recommended 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package texlive-fonts-recommended is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' texlive-font-utils 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package texlive-font-utils is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' texlive-lang-cjk 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package texlive-lang-cjk is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' texlive-xetex 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package texlive-xetex is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' plantuml 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package plantuml is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' xindy 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package xindy is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' tex-gyre 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package tex-gyre is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)
	@. $(VENV); (dpkg-query -W -f='$${Status}' dvipng 2>/dev/null | grep -c "ok installed" >/dev/null && echo "Package dvipng is installed") || (echo "PDF generation requires the installation of the following packages: latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng" && echo "" && echo "make pdf-prep-force will install these packages" && echo "" && echo "Please be aware these packages will be installed to your system" && false)

sp-pdf-prep-force:
	@. $(VENV); apt-get update
	@. $(VENV); apt-get upgrade -y
	@. $(VENV); apt-get install --no-install-recommends -y latexmk fonts-freefont-otf fonts-ibm-plex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-font-utils texlive-lang-cjk texlive-xetex plantuml xindy tex-gyre dvipng \

sp-pdf: sp-pdf-prep
	@. $(VENV); sphinx-build -M latexpdf "$(SOURCEDIR)" "_build" $(SPHINXOPTS)
	@. $(VENV); find ./_build/latex -name "*.pdf" -exec mv -t ./ {} +
	@. $(VENV); rm -r _build

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile.sp
	. $(VENV); $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
