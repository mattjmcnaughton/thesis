# Makefile
#
# Used to run latex compilation, run evaluation tests...

LATEX = latex
BIBTEX = bibtex
PDFLATEX = pdflatex

THESIS_DIR = thesis
THESIS_DESCRIPTION_DIR = thesis-description

THESIS_FILE = thesis.tex
THESIS_DESCRIPTION_FILE = thesis-description.tex

THESIS_BIBTEX = thesis
THESIS_DESCRIPTION_BIBTEX = thesis-description

# `make build-thesis`
#
# Build the thesis.
build-thesis:
	cd $(THESIS_DIR) && \
	$(LATEX) $(THESIS_FILE) && \
	$(BIBTEX) $(THESIS_BIBTEX) && \
	$(LATEX) $(THESIS_FILE) && \
	$(PDFLATEX) $(THESIS_FILE)

# `make build-thesis-description`
#
# Build the thesis description.
build-thesis-description:
	cd $(THESIS_DESCRIPTION_DIR) && \
	$(LATEX) $(THESIS_DESCRIPTION_FILE) && \
	$(BIBTEX) $(THESIS_DESCRIPTION_BIBTEX) && \
	$(LATEX) $(THESIS_DESCRIPTION_FILE) && \
	$(PDFLATEX) $(THESIS_DESCRIPTION_FILE)

# `make build`
#
# Build all Latex files.
build: build-thesis build-thesis-description

# `make`
#
# If no target is specified, run `build`.
.DEFAULT_GOAL := build
