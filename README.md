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
├── data/
│   ├── results.csv          # результаты замеров
│   └── complexity.csv       # таблица теоретических сложностей
├── scripts/
│   ├── benchmark.py         # реализация алгоритмов и замеры → data/results.csv
│   ├── plot.py              # построение рисунков → img/*.png
│   ├── tables.py            # CSV-файлы таблиц по результатам замеров → tables/*.csv
│   └── assemble.py          # склейка разделов, вставка таблиц из CSV и их нумерация
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

Запускать `make` нужно из Git Bash. На Windows Makefile сам выбирает
интерпретатор `python` и шрифты Times New Roman / Consolas, в Linux —
`python3` и Liberation Serif / Mono. Любое значение можно переопределить,
например `make FONT="Arial"`.

Оглавление в DOCX — это поле Word: при открытии файла Word предложит обновить
поля, нужно согласиться.

## Таблицы

Таблицы не пишутся в markdown вручную, а берутся из CSV-файлов. В тексте
таблица вставляется так:

```markdown
Результаты приведены в таблице @tbl:time.

!table[Среднее время сортировки, мс](tables/time.csv){#tbl:time}
```

Скрипт `scripts/assemble.py` склеивает разделы из `src/` в `build/article.md`,
заменяет такие строки таблицами из CSV (первая строка — заголовок), нумерует
таблицы по порядку и заменяет ссылки `@tbl:...` номерами. Pandoc собирает
документы уже из `build/article.md`.

## Автоматическая сборка

При каждом push в ветку `main` GitHub Actions собирает все три формата.
Результат — во вкладке **Actions** → последний запуск → артефакт `article`.
