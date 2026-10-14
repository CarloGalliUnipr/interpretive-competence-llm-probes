# Model and API metadata

The repository does **not** contain model weights. All three systems were accessed through their providers' APIs. Exact model identifiers used in the run are recorded below and in `protocol/protocol.json`.

| Provider | Label used in paper | API model ID |
|---|---|---|
| Openai | GPT-6.1 Sol | `gpt-6.1-sol` |
| Anthropic | Claude Sonnet 5.5 | `claude-sonnet-5-5` |
| Google | Gemini 3.8 Flash | `gemini-3.8-flash` |

Protocol snapshot saved: `2026-10-13T09:12:36.410658+00:00`.

Provider-default reasoning/thinking behaviour was retained. Temperature and top-p were not explicitly set. No system prompt, tools, retrieval, or web search were supplied by the notebook.
