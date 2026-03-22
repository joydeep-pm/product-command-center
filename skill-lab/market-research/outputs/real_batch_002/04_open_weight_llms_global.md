# Open-Weight LLM Models of the World

## Executive Summary
The open-weight frontier is now led by a small number of globally relevant families: `DeepSeek`, `Qwen`, `Gemma`, `Mistral`, and specialist coding models such as `Codestral`. The first batch failed because it discussed these models qualitatively; this rerun fixes that by using a benchmark matrix with vendor-published numbers where available and by explicitly marking where numbers are not directly comparable or not machine-readable on the official page.

## Scope
- **Category**: major open-weight LLM families with current global relevance.
- **Decision uses**: model benchmarking, investor briefing, internal strategy, enterprise shortlist formation.
- **Required dimensions**: reasoning, coding, multilingual capability, context length, license/commercial usability, deployability.

## Coverage Checklist
| Requested slice | Status | Notes |
|---|---|---|
| General-purpose frontier open-weight models | Covered | DeepSeek, Qwen, Gemma, Mistral included. |
| Coding-specialist open-weight model | Covered | Codestral included separately. |
| Benchmark numbers | Covered | Vendor-published numbers included where retrievable from official sources. |
| Multilingual capability | Covered | Mix of numeric and official language-support disclosures. |
| License / commercial usability | Covered | Category-level license notes included. |
| Deployment / efficiency | Covered | Context, size, and deployment notes included. |

## Benchmark Matrix
| Model | Published benchmark evidence | Reasoning / knowledge | Coding | Multilingual / global | Context | License / commercial usability | Deployability read |
|---|---|---|---|---|---|---|---|
| [DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3) | Official README with side-by-side benchmark tables | MMLU-Pro **75.9**, GPQA-Diamond **59.1** | LiveCodeBench **37.6**, HumanEval-Mul **82.6**, Codeforces **51.6** | MMMLU-non-English **79.4** | **128K** | MIT code repo + model license; official page says commercial use supported | Very strong frontier reasoning/coding tradeoff, but large and operationally heavy. |
| [Qwen2.5-72B-Instruct](https://qwenlm.github.io/blog/qwen2.5-llm/) | Official Qwen blog and model card | MATH **83.1**, strong MMLU and GPQA improvement claims; base 72B MMLU **86.1** | LiveCodeBench **55.5** | Qwen positions the family as strong across multilingual tasks; public page lists Multi-Exam, MGSM, BELEBELE, XCOPA, Flores evaluations | **128K** | Qwen2.5-72B uses Qwen License; smaller dense variants mostly Apache 2.0 | Best current open-weight choice when you want strong coding plus long context without DeepSeek-scale deployment cost. |
| [Gemma 3 27B IT](https://ai.google.dev/gemma/docs/core/model_card_3) | Official model card with benchmark tables | GPQA Diamond **42.4**, MMLU-Pro **67.5** | LiveCodeBench **29.7**, HumanEval **87.8** | Global-MMLU-Lite **75.1**; official support for **140+ languages** | **128K** | Custom Gemma terms rather than Apache/MIT | Excellent efficiency and multilingual reach for its size; weaker frontier reasoning than DeepSeek or top Qwen. |
| [Mistral Small 3.1](https://mistral.ai/news/mistral-small-3-1) | Official launch page; benchmark charts are visual rather than easily extractable as text | Vendor says it outperforms Gemma 3 and GPT-4o Mini in its weight class | No machine-readable exact coding scores on the page, but Mistral positions it as a top small open model | Explicit multilingual positioning | **128K** | **Apache 2.0** | Strong enterprise-friendly small model candidate because of size, speed, and permissive license. |
| [Codestral-2501](https://mistral.ai/news/codestral-2501) | Official Mistral benchmark table | Not a general reasoning model; use as coding specialist | HumanEval **86.6%**, MBPP **80.2%**, LiveCodeBench **37.9%**, RepoBench **38.0%**, HumanEvalFIM avg **85.9%** | Not the right benchmark target for multilingual/general tasks | **256K** | Commercial/open-weight via Mistral ecosystem; check deployment terms per channel | Best coding-specialist open-weight option in this set when code generation and FIM matter more than general reasoning. |

## How to Read the Table
- Not every vendor publishes the same benchmark suite in the same format.
- I have kept vendor-published benchmark numbers only where they were directly available from official text or official tables.
- You should not directly compare `HumanEval`, `LiveCodeBench`, `GPQA`, and `MMLU-Pro` as if they were one score; each measures a different dimension.

## Practical Shortlist by Use Case
### 1. Best all-round frontier open-weight model
- `DeepSeek-V3` remains the strongest evidence-backed frontier model in this set on reasoning, coding, and multilingual breadth.
- Tradeoff: it is operationally heavier and has a less frictionless license story than Apache-only models.

### 2. Best balance of performance and deployability
- `Qwen2.5-72B-Instruct` is the most balanced choice if you want strong coding, long context, and more practical self-hosting than DeepSeek-V3.
- `Gemma 3 27B` is the most attractive option when weight class, multilingual support, and infrastructure efficiency matter more than absolute frontier scores.

### 3. Best small-model enterprise option
- `Mistral Small 3.1` is the cleanest small-model enterprise candidate in this batch because of Apache 2.0 licensing, 128K context, and explicit emphasis on speed.

### 4. Best coding specialist
- `Codestral-2501` is the best coding-focused model here by explicit benchmark evidence.
- It should be benchmarked separately from general-purpose assistants rather than lumped into the same ranking.

## Recommendations
1. Use `DeepSeek-V3` as the benchmark ceiling for open-weight frontier quality, but do not assume it is the best enterprise deployment choice.
2. Use `Qwen2.5-72B-Instruct` as the default general-purpose shortlist candidate for self-hosted high-performance deployments.
3. Use `Gemma 3 27B` and `Mistral Small 3.1` as the strongest efficient-model options when licensing, latency, and infrastructure cost matter.
4. Keep `Codestral-2501` in a separate coding lane. It is not the right substitute for a general-purpose LLM, but it is highly relevant if developer workflows are central.

## Source Notes
- DeepSeek benchmarks and license: [DeepSeek-V3 GitHub README](https://github.com/deepseek-ai/DeepSeek-V3)
- Qwen2.5 model card and benchmark discussion: [Qwen2.5 LLM blog](https://qwenlm.github.io/blog/qwen2.5-llm/)
- Gemma 3 benchmarks and multilingual/context details: [Gemma 3 model card](https://ai.google.dev/gemma/docs/core/model_card_3)
- Mistral Small 3.1 context, license, speed, and model positioning: [Mistral Small 3.1](https://mistral.ai/news/mistral-small-3-1)
- Codestral-2501 coding benchmarks: [Codestral-2501](https://mistral.ai/news/codestral-2501)
