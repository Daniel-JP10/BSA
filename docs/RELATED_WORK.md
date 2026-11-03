# Related work

[Español](RELATED_WORK.es.md)

Reviewed in November 2026. For the four benchmarks closest to BSA, sizes and repetition counts were checked against each paper's text, and the artifact links were opened, except the Red-Teaming link. The "how success is judged" column for INFUSE and Red-Teaming comes from a summary of the paper. The general benchmarks were read from their abstracts or pages. Check the originals before quoting. Numbered sources are in [REFERENCES.md](REFERENCES.md), and the published IssueTrojanBench results were also recalculated: see [Published data](PUBLISHED_DATA.md).

## Benchmarks closest to BSA

| Work | Agents run | Size | How success is judged | Repetitions | Public artifact |
|---|---|---|---|---|---|
| [INFUSE](https://arxiv.org/abs/2610.20776) | Mini-SWE-Agent; replay on Claude Code and Codex CLI | 40 tasks, 56 attacks, 5 categories | LLM judge plus heuristic checks in the container | One trajectory per cell | [Code](https://github.com/judydnguyen/infuse) |
| [IssueTrojanBench](https://arxiv.org/abs/2607.20759) | Cursor, Claude Code, Codex Desktop | 696 artifacts, 4,176 runs | Marker files created by the agent, checked by the runner | One run per configuration, checked in the published results | [Zenodo](https://doi.org/10.5281/zenodo.19245678) |
| [AIShellJack](https://arxiv.org/abs/2509.22040) | Cursor, GitHub Copilot | 314 payloads, 70 ATT&CK techniques | Matching logged commands | Each test ran once | [figshare](https://doi.org/10.6084/m9.figshare.30111988) |
| [Red-Teaming Coding Agents](https://arxiv.org/abs/2509.05755) | Six real coding agents, including Claude Code and Cursor | 25 agent-model pairs | Tool invocation with the intended payload | 10 attempts per pair in its prompt-leak phase | Anonymous link |

IssueTrojanBench's artifact lists the 41st IEEE/ACM International Conference on Automated Software Engineering (2026) with anonymized authors in its citation entry, so this repository treats it as a preprint.

## General agent benchmarks

| Work | Scope | Note for BSA |
|---|---|---|
| [AgentDojo](https://arxiv.org/abs/2406.13352) | Simulated workspace, Slack, travel and banking | Deterministic security checks, and an explicit rejection of LLM judges. A methodological reference for BSA, not a coding agent test |
| [LivePI](https://arxiv.org/abs/2605.17986) | Real OpenClaw on a real virtual machine | Live environment, with an LLM judge plus artifact inspection |
| [PIArena](https://arxiv.org/abs/2604.08499) | Unified platform over existing benchmarks | Adaptive, feedback-based attacks |
| [Taxonomy of 40 safety benchmarks](https://arxiv.org/abs/2605.16282) | Survey | Reports that benchmark choice can yield contradictory conclusions, and that coverage counts often overstate depth |
| [AgentDrift](https://arxiv.org/abs/2609.06972) | 12,536 synthetic trajectories, 71,024 labeled steps | A corpus for training detectors, which labels the step where an injection enters. It runs no product |

## Reports on the controls themselves

| Work | What it reports | Note for BSA |
|---|---|---|
| [From Approval to Abuse](https://arxiv.org/abs/2610.22987) | Text planted in a repository steers an agent into asking for a broad allow-rule. Across products including Claude Code and Codex CLI, agents elicited the target rule in 58% of instances, and with the rule approved, 47 of 58 eligible instances reached their goal silently | Approval is a control that can be attacked. BSA has not measured this, because it needs a person's decision |
| [Breaking Claude Code Opus 5 Auto Mode](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/) | Lab runs by the author with small samples (3 of 5, 3 of 5 and 4 of 5). As the author tells it, the vendor closed the report as informative and pointed to operating-system isolation and network egress control as the real boundary | BSA's matrix leaves auto mode out, since it depends on a classifier the scripted model cannot stand in for |

## What BSA takes from them, and where it parts ways

From these works BSA takes deterministic checks instead of LLM judges (AgentDojo), containers with simulated destinations (INFUSE), verdicts based on files and other effects (IssueTrojanBench), and the idea of organizing attacks into families.

It does not repeat them. Those benchmarks fool a real model and count how often it obeys, which measures the model first. BSA replaces the model with a script that asks for the risky action, as a model that has already been fooled would, and measures what the product's controls do next. That needs no attack text and no account, and it gives the same answer on every run.

## The gap BSA aims at

No single work reviewed here combines all of the following on closed commercial agents:

1. Real side effects checked by an independent observer, inside an isolated environment.
2. Repeated runs with confidence intervals.
3. A permission mode matrix.
4. Pinned versions, re-run over time to show drift.
5. Utility and false positive measurements for product-level defenses.
6. The product's effect separated from the model's effect. The IssueTrojanBench authors report that no rejection came from a product's framework, and that the same model gave the same results across products ([details](PUBLISHED_DATA.md)).

This is a statement about the works listed here, not about everything published. Today BSA covers points 1, 3, 4 and 6 for one agent, with a scripted model: see the [control matrix](RESULTS.md#control-matrix) and the [version comparison](RESULTS.md#the-same-contracts-across-versions). Point 2 does not apply to deterministic controls yet, and point 5 is not done.
