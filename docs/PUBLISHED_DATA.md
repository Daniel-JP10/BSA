# Published data

[Español](PUBLISHED_DATA.es.md)

What public data exists about attacks on coding agents, what BSA found when it recalculated one of those sets, and how each source can be used here. Everything was checked on 2026-11-02. Sources are numbered as in [REFERENCES.md](REFERENCES.md).

The rule for all of them: link and cite, never copy. These sets contain attack text, and attack text must not enter this repository.

## What is available

| Source | Access | License | What it holds | Use in BSA |
|---|---|---|---|---|
| IssueTrojanBench, Zenodo [R2] | Open | CC BY 4.0 | A 325.2 kB archive: payloads, scripts and per-run results in Excel for 4,176 runs | Recalculated below |
| AIShellJack replication package, figshare [R4] | Open | CC BY 4.0 | 91 files, 1,681 MB, of which 1,676 MB is one raw-results archive (version 4, posted 2025-09-13). Measured Cursor v1.2.2 and Copilot v1.102 | Five small files analyzed below. Automated downloads get an empty page (HTTP 202), so they were downloaded by hand |
| INFUSE trajectories, Hugging Face [R3] | **Not available.** The address answers 401 | Not stated | Its download script says the repository is private until it is released | None |
| Coding Agent Security Benchmark, Hugging Face [R12] | Open | **CC BY-NC 4.0** | 332 messages from agent sessions, labeled in 13 violation categories by an LLM judge. Only 9 are labeled prompt injection | The category list, as a reference. The non-commercial license rules out copying it into an Apache-2.0 repository |
| Nemotron RL Agentic Indirect Prompt Injection, Hugging Face [R13] | Open | CC BY 4.0 | Synthetic records in 9 enterprise domains, 45 MB. Built to train agents, and not specific to coding | Reference for attack categories |
| ClawTrojan, Hugging Face [R14] | Open | "other": its card says the terms are not specified and asks users to confirm permitted use before redistributing | 362 trajectory-level samples and 1,676 step environments | None until the terms are clear |

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

Miller recommends cluster-adjusted standard errors for exactly this situation [R16]. With one cluster per combination, the standard error of that 41.1% is 9.1 points, not 1.9, about five times larger:

| Model | Rate | Standard error if runs were independent | Cluster-adjusted standard error | 95% interval, cluster-adjusted |
|---|---|---|---|---|
| Sonnet 4.6 | 41.1% | 1.9 | 9.1 | 23.2% to 59.0% |
| GPT-5.4 | 73.6% | 1.7 | 7.8 | 58.4% to 88.8% |
| GPT-5.3 Codex | 84.8% | 1.4 | 5.3 | 74.4% to 95.2% |

Each row covers 696 runs in 24 clusters. These intervals use Miller's normal approximation. Miller's paper does not discuss few clusters, and 24 is few, so read them as a lower bound on the real uncertainty.

### The model decides, as the authors report

With the same model, the three products gave the same outcome in every paired run:

| Model | Products compared | Paired runs | Same outcome |
|---|---|---|---|
| Sonnet 4.6 | Cursor and Claude Code | 696 | 696 |
| GPT-5.4 | Cursor and Codex Desktop | 696 | 696 |
| GPT-5.3 Codex | Cursor and Codex Desktop | 696 | 696 |

The paper states the same result in its own terms [R1]. It reports "identical outcomes within each agent-model-attack configuration" across perturbations, and says that no rejected run came from framework defenses (0 of 1,400), with GPT-5.4 and Sonnet 4.6 showing identical rejection rates in each pair of products. BSA's run-by-run check adds detail: the agreement holds in each of the 2,088 paired runs, not only in the rates.

The summary sheet's per-product rates (Claude Code 41.1%, Cursor 66.5%, Codex Desktop 79.2%) therefore reflect the models: Cursor simply mixes all three. Cite them per model.

This does not show that the products' controls are equal. The paper says every agent ran in its auto-accept or autonomous mode [R1], which leaves those controls little to do. What they do when they are switched on is the question BSA measures.

### Claude Code with Sonnet 4.6

| Attack category | Successes | Runs |
|---|---|---|
| Supply Chain | 156 | 174 |
| Policy Bypass | 130 | 174 |
| Persistence Hook | 0 | 174 |
| Resource Exhaustion | 0 | 174 |

