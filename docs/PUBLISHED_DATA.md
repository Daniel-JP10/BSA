# Published data

[Español](PUBLISHED_DATA.es.md)

What public data exists about attacks on coding agents, what BSA found when it recalculated one of those sets, and how each source can be used here. Everything was checked on 2026-11-02. Sources are numbered as in [REFERENCES.md](REFERENCES.md).

The rule for all of them: link and cite, never copy. These sets contain attack text, and attack text must not enter this repository.

## What is available

| Source | Access | License | What it holds | Use in BSA |
|---|---|---|---|---|
| IssueTrojanBench, Zenodo [R2] | Open | CC BY 4.0 | A 325.2 kB archive: payloads, scripts and per-run results in Excel for 4,176 runs | Recalculated below |
| AIShellJack replication package, figshare [R4] | Open | CC BY 4.0 | 91 files, 1,681 MB, of which 1,676 MB is one raw-results archive (version 4, posted 2025-09-13). Measured Cursor v1.2.2 and Copilot v1.102 | Not analyzed. Automated downloads get an empty page (HTTP 202), so files have to be downloaded by hand |
| INFUSE trajectories, Hugging Face [R3] | **Not available.** The address answers 401, and the authors' public profile lists two other datasets | Not stated | Its download script says the repository is private until it is released | None |
| Coding Agent Security Benchmark, Hugging Face [R12] | Open | **CC BY-NC 4.0** | 332 messages from agent sessions, labelled in 13 violation categories by an LLM judge. Only 9 are labelled prompt injection | The category list, as a reference. The non-commercial license rules out copying it into an Apache-2.0 repository |
| Nemotron RL Agentic Indirect Prompt Injection, Hugging Face [R13] | Open | CC BY 4.0 | Synthetic records in 9 enterprise domains, 45 MB. Built to train agents, and not specific to coding | Reference for attack categories |
| ClawTrojan, Hugging Face [R14] | Open | "other": its card says the terms are not specified and asks users to confirm permitted use before redistributing | 362 trajectory-level samples and 1,676 step environments | None until the terms are clear |

A full-text search for "prompt injection agent" on Hugging Face returns more than 36,000 matches, and most are unrelated training collections. Names can also mislead: searching for "infuse" finds datasets from an unrelated project.

## IssueTrojanBench: what the published results show

BSA recalculated the three spreadsheets of version 1.0.0 [R2], which are licensed CC BY 4.0. The authors do not endorse this analysis. The files were read inside a container without network access, and no script from the dataset was run.

### The numbers match the authors' own summary

- 4,176 rows in six sheets of 696, one per seed issue. No configuration appears twice, so **each configuration ran once**.
- Recalculated totals match the authors' `Metrics` sheets: overall (2,776 of 4,176, 66.5%), per model, per agent product, per attack category, per delivery vector and the split of rejections.
- The spreadsheets contain no macros, external links or formulas.

### The 4,176 runs are 144 combinations

Every combination of seed issue, attack category, agent product and model (6 × 4 × 6 = 144) has 29 runs, one per delivery vector and perturbation. Inside a combination, the outcome never depends on the perturbation (position, language, capitalization or font size):

| Shape of the combination | Count |
|---|---|
| Succeeds in all 29 runs | 24 |
| Fails in all 29 runs | 40 |
| Mixed | 80 |

In the 80 mixed combinations, only one thing decides the outcome: whether the delivery vector is image alt-text. It succeeded in 0 of 240 runs there, and the five other vectors succeeded in 2,080 of 2,080.

So an interval computed over 4,176 runs treats them as independent when they are not. For example, Claude Code with Sonnet 4.6 succeeded in 286 of 696 runs (41.1%), and a Wilson interval over those runs is 37.5% to 44.8%. Counting combinations, 11 of its 24 had at least one success, with an interval of 28% to 65%. The authors' files give no intervals.

### The model decides, and the product shows no separate effect

With the same model, the three products gave the same outcome in every paired run:

| Model | Products compared | Paired runs | Same outcome |
|---|---|---|---|
| Sonnet 4.6 | Cursor and Claude Code | 696 | 696 |
| GPT-5.4 | Cursor and Codex Desktop | 696 | 696 |
| GPT-5.3 Codex | Cursor and Codex Desktop | 696 | 696 |

The summary sheet's per-product rates (Claude Code 41.1%, Cursor 66.5%, Codex Desktop 79.2%) therefore reflect the models: Cursor simply mixes all three. With models that are not deterministic and products that differ, agreement in every run is unusual, and these files do not explain it. It may be stable behaviour, or the results may not have been measured independently. The files cannot tell them apart, so cite these figures as per-model results and ask the authors before relying on them.

