# Сравнительный анализ алгоритмов сортировки

Статья в формате Markdown, которая автоматически собирается в **PDF**, **DOCX** и
**HTML** с помощью [Pandoc](https://pandoc.org) и `make`.

В статье есть оглавление, LaTeX-формулы, таблицы, рисунки (строятся скриптом
по данным эксперимента) и список литературы по ГОСТ Р 7.0.5-2008.

## Структура

```
.
├── Makefile                 # сборка
├── metadata.yaml            # заголовок, автор, аннотация, настройки pandoc/LaTeX
├── references.bib           # список литературы (BibTeX)
├── src/                     # текст статьи, по файлу на раздел
│   ├── 01-introduction.md
│   ├── 02-theory.md
│   ├── 03-experiment.md
│   ├── 04-conclusion.md
│   └── 05-references.md
├── data/results.csv         # результаты замеров
├── scripts/
│   ├── benchmark.py         # реализация алгоритмов и замеры → data/results.csv
│   └── plot.py              # построение рисунков → img/*.png
├── styles/
│   ├── gost-r-7-0-5-2008-numeric.csl   # стиль библиографии
│   └── web.css              # стиль HTML-версии
└── .github/workflows/build.yml         # автоматическая сборка в GitHub Actions
```

## Сборка

Нужны: `pandoc` ≥ 3.0, `make`, Python 3 с `matplotlib`, а для PDF — XeLaTeX
(TeX Live, MiKTeX или TinyTeX) с поддержкой русского языка.

```bash
make            # PDF + DOCX + HTML в каталог build/
make docx       # только Word
make pdf        # только PDF
make html       # только HTML
make clean      # удалить build/ и img/
make bench      # заново провести замеры (перезапишет data/results.csv)
```

На Windows:

```bash
winget install JohnMacFarlane.Pandoc ezwinports.make
```

и сборка с системным шрифтом и интерпретатором `python`:

```bash
make PYTHON=python FONT="Times New Roman" MONO=Consolas
```

Оглавление в DOCX — это поле Word: при открытии файла Word предложит обновить
поля, нужно согласиться.

## Автоматическая сборка

При каждом push в ветку `main` GitHub Actions собирает все три формата.
Результат — во вкладке **Actions** → последний запуск → артефакт `article`.
