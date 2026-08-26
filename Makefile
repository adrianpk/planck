.SILENT:

PYTHON ?= python3

.PHONY: diagrams
diagrams:
	$(PYTHON) scripts/generate_layer_diagrams.py
