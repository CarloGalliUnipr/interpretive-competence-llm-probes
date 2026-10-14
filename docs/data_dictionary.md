# Data dictionary

`final_outputs.csv` contains one final-turn record for each of the 57 official jobs. `official_turns.csv` / `official_turns.jsonl` contain all 111 official API turns, including intermediate turns in S4. `all_attempts.csv` / `all_attempts.jsonl` contain every saved model-response attempt.

In the completed run, all saved jobs completed on the first saved attempt and no official turn was length-truncated. The public copies omit provider `response_id` values because they are unnecessary for reproducing the analysis. API keys were never written to the result files.

## Columns

- `attempt_kind` — Whether the row comes from the official corpus or the saved-attempt record.
- `job_id` — Unique job identifier.
- `attempt_number` — Saved-attempt number for the job.
- `official_attempt` — Attempt selected as official after the truncation rule.
- `previous_truncated_attempt` — Whether an earlier length-truncated attempt preceded the official attempt.
- `provider` — API provider key used by the notebook.
- `model_label` — Human-readable model label.
- `model_requested` — Requested API model identifier.
- `model_returned` — Model identifier returned by the provider, when available.
- `scenario_id` — Scenario identifier S1–S6.
- `paper_section` — Paper section associated with the scenario.
- `scenario_title` — Human-readable scenario title.
- `conceptual_issue` — Conceptual vulnerability the scenario was designed to instantiate.
- `condition_id` — Within-scenario condition identifier.
- `condition_label` — Human-readable condition label.
- `repetition` — Repetition number; three only for S1 and S4.
- `turn_index` — Turn number within the conversation.
- `n_turns` — Total number of turns in that job.
- `is_final_turn` — Whether the row is the final turn used as the scenario output.
- `prompt` — Verbatim prompt supplied to the model.
- `response_text` — Verbatim visible model output.
- `status_or_stop_reason` — Provider completion/stop status.
- `incomplete_details` — Serialized provider incompletion details, when available.
- `truncated` — Length-truncation flag.
- `usage` — Provider usage metadata serialized as JSON when available.
- `timestamp_utc` — UTC timestamp recorded by the notebook.
