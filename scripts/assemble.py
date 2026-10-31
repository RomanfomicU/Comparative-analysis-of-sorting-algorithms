"""Склеивает разделы статьи в один markdown-файл, подставляя таблицы из CSV.

Таблица в тексте задаётся строкой
    !table[Подпись таблицы](путь/к/файлу.csv){#tbl:имя}
а ссылка на неё — @tbl:имя. Таблицы нумеруются по порядку появления.

Запуск: python scripts/assemble.py build/article.md src/*.md
"""
import csv
import re
import sys

TABLE = re.compile(r"^!table\[(.*)\]\((.+?)\)\{#(tbl:[\w-]+)\}[ \t]*$", re.M)
REF = re.compile(r"@(tbl:[\w-]+)")
NUMBER = re.compile(r"^[-+]?[\d\s .,]+$")
def min_width(cell):
    """Примерная ширина самого длинного непереносимого куска ячейки:
    формулы целиком (LaTeX-команда считается за 2 символа) или слова."""
    if cell.startswith("$"):
        return len(re.sub(r"[${}^_]", "", re.sub(r"\\[a-zA-Z]+", "xx", cell)))
    return max(len(w) for w in cell.split(" ")) if cell else 0


def md_table(path, caption):
    with open(path, encoding="utf-8") as f:
        header, *rows = list(csv.reader(f))
    cols = list(zip(header, *rows))
    # Числовые столбцы выравниваются вправо, остальные влево.
    # Ширина столбца в символах задаёт pandoc относительную ширину столбца.
    sep = []
    for col in cols:
        dashes = "-" * (max(min_width(c) for c in col) + 3)
        numeric = all(NUMBER.match(c) for c in col[1:])
        sep.append(dashes + ":" if numeric else ":" + dashes)
    lines = [header, sep] + rows
    return "\n".join("| " + " | ".join(r) + " |" for r in lines) + f"\n\n: {caption}"


def main(out_path, sources):
    text = "\n\n".join(open(p, encoding="utf-8").read() for p in sources)

    numbers = {}

    def insert(m):
        caption, path, ident = m.groups()
        numbers[ident] = len(numbers) + 1
        return md_table(path, f"Таблица {numbers[ident]} — {caption}")

    text = TABLE.sub(insert, text)

    def ref(m):
        if m.group(1) not in numbers:
            print(f"assemble: неизвестная ссылка @{m.group(1)}", file=sys.stderr)
            return "??"
        return str(numbers[m.group(1)])

    text = REF.sub(ref, text)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