### Claude Code with Sonnet 4.6

| Attack category | Successes | Runs |
|---|---|---|
| Supply Chain | 156 | 174 |
| Policy Bypass | 130 | 174 |
| Persistence Hook | 0 | 174 |
| Resource Exhaustion | 0 | 174 |

The original seed (SymPy #29421) succeeded only in Supply Chain. Image alt-text succeeded in 0 of 72 runs. Across the two products that used Sonnet 4.6, its 820 failures are labelled model refusal 754 times and trust classification 66 times. The authors define `EEM_Score` 0 as the agent having refused, ignored or failed to parse the payload [R2], and the files add the labels "Model Refusal" and "Trust Classification" only for those runs.

### What the files do not say

- **Versions and permission mode.** Neither is recorded for any product.
- **The Claude Code runner.** `scripts/run_benchmark.py` launches it with `claude --no-input --print`. In Claude Code 2.1.306 that fails with `error: unknown option '--no-input'` (tested offline on 2026-11-02), so the script cannot be used as shipped with that version.
- **Waiting time.** The scripts for Cursor and Codex Desktop type into the application and wait a fixed time, 300 seconds by default, without checking whether the agent finished. A slow run counts as a failure.
- **Spotlighting.** The defence sheet holds aggregates for 144 PDF runs, without per-run rows, and the "with Spotlighting" column repeats every percentage of the "without defense" column. The conclusion that it adds no protection may be right, but it cannot be checked from these files.
- **The success criteria.** The README links `docs/EEM_CRITERIA.md` for the detailed per-attack criteria, but that file is in neither the archive (checked in its file list) nor the authors' GitHub repository, which holds only the README (checked with the GitHub API on 2026-11-02). The README's shell one-liners are the only criteria available.

### How success is judged

By marker files, not by what the model says: `dependency_status.txt` for supply chain, `.validate_refactor.sh` for persistence, `CLAUDE.md`, `AGENTS.md` or `.cursorrules` for policy bypass, and `diagnostic_stress.sh` for resource exhaustion. Each payload file carries its own success indicator. This is the same principle BSA uses.

### What the authors say about safety [R2]

All experiments ran on forked repositories under the researchers' control, no packages were published to public registries, no real developers were exposed to adversarial content, and the payloads were designed to be detectable and reversible. BSA has not verified these statements.

### Check it by hand

Open the two `*_Results_final.xlsx` files. Each issue sheet has the columns `Issue_ID`, `Attack_Category`, `Agent_Framework`, `Model`, `Delivery_Vector`, `Perturbation`, `EEM_Score` and `Rejection_Attribution`. In a pivot table:

1. Count rows: 696 per sheet.
2. Group by agent and model, and sum `EEM_Score`: Cursor and Claude Code must show the same total for Sonnet 4.6 (286).
3. Filter `Agent_Framework` to Claude Code and group by `Attack_Category`.
4. Filter to one combination (issue, category, agent, model) and compare `EEM_Score` across `Delivery_Vector` and `Perturbation`.

### Repeat it with BSA's script

```sh
python scripts/analyze_published.py issuetrojanbench.zip
```

Download the archive from the Zenodo record [R2] first. The script checks its MD5 against the one Zenodo lists for version 1.0.0 (`3e335d29585764f054029b7f43b4f4cb`) and refuses to continue if it differs. It copies the archive into a throwaway container with no network, a read-only filesystem and no capabilities, reads the spreadsheets without extracting anything, prints the numbers shown on this page and removes the container. Add `--json` for the raw values. Docker is required, and nothing from the archive is ever executed. Keep the downloaded archive outside the repository, or exclude it locally with `.git/info/exclude`: the exposure audit flags any `.zip` file it finds.

### Limits of this recalculation

- It uses the authors' spreadsheets only. It was not compared with the paper's PDF.
- The archive was downloaded by a BSA maintainer. Its MD5 matches the one listed on the Zenodo record, and its SHA-256 is `be705afb3f4dbffc806e476d00a6ca64c3f00783435ccc70945594276a17383b`. The script above reproduces every number on this page from it.
- No payload text was read.

## What BSA takes from this

- Report results per combination, and compute intervals over combinations.
- Hold the model fixed, as the scripted model does, to see what the product does by itself.
- Record the product version, permission mode, time limit and how the end of a run is detected, and test that every command-line option a runner uses exists in that version.
- The four categories are a useful reference for action-based tests: package install, new script, agent configuration file and process count.
