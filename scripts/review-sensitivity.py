"""Descriptive review follow-ups from saved results; no model inference.

Run from any directory with Python 3.10+. Item-deletion ranges are not
confidence intervals or paired tests. Binding sign counts summarize the
registered secondary aggregations, not new confirmatory tests.
"""
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import correlation, mean

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/analysis"


def read(name):
    with (OUT / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def write(name, rows):
    with (OUT / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def ranks(values):
    positions = defaultdict(list)
    for i, value in enumerate(sorted(values), 1):
        positions[value].append(i)
    return [mean(positions[value]) for value in values]


groups = defaultdict(lambda: defaultdict(list))
scores = {"correct": 1.0, "partial": 0.5, "incorrect": 0.0}
for row in read("elicitation_coded.csv"):
    if (row["domain"] == "accessibility" and row["source"] == "original"
            and row["prompt_type"] in ("declarative", "evaluative")):
        groups[(row["suite"], row["scale_label"], row["model"])][row["prompt_type"]].append(
            (row["prompt_id"], scores[row["accuracy"]]))
assert len(groups) == 13
baseline = {(family, row["scale"]): float(row["gap_pct_pts"])
            for family in ("pythia", "gpt2", "olmo")
            for row in read(f"{family}_gap.csv")}
deletions = []
for (family, scale, model), batteries in sorted(groups.items()):
    d = [v for _, v in batteries["declarative"]]
    e = [v for _, v in batteries["evaluative"]]
    assert len(d) == 10 and len(e) == 5
    assert all(len({p for p, _ in values}) == len(values) for values in batteries.values())
    gap = 100 * (mean(d) - mean(e))
    assert math.isclose(gap, baseline[family, scale], abs_tol=1e-10)
    variants = [100 * (mean(d[:i] + d[i+1:]) - mean(e)) for i in range(10)]
    variants += [100 * (mean(d) - mean(e[:i] + e[i+1:])) for i in range(5)]
    deletions.append(dict(family=family, scale=scale, model=model,
                          gap_pp=round(gap, 6), deletion_min_pp=round(min(variants), 6),
                          deletion_max_pp=round(max(variants), 6), n_deletions=15))
write("original_gap_item_deletion.csv", deletions)

signs = []
for condition in ("natural", "uniform"):
    compounds = defaultdict(list)
    for row in read(f"effective_binding_compound_summary_{condition}.csv"):
        compounds[row["model"]].append(row)
    saved = read(f"effective_binding_correlations_{condition}.csv")
    for measure in ("p95_relative", "max_relative", "mean_top5_relative"):
        selected = [r for r in saved if r["measure"] == measure]
        assert len(selected) == 13
        for row in selected:
            group = compounds[row["model"]]
            assert len(group) == len({r["compound"] for r in group}) == 49
            rho = correlation(ranks([float(r["log_frequency"]) for r in group]),
                              ranks([float(r[measure]) for r in group]))
            assert math.isclose(rho, float(row["rho"]), abs_tol=1e-12)
        values = [float(r["rho"]) for r in selected]
        signs.append(dict(condition=condition, measure=measure, n_models=13,
                          n_negative=sum(v < 0 for v in values),
                          rho_min=min(values), rho_max=max(values)))
write("effective_binding_aggregation_signs.csv", signs)
print("Verified original means for 13 models and 78 saved binding correlations.")
for row in deletions:
    print(row)
for row in signs:
    print(row)
