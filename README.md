# Interpretive Probes for AI-Mediated Knowledge Production

Reproducibility package for the illustrative LLM runs accompanying the paper **“Interpretive Competence as Epistemic Infrastructure in AI-Mediated Knowledge Production.”**

## What this repository contains

The package documents six illustrative scenarios used to instantiate the paper's conceptual claims with real model outputs. It includes the exact pre-run protocol, prompts and constructed materials, the clinical reference used for descriptive comparison in S2, a Colab notebook and code export, model/API metadata, technical preflight checks, all official outputs, all saved attempts, and convenience comparison tables for the two comparative scenarios (S1 and S4).

The runs are **illustrative rather than a benchmark or validation study**. They do not estimate failure prevalence, rank models, validate the four human competencies, or use inferential statistics.

## Models

The run used three API-accessed models:

- OpenAI GPT-6.1 Sol — `gpt-6.1-sol`
- Anthropic Claude Sonnet 5.5 — `claude-sonnet-5-5`
- Google Gemini 3.8 Flash — `gemini-3.8-flash`

Model weights are proprietary and are **not** part of this repository. Exact API identifiers and recorded SDK versions are in `docs/model_metadata.md` and `protocol/protocol.json`.

## Design

- S1 framing: 3 formulations × 3 repetitions × 3 models = 27 final outputs
- S2 uncertainty: 1 × 1 × 3 = 3
- S3 evidential coherence: 1 × 1 × 3 = 3
- S4 interactional provenance: 2 trajectories × 3 repetitions × 3 models = 18
- S5 engineering standards: 3
- S6 science communication: 3

**Total: 57 final outputs and 111 official API turns.** The three repetitions in S1 and S4 are robustness checks, not a statistical sample.

## Repository structure

```text
notebooks/
  official_run_notebook.ipynb   # public copy of the notebook used for the run
  reproduce_run.ipynb           # same workflow, writes to a fresh Drive folder
protocol/
  protocol.json                 # exact model/scenario/generation policy snapshot
  job_manifest.csv              # 57 planned jobs
  analysis_questions.md         # prespecified descriptive questions
inputs/                         # constructed study/standards/science-communication materials
reference/
  reference_standard_S2.md      # descriptive clinical reference; never shown to models
results/
  final_outputs.csv             # 57 final outputs
  official_turns.csv/jsonl      # all 111 official turns
  all_attempts.csv/jsonl        # all saved attempts
  supplement_model_outputs.md   # every official prompt and visible output, verbatim
  S1_framing_comparison.csv
  S4_provenance_comparison.csv
  run_summary.csv
  connectivity_test.csv
  multiturn_preflight.csv
provenance/
  pre_run_protocol_bundle.zip   # snapshot made before official calls
  run_record.md
docs/
  framework_and_scenario_mapping.md
  model_metadata.md
  data_dictionary.md
scripts/
  official_run_code_export.py
  validate_outputs.py
```

## Reproducing the run in Colab

1. Open `notebooks/reproduce_run.ipynb` in Google Colab.
2. Run the install cell. The public notebook pins the SDK versions recorded in the original run.
3. When prompted, enter API keys for OpenAI, Anthropic and Google. `getpass()` hides the keys and the notebook does not save them.
4. Run the one-turn connectivity check and the two-turn conversation preflight.
5. Run the official jobs. The notebook is resumable and saves individual jobs atomically.
6. Run the consolidation/export cells.

API models are external services and can change over time even when the same model alias remains available, so a future rerun is not expected to reproduce wording exactly. The archived output files are the record of the October 2026 run.

## Public-data note

The public result files preserve prompts, visible model outputs, model identifiers, stop/status metadata, usage metadata, timestamps and study metadata. Provider-specific response IDs have been removed because they are not needed for replication. No API keys are present.

## Quick integrity check

```bash
python scripts/validate_outputs.py
```

This checks that the package contains 57 final outputs, 111 official turns, the expected scenario counts, and no official length truncations.

## Citation and license

Please cite the associated paper when using this repository. Add the final bibliographic citation/DOI to this README once the paper is accepted or published. No software/data license has been imposed in this package; choose the license that matches the authors' and journal's intended reuse terms before making the repository public.
