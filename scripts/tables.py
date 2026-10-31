"""Формирование CSV-файлов таблиц статьи по данным data/results.csv.

Запуск: python scripts/tables.py data/results.csv tables
"""
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

LABELS = {
    "insertion": "Вставками",
    "merge": "Слиянием",
    "quick": "Быстрая",
    "heap": "Пирамидальная",
}

NBSP = " "  # неразрывный пробел между разрядами


def fmt_int(x):
    return f"{round(x):,}".replace(",", NBSP)


def fmt_float(x, digits):
    return f"{x:.{digits}f}".replace(".", ",")


# Теоретическая оценка числа сравнений: (формула для таблицы, функция от n)
def harmonic(n):
    return sum(1 / k for k in range(1, n + 1))


THEORY = {
    "insertion": ("$n^2/4$", lambda n: n * n / 4),
    "merge": (
        r"$\le n\lceil\log_2 n\rceil - 2^{\lceil\log_2 n\rceil} + 1$",
        lambda n: n * math.ceil(math.log2(n)) - 2 ** math.ceil(math.log2(n)) + 1,
    ),
    "quick": ("$2(n+1)H_n - 4n$", lambda n: 2 * (n + 1) * harmonic(n) - 4 * n),
    "heap": (r"$\le 2 n \log_2 n$", lambda n: 2 * n * math.log2(n)),
}


def load(path):
    data = defaultdict(dict)  # algorithm -> n -> row
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["algorithm"]][int(row["n"])] = row
    return data


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def time_table(data):
    sizes = sorted(next(iter(data.values())))
    rows = [["Алгоритм"] + [f"$n={n}$" for n in sizes]]
    for name, by_n in data.items():
        rows.append([LABELS[name]] + [fmt_float(float(by_n[n]["time_ms"]), 3) for n in sizes])
    return rows


def comparisons_table(data):
    n = max(next(iter(data.values())))
    nlogn = n * math.log2(n)
    rows = [[
        "Алгоритм",
        "Измерено $C(n)$",
        "Теоретическая оценка",
        "Значение оценки",
        r"$C(n) / (n\log_2 n)$",
    ]]
    for name, by_n in data.items():
        c = int(by_n[n]["comparisons"])
        formula, estimate = THEORY[name]
        ratio = c / nlogn
        rows.append([
            LABELS[name],
            fmt_int(c),
            formula,
            fmt_int(estimate(n)),
            fmt_float(ratio, 1 if ratio >= 10 else 3),
        ])
    return rows


def main(csv_path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    data = load(csv_path)
    write(out_dir / "time.csv", time_table(data))
    write(out_dir / "comparisons.csv", comparisons_table(data))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
