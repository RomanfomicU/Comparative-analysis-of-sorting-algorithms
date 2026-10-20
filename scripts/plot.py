"""Построение рисунков статьи по данным data/results.csv.

Запуск: python scripts/plot.py data/results.csv img
"""
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

LABELS = {
    "insertion": "Вставками",
    "merge": "Слиянием",
    "quick": "Быстрая",
    "heap": "Пирамидальная",
}


def load(path):
    data = defaultdict(lambda: {"n": [], "time_ms": [], "comparisons": []})
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = data[row["algorithm"]]
            d["n"].append(int(row["n"]))
            d["time_ms"].append(float(row["time_ms"]))
            d["comparisons"].append(int(row["comparisons"]))
    return data


def plot_time(data, out):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for name, d in data.items():
        ax.plot(d["n"], d["time_ms"], marker="o", label=LABELS[name])
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("Размер массива $n$")
    ax.set_ylabel("Время, мс")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def plot_ratio(data, out):
    """Отношение числа сравнений к n*log2(n) — для n log n алгоритмов
    оно должно стремиться к константе."""
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for name, d in data.items():
        if name == "insertion":
            continue
        ratio = [c / (n * math.log2(n)) for n, c in zip(d["n"], d["comparisons"])]
        ax.plot(d["n"], ratio, marker="s", label=LABELS[name])
    ax.set_xscale("log", base=2)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Размер массива $n$")
    ax.set_ylabel(r"$C(n) \,/\, (n \log_2 n)$")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def main(csv_path, img_dir):
    img_dir.mkdir(parents=True, exist_ok=True)
    data = load(csv_path)
    plot_time(data, img_dir / "time.png")
    plot_ratio(data, img_dir / "ratio.png")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
