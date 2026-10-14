from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
results = ROOT / "results"

final = pd.read_csv(results / "final_outputs.csv")
off = pd.read_csv(results / "official_turns.csv")

assert len(final) == 57, f"Expected 57 final outputs, found {len(final)}"
assert len(off) == 111, f"Expected 111 official turns, found {len(off)}"
assert not off["truncated"].astype(str).str.lower().eq("true").any(), "A public official turn is marked truncated"

expected = {
    "S1_framing": 27,
    "S2_uncertainty": 3,
    "S3_coherence": 3,
    "S4_provenance": 18,
    "S5_engineering": 3,
    "S6_scicomm": 3,
}
counts = final.groupby("scenario_id").size().to_dict()
assert counts == expected, f"Unexpected scenario counts: {counts}"

print("OK: 57 final outputs, 111 official turns, no official truncations.")
