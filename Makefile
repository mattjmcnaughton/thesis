# Makefile
#
# Used to run latex compilation, run evaluation tests...

# Use `-shell-escape` to support the `minted` package for including code.
LATEX = pdflatex -shell-escape
BIBTEX = bibtex
PDFLATEX = pdflatex -shell-escape

THESIS_DIR = thesis
PROPOSAL_DIR = proposal

THESIS_FILE = thesis.tex
PROPOSAL_FILE = proposal.tex

THESIS_BIBTEX = thesis
PROPOSAL_BIBTEX = proposal

# `make build-thesis`
#
# Build the thesis.
build-thesis:
	cd $(THESIS_DIR) && \
	$(LATEX) $(THESIS_FILE) && \
	$(BIBTEX) $(THESIS_BIBTEX) && \
	$(LATEX) $(THESIS_FILE) && \
	$(PDFLATEX) $(THESIS_FILE)

# `make build-proposal`
#
# Build the thesis description.
build-proposal:
	cd $(PROPOSAL_DIR) && \
	$(LATEX) $(PROPOSAL_FILE) && \
	$(BIBTEX) $(PROPOSAL_BIBTEX) && \
	$(LATEX) $(PROPOSAL_FILE) && \
	$(PDFLATEX) $(PROPOSAL_FILE)

# `make build-all`
#
# Build the thesis and the proposal.
build-all: build-proposal build-thesis

# `make build`
#
# Build all Latex files.
build: build-thesis

# `make spellcheck`
#
# Spellcheck the thesis.
spellcheck:
	find $(THESIS_DIR) -type f -name "*.tex" -exec aspell -t -c {} \;

# `make tmux`
#
# Open the projects tmux (based on the `.tmuxinator.yml`) file.
tmux:
	tmuxinator start .

# `make`
#
# If no target is specified, run `build`.
.DEFAULT_GOAL := build