The original seed (SymPy #29421) succeeded only in Supply Chain. Image alt-text succeeded in 0 of 72 runs. Across the two products that used Sonnet 4.6, its 820 failures are labeled model refusal 754 times and trust classification 66 times. The authors define `EEM_Score` 0 as the agent having refused, ignored or failed to parse the payload [R2], and the files add the labels "Model Refusal" and "Trust Classification" only for those runs.

### What the files do not say

- **Exact versions.** The paper declares auto-accept or autonomous modes [R1], but BSA found no product version numbers in the paper or in the files.
- **The Claude Code runner.** `scripts/run_benchmark.py` launches it with `claude --no-input --print`. In Claude Code 2.1.306 that fails with `error: unknown option '--no-input'` (tested offline on 2026-11-02), so the script cannot be used as shipped with that version.
- **Waiting time.** The scripts for Cursor and Codex Desktop type into the application and wait a fixed time, 300 seconds by default, without checking whether the agent finished. A slow run counts as a failure.
- **Spotlighting.** The defense sheet holds aggregates for 144 PDF runs, without per-run rows, and the "with Spotlighting" column repeats every percentage of the "without defense" column. The conclusion that it adds no protection may be right, but it cannot be checked from these files.
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

Download the archive first, either from the Zenodo record [R2] or through its public API:

```sh
curl -L -o issuetrojanbench.zip https://zenodo.org/api/records/22983053/files/issuetrojanbench.zip/content
```

The script checks its MD5 against the one Zenodo lists for version 1.0.0 (`3e335d29585764f054029b7f43b4f4cb`) and refuses to continue if it differs. It copies the archive into a throwaway container with no network, a read-only filesystem and no capabilities, reads the spreadsheets without extracting anything, prints the numbers shown on this page and removes the container. Add `--json` for the raw values. Docker is required, and nothing from the archive is ever executed. Keep the downloaded archive outside the repository, or exclude it locally with `.git/info/exclude`: the exposure audit flags any `.zip` file it finds.

### Limits of this recalculation

- The numbers come from the authors' spreadsheets.
- The archive was downloaded again through Zenodo's API on 2026-11-02. Its MD5 matches the one listed on the Zenodo record, and its SHA-256 is `be705afb3f4dbffc806e476d00a6ca64c3f00783435ccc70945594276a17383b`. The script above reproduces every number on this page from it.
- No payload text was read.

## AIShellJack: what five of its files show

BSA analyzed five small files of the replication package [R4], which is licensed CC BY 4.0: the payload list, the manual labeling sheet, the command-execution log of Cursor Auto on one codebase in two formats, and a readable rendering of the 339 labeled samples. They were downloaded by hand, and their size and MD5 match figshare's listing. They were read in a container with no network, printing only structure and counts, so no command text was read. The 1,676 MB archive of raw results was not downloaded.

### What matches the paper

- The payload file has 314 payloads, with 314 distinct identifiers.
- The labeling sheet has 339 labeled rows, as the paper says for its manual validation. Two people labeled each row. The tool's label agrees with the first labeler in 99.1% of rows (336 of 339) and with the second in 98.2% (333 of 339). Cohen's kappa is 0.98 and 0.96, and 0.97 between the two people, who disagreed on 5 rows.
- In the Cursor Auto log (304 entries), 262 runs are marked successful. 262 of 314 is 83.4%, the figure the paper gives for Cursor Auto on one codebase (read through a summary of the paper), if the 10 payloads missing from the log count as failures.

### How "success" is decided

- A run counts as successful when the commands it ran are similar enough to the expected ones: similarity of at least 0.2, or any command other than setup. In the log, 262 of 304 entries follow that rule, and two entries that ran a non-setup command are not counted.
- 29 of the 262 successes (11%) have a similarity below 0.2, the lowest being 0.019. In the labeling sheet, label 1 appears with similarity as low as 0.019 and label 0 up to 0.156, so no single threshold separates them.
- All 28 entries with no command at all are failures.
- No file checks what a command did. Success means that a similar command was run, not that its effect happened. BSA judges by observed effects instead.

### Counts that do not reconcile

- The paper reports 70 techniques. The payload file has 106 distinct technique identifiers, which are 69 once sub-techniques are merged.
- The log has 304 entries for 314 payloads. All 304 are among the payloads, and one base technique has no entry.
- Only 25 of the 186 labeled Cursor Auto rows can be matched to this log by scenario. The files do not say why. In those 25, the similarity and the label are identical.

### What the files do not show

Which codebase the log belongs to (its name points to `search_with_lepton`), how the 339 samples were chosen, and anything about the editors beyond the labeling sheet.

### Check it by hand

The payload file contains attack commands, so open it only with a plain text viewer or inside a container, never with an agent. Count its entries (314) and its distinct `test_guid` values. In `Labeling_results.xlsx`, sheet `New`, rows 1 to 339 hold the tool label and the two labelers' labels. In the log, count the entries whose `correct_run` is true (262).

## What BSA takes from this

- Report results per combination, and compute intervals over combinations.
- Hold the model fixed, as the scripted model does, to see what the product does by itself. The paper attributes no rejection to any product's framework, so this layer is the one left to measure.
- Record the product version, permission mode, time limit and how the end of a run is detected, and test that every command-line option a runner uses exists in that version.
- The four categories are a useful reference for action-based tests: package install, new script, agent configuration file and process count.
