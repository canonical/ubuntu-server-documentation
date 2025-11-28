# Wrapper Makefile to forward all commands to docs/Makefile
# This allows "make" commands to be run from the root dir

# Get the directory where this Makefile is located (repository root)
ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# Forward all targets to the docs/Makefile
.DEFAULT_GOAL := help

# Catch-all target: route all unknown targets to docs/Makefile
%:
	@$(MAKE) -C $(ROOT_DIR)docs $@

.PHONY: help
