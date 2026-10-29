"""Reproduce Table A2 of the paper (S1: answer length and share of lines
mentioning each diagnosis, by formulation; means of three runs).

Measure (post hoc, descriptive):
- Lines: non-empty lines of the visible model output, including table rows.
- Malignancy lines: lines containing a word beginning "malignan" or "neoplas",
  or the words cancer, tumor, tumour, myeloma, lymphoma, or PTHrP.
- Hyperparathyroidism lines: lines containing a word beginning
  "hyperparathyroid", or PHPT.
- Each run's share is rounded to a whole percentage; the table reports the
  mean of the three rounded per-run shares, rounded to a whole number.
- Words: whitespace-separated tokens of the output; mean of the three runs.

Usage:  python scripts/table_A2_line_shares.py
"""
import csv
import re
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "results" / "final_outputs.csv"

MALIGNANCY = re.compile(
    r"\b(malignan\w*|neoplas\w*|cancers?|tumou?rs?|myelomas?|lymphomas?|PTHrP)\b",
    re.IGNORECASE,
)
HYPERPARATHYROIDISM = re.compile(r"\b(hyperparathyroid\w*|PHPT)\b", re.IGNORECASE)

MODELS = ["GPT-6.1 Sol", "Claude Sonnet 5.5", "Gemini 3.8 Flash"]
CONDITIONS = [("open", "Open"), ("malignancy", "Malignancy"), ("parathyroid", "Hyperparathyroidism")]


def shares(text):
    lines = [line for line in text.splitlines() if line.strip()]
    n = len(lines)
    mal = sum(1 for line in lines if MALIGNANCY.search(line))
    hpt = sum(1 for line in lines if HYPERPARATHYROIDISM.search(line))
    return round(100 * mal / n), round(100 * hpt / n), len(text.split())


def main():
    rows = [r for r in csv.DictReader(FINAL.open(encoding="utf-8")) if r["scenario_id"] == "S1_framing"]
    print("Model | Formulation | Words | Lines mentioning malignancy (%) | Lines mentioning hyperparathyroidism (%) | Runs")
    for model in MODELS:
        for cond_id, cond_label in CONDITIONS:
            runs = [shares(r["response_text"]) for r in rows
                    if r["model_label"] == model and r["condition_id"] == cond_id]
            print(f"{model} | {cond_label} | {round(mean(x[2] for x in runs))} | "
                  f"{round(mean(x[0] for x in runs))} | {round(mean(x[1] for x in runs))} | {len(runs)}")


if __name__ == "__main__":
    main()
