# Makefile
#
# Used to run latex compilation, run evaluation tests...

LATEX = pdflatex
BIBTEX = bibtex
PDFLATEX = pdflatex

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

# `make build`
#
# Build all Latex files.
build: build-thesis build-proposal

# `make`
#
# If no target is specified, run `build`.
.DEFAULT_GOAL := build
