# Сборка статьи из markdown-исходников с помощью pandoc.
#
#   make          — собрать PDF, DOCX и HTML
#   make pdf      — только PDF (нужен XeLaTeX)
#   make docx     — только DOCX
#   make html     — только HTML (статический сайт)
#   make bench    — заново выполнить замеры (перезапишет data/results.csv)
#   make clean    — удалить результаты сборки

PANDOC  ?= pandoc

# На Windows интерпретатор называется python, а шрифты Liberation обычно не установлены
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
DEPS    := metadata.yaml references.bib $(SOURCES) $(FIGURES)

PANDOC_FLAGS := metadata.yaml $(SOURCES) --citeproc --toc --number-sections \
                --resource-path=.

.PHONY: all pdf docx html bench figures clean

all: pdf docx html

pdf:  $(BUILD)/$(NAME).pdf
docx: $(BUILD)/$(NAME).docx
html: $(BUILD)/index.html
figures: $(FIGURES)

$(BUILD)/$(NAME).pdf: $(DEPS) | $(BUILD)
	$(PANDOC) $(PANDOC_FLAGS) --pdf-engine=xelatex \
		-V mainfont="$(FONT)" -V monofont="$(MONO)" -o $@

$(BUILD)/$(NAME).docx: $(DEPS) | $(BUILD)
	$(PANDOC) $(PANDOC_FLAGS) -o $@

$(BUILD)/index.html: $(DEPS) | $(BUILD)
	$(PANDOC) $(PANDOC_FLAGS) --standalone --embed-resources \
		--math-method=mathml --css=styles/web.css -o $@

$(FIGURES) &: scripts/plot.py data/results.csv
	$(PYTHON) scripts/plot.py data/results.csv img

bench:
	$(PYTHON) scripts/benchmark.py data/results.csv

$(BUILD):
	mkdir -p $(BUILD)

clean:
	rm -rf $(BUILD) img
