.PHONY: clean test setup install_deps run_example help

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PYTHON_INTERPRETER = python
CONDA_ENV = lunapulse

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install dependencies and setup the project
setup: install_deps
	@$(PYTHON_INTERPRETER) -m pip install -e . >/dev/null 2>&1

## Install dependencies from requirements.txt
install_deps:
	@$(PYTHON_INTERPRETER) -m pip install -r requirements.txt >/dev/null 2>&1
	@echo "Dependencies installed. Verify pytest:"
	@$(PYTHON_INTERPRETER) -m pytest --version

## Run unit tests with pytest
test:
	@$(PYTHON_INTERPRETER) -m pytest Tests/

## Run the example wedge breakout backtest
run_example:
	@$(PYTHON_INTERPRETER) Examples/example_wedge_breakout.py

## Delete all compiled Python files and build artifacts
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -exec rm -r {} + >/dev/null 2>&1
	@find . -type d -name ".ipynb_checkpoints" -exec rm -r {} + >/dev/null 2>&1
	@find . -type d -name "build" -exec rm -r {} + >/dev/null 2>&1
	@find . -type d -name "dist" -exec rm -r {} + >/dev/null 2>&1
	@find . -type d -name "*.egg-info" -exec rm -r {} + >/dev/null 2>&1

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')