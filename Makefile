# Makefile
#
# Used to run latex compilation, run evaluation tests...

LATEX = pdflatex
BIBTEX = bibtex
PDFLATEX = pdflatex

THESIS_DIR = thesis
PROPOSAL_DIR = proposal
PRESENTATION_DIR = presentation

THESIS_FILE = thesis.tex
PROPOSAL_FILE = proposal.tex
PRESENTATION_FILE = presentation.tex

THESIS_BIBTEX = thesis
PROPOSAL_BIBTEX = proposal
PRESENTATION_BIBTEX = presentation

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

# `make build-presentation`
#
# Can optionally be referred to as `bpres`.
#
# Build the presentation.
build-presentation bpres:
	cp $(THESIS_DIR)/$(THESIS_BIBTEX).bib $(PRESENTATION_DIR)/$(PRESENTATION_BIBTEX).bib && \
	cd $(PRESENTATION_DIR) && \
	$(LATEX) $(PRESENTATION_FILE) && \
	$(BIBTEX) $(PRESENTATION_BIBTEX) && \
	$(LATEX) $(PRESENTATION_FILE) && \
	$(PDFLATEX) $(PRESENTATION_FILE)

# `make build-all`
#
# Build the thesis and the proposal.
build-all: build-proposal build-thesis build-presentation

# `make build`
#
# Build all Latex files.
build: build-thesis

# `make spellcheck`
#
# Spellcheck the thesis.
spellcheck:
	find $(THESIS_DIR) -type f -name "*.tex" -exec aspell -t -c {} \;

# `make`
#
# If no target is specified, run `build`.
.DEFAULT_GOAL := build
