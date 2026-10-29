# Run record

- Run date: 13 October 2026; official calls between 07:38:10 and 09:20:09 UTC
- Models: GPT-6.1 Sol, Claude Sonnet 5.5, Gemini 3.8 Flash
- Official final outputs: 57
- Completed official API turns: 111
- S1 repetitions: 3 per formulation per model
- S4 repetitions: 3 per trajectory per model
- S2/S3/S5/S6: 1 run per model
- Length-truncated official turns: 0
- Human ratings / kappa / inferential statistics: none

The final corpus is complete across all six scenarios and all three models. Technical connectivity and multi-turn preflight outputs are included under `results/`.

## Quota failures and session restart

- Between 08:19:07 and 08:23:08 UTC, eight Gemini 3.8 Flash jobs failed because the Gemini API daily request quota for the project had been exhausted (HTTP 429, `RESOURCE_EXHAUSTED`). The notebook retried each request automatically (up to six attempts with back-off) and then logged the job as failed. No model output was returned for these jobs, so nothing was discarded. The failed jobs are listed in `results/request_errors.csv`.
- The notebook was then re-executed at about 09:12 UTC. Jobs already completed were skipped; the eight outstanding Gemini jobs ran between 09:14 and 09:20 UTC.
- Re-execution rewrote the protocol snapshot (`protocol/protocol.json` and `provenance/pre_run_protocol_bundle.zip`, both timestamped 09:12:36 UTC) and repeated the connectivity check. The snapshot written before the first official call was overwritten. Every one of the 111 official prompts, including those sent before 09:12, is identical to the prompt templates in `protocol/protocol.json` filled with the materials in `inputs/`.

## Table A2

`scripts/table_A2_line_shares.py` reproduces Table A2 of the paper from `results/final_outputs.csv`. Each run's line share is rounded to a whole percentage before the three runs are averaged.
