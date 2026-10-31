# Сборка статьи из markdown-исходников с помощью pandoc.
#
#   make          — собрать PDF, DOCX и HTML
#   make pdf      — только PDF (нужен XeLaTeX)
#   make docx     — только DOCX
#   make html     — только HTML (статический сайт)
#   make bench    — заново выполнить замеры (перезапишет data/results.csv)
#   make clean    — удалить результаты сборки

PANDOC  ?= pandoc

ifeq ($(OS),Windows_NT)
PYTHON  ?= python
FONT    ?= Times New Roman
MONO    ?= Consolas
else
PYTHON  ?= python3
FONT    ?= Liberation Serif
MONO    ?= Liberation Mono
endif

BUILD   := build
NAME    := article
SOURCES := $(sort $(wildcard src/*.md))
FIGURES := img/time.png img/ratio.png
TABLES  := tables/time.csv tables/comparisons.csv
ARTICLE := $(BUILD)/$(NAME).md
DEPS    := metadata.yaml references.bib $(ARTICLE) $(FIGURES)

PANDOC_FLAGS := metadata.yaml $(ARTICLE) --citeproc --toc --number-sections \
                --resource-path=.

.PHONY: all pdf docx html bench figures tables clean

all: pdf docx html

pdf:  $(BUILD)/$(NAME).pdf
docx: $(BUILD)/$(NAME).docx
html: $(BUILD)/index.html
figures: $(FIGURES)
tables: $(TABLES)

$(BUILD)/$(NAME).pdf: $(DEPS) | $(BUILD)
	$(PANDOC) $(PANDOC_FLAGS) --pdf-engine=xelatex \
		-V mainfont="$(FONT)" -V monofont="$(MONO)" -o $@

$(BUILD)/$(NAME).docx: $(DEPS) | $(BUILD)
	$(PANDOC) $(PANDOC_FLAGS) -o $@

$(BUILD)/index.html: $(DEPS) | $(BUILD)
	$(PANDOC) $(PANDOC_FLAGS) --standalone --embed-resources \
		--math-method=mathml --css=styles/web.css -o $@

$(ARTICLE): scripts/assemble.py $(SOURCES) $(TABLES) data/complexity.csv | $(BUILD)
	$(PYTHON) scripts/assemble.py $@ $(SOURCES)

$(FIGURES) &: scripts/plot.py data/results.csv
	$(PYTHON) scripts/plot.py data/results.csv img

$(TABLES) &: scripts/tables.py data/results.csv
	$(PYTHON) scripts/tables.py data/results.csv tables

bench:
	$(PYTHON) scripts/benchmark.py data/results.csv

$(BUILD):
	mkdir -p $(BUILD)

clean:
	rm -rf $(BUILD) img tables
