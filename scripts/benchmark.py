"""Замер времени работы и числа сравнений для четырёх алгоритмов сортировки.

Результат записывается в data/results.csv. Запуск: python scripts/benchmark.py
"""
import csv
import random
import sys
import time
from pathlib import Path

SIZES = [250, 500, 1000, 2000, 4000]
REPEATS = 5
SEED = 42


class Counter:
    """Считает количество сравнений элементов."""

    def __init__(self):
        self.n = 0

    def less(self, a, b):
        self.n += 1
        return a < b


def insertion_sort(a, c):
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and c.less(x, a[j]):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def merge_sort(a, c):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid], c), merge_sort(a[mid:], c)
    res, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if c.less(right[j], left[i]):
            res.append(right[j])
            j += 1
        else:
            res.append(left[i])
            i += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res


def quick_sort(a, c, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    while lo < hi:
        pivot = a[random.randint(lo, hi)]
        i, j = lo, hi
        while i <= j:
            while c.less(a[i], pivot):
                i += 1
            while c.less(pivot, a[j]):
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        # рекурсия в меньшую часть, чтобы глубина стека была O(log n)
        if j - lo < hi - i:
            quick_sort(a, c, lo, j)
            lo = i
        else:
            quick_sort(a, c, i, hi)
            hi = j


def heap_sort(a, c):
    def sift(start, end):
        root = start
        while 2 * root + 1 <= end:
            child = 2 * root + 1
            if child + 1 <= end and c.less(a[child], a[child + 1]):
                child += 1
            if c.less(a[root], a[child]):
                a[root], a[child] = a[child], a[root]
                root = child
            else:
                return

    n = len(a)
    for start in range(n // 2 - 1, -1, -1):
        sift(start, n - 1)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift(0, end - 1)


ALGORITHMS = {
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
}


def run(func, data):
    a = list(data)
    c = Counter()
    t0 = time.perf_counter()
    out = func(a, c)
    elapsed = time.perf_counter() - t0
    result = out if out is not None else a
    assert result == sorted(data)
    return elapsed, c.n


def main(out_path):
    random.seed(SEED)
    rows = []
    for n in SIZES:
        inputs = [[random.random() for _ in range(n)] for _ in range(REPEATS)]
        for name, func in ALGORITHMS.items():
            times, comps = [], []
            for data in inputs:
                t, k = run(func, data)
                times.append(t)
                comps.append(k)
            rows.append({
                "algorithm": name,
                "n": n,
                "time_ms": round(1000 * sum(times) / REPEATS, 3),
                "comparisons": round(sum(comps) / REPEATS),
            })
            print(f"{name:>10} n={n:<5} {rows[-1]['time_ms']:>10.3f} мс")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "data/results.csv"))
