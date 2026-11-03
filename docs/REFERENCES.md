# References

[Español](REFERENCES.es.md)

Every claim in this repository that comes from outside should trace back to an entry here. All sources were checked on 2026-11-02. The "How it was read" column says how much of each source was actually read, so nobody mistakes a summary for a verification.

## Sources

| ID | Source | Link | License or access | How it was read |
|---|---|---|---|---|
| R1 | *IssueTrojanBench: Benchmarking AI Coding Agents Against Malicious Issue Requests* (arXiv 2607.20759) | [arxiv.org/abs/2607.20759](https://arxiv.org/abs/2607.20759) | Paper: CC BY-NC-ND 4.0 | HTML read in full, apart from a summarized tail. The passages quoted in PUBLISHED_DATA were read directly |
| R2 | IssueTrojanBench artifact, version 1.0.0, by "software-artifacts" | [Zenodo record](https://zenodo.org/records/22983053), version DOI `10.5281/zenodo.22983053`, concept DOI `10.5281/zenodo.19245678`, which is the one in the paper's footnote. Code: [github.com/software-artifacts/IssueTrojanBench](https://github.com/software-artifacts/IssueTrojanBench) | CC BY 4.0 on Zenodo. GitHub detects no license in the code repository, which holds only a README | Archive downloaded through Zenodo's public API, and its MD5 matches the one Zenodo lists. Spreadsheets read without extraction in a container with no network. The GitHub README was opened by a BSA maintainer, not fetched by BSA |
| R3 | *INFUSE: A Unified Surface Benchmark for Indirect Prompt Injection in Agentic Systems* (arXiv 2610.20776), its [code](https://github.com/judydnguyen/infuse) and its trajectories on [Hugging Face](https://huggingface.co/datasets/judynguyen16/infuse-bench-trajectories) | [arxiv.org/abs/2610.20776](https://arxiv.org/abs/2610.20776) | Code: MIT. Trajectories: not available (the address answers 401) | HTML read up to section 3.2, the rest through a summary. The download script's header was read directly |
| R4 | *"Your AI, My Shell": Demystifying Prompt Injection Attacks on Agentic AI Coding Editors* (arXiv 2509.22040) and its [replication package](https://doi.org/10.6084/m9.figshare.30111988) | [arxiv.org/abs/2509.22040](https://arxiv.org/abs/2509.22040) | Package: CC BY 4.0, anonymous author | HTML read up to section V-A, the rest through a summary. The figshare page was opened in a browser. Five files were downloaded by hand, with MD5 and size matching figshare's listing, and read in a container with no network, structure and counts only |
| R5 | *Red-Teaming Coding Agents from a Tool-Invocation Perspective* (arXiv 2509.05755) | [arxiv.org/abs/2509.05755](https://arxiv.org/abs/2509.05755) | Artifact link is anonymous | HTML read to about 39,000 characters, the rest through a summary. The artifact link was not opened |
| R6 | *AgentDojo* (arXiv 2406.13352) | [arxiv.org/abs/2406.13352](https://arxiv.org/abs/2406.13352) | Code at github.com/ethz-spylab/agentdojo, license not checked | HTML read in part, the rest through a summary |
| R7 | *LivePI* (arXiv 2605.17986) | [arxiv.org/abs/2605.17986](https://arxiv.org/abs/2605.17986) | Not checked | Abstract and HTML, apart from the last 1,100 characters |
| R8 | *PIArena* (arXiv 2604.08499) | [arxiv.org/abs/2604.08499](https://arxiv.org/abs/2604.08499) | Code: MIT | Abstract only |
| R9 | *Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents* (arXiv 2605.16282) | [arxiv.org/abs/2605.16282](https://arxiv.org/abs/2605.16282) | Not checked | Abstract read directly, the body through a summary |
| R10 | *The Attacker Moves Second* (arXiv 2510.09023) | [arxiv.org/abs/2510.09023](https://arxiv.org/abs/2510.09023) | Not checked | Abstract-level only, through a search result. The paper itself was not read |
| R11 | Claude Code documentation: [hooks](https://code.claude.com/docs/en/hooks), [settings](https://code.claude.com/docs/en/settings), [security](https://code.claude.com/docs/en/security), [permissions](https://code.claude.com/docs/en/permissions), [sandboxing](https://code.claude.com/docs/en/sandboxing), [permission modes](https://code.claude.com/docs/en/permission-modes) | | Public documentation | Settings and security pages read verbatim. The quoted sentences of the permission modes page were read directly, and the rest of it through a summary. The hooks and permissions pages partly through summaries, and two statements on those pages disagree (see the note below) |
| R12 | Coding Agent Security Benchmark, Rogue Security | [huggingface.co/datasets/rogue-security/coding-agent-security-benchmark](https://huggingface.co/datasets/rogue-security/coding-agent-security-benchmark) | CC BY-NC 4.0 | Page opened in a browser and its card read. |
| R13 | Nemotron RL Agentic Indirect Prompt Injection v1, NVIDIA | [huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1](https://huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1) | CC BY 4.0 | Card and file list read through the public API |
| R14 | ClawTrojan | [huggingface.co/datasets/zstanjj/ClawTrojan](https://huggingface.co/datasets/zstanjj/ClawTrojan) | "other", terms not specified | Card read through the public API |
| R15 | Docker documentation: [Docker Engine security](https://docs.docker.com/engine/security/), [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/), [Docker Desktop on Linux](https://docs.docker.com/desktop/setup/install/linux/), [Compose networks](https://docs.docker.com/reference/compose-file/networks/) | | Public documentation | The quoted sentences were read in each page |
| R16 | Evan Miller, *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations* (arXiv 2411.00640) | [arxiv.org/abs/2411.00640](https://arxiv.org/abs/2411.00640) | Not checked | Abstract and formulas read in the HTML version. Its author lists an Anthropic affiliation |
| R17 | *From Approval to Abuse: Privilege Escalation Attacks on Harness-Protected Coding Agents* (arXiv 2610.22987) | [arxiv.org/abs/2610.22987](https://arxiv.org/abs/2610.22987) | Not checked | Abstract only |
| R18 | *AgentDrift: A Step-Labeled Benchmark of Injection-Hijacked LLM Agent Trajectories* (arXiv 2609.06972) | [arxiv.org/abs/2609.06972](https://arxiv.org/abs/2609.06972) | Corpus: CC BY 4.0, according to the abstract | Abstract only |
| R19 | *Breaking Claude Code Opus 5 Auto Mode*, Embrace The Red, 2026-08-26 | [embracethered.com](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/) | Public blog post | Post read. Its video and screenshots were not checked, and the vendor's reply is as the author reports it |
| R20 | OWASP Top 10 for LLM Applications 2025: [LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) | | Public pages | Both pages read |
| R21 | Vulnerability records: [CVE-2025-55284](https://nvd.nist.gov/vuln/detail/CVE-2025-55284), [CVE-2025-54135](https://nvd.nist.gov/vuln/detail/CVE-2025-54135), [CVE-2025-61591](https://nvd.nist.gov/vuln/detail/CVE-2025-61591), [CVE-2025-62222](https://nvd.nist.gov/vuln/detail/CVE-2025-62222), [CVE-2026-31854](https://nvd.nist.gov/vuln/detail/CVE-2026-31854), [GHSA-ff64-7w26-62rf](https://github.com/advisories/GHSA-ff64-7w26-62rf), [GHSA-5hhx-v7f6-x7gv](https://github.com/advisories/GHSA-5hhx-v7f6-x7gv) | | Public records | Read through the NVD and GitHub Advisory APIs |
| R22 | Claude Code [issue 26637](https://github.com/anthropics/claude-code/issues/26637), *disableAllHooks bypasses managed organization hooks*, and the [npm version history](https://www.npmjs.com/package/@anthropic-ai/claude-code?activeTab=versions) | | Public | Issue read through the GitHub API, including the reporter's comment naming 2.1.49 as the fix. Dates from the npm registry |

**Citing the IssueTrojanBench data.** software-artifacts. *IssueTrojanBench*, version 1.0.0. Zenodo. DOI 10.5281/zenodo.22983053. CC BY 4.0. Its citation entry names ASE 2026 with anonymized authors, so the paper is treated here as a preprint.

**About R11.** The settings page does not list hooks among the settings that wait for folder trust, while the hooks page says that interactive sessions hold hooks back until the folder is trusted. BSA did not resolve that difference.

## Claims that depend on these sources

| Claim | Where | Sources | Status |
|---|---|---|---|
| Published benchmarks aim these attacks at commercial agents such as Cursor and Claude Code | README, RELATED_WORK | R1, R5 | R1 names Cursor, Claude Code and Codex Desktop. R5 names Claude Code and Cursor among six agents |
| The paper's statements on identical outcomes, 0 of 1,400 framework rejections and auto-accept modes | PUBLISHED_DATA, README | R1 | Read in the HTML text |
| Cluster-adjusted standard errors and their formula | PUBLISHED_DATA, `bsa/stats.py` | R16 | Equation 4 and appendix A read directly. The paper uses a normal approximation and does not discuss few clusters |
| Allow-rule escalation, the 2026 Auto Mode report and step-labeled trajectories | RELATED_WORK | R17, R18, R19 | Figures quoted from each abstract or post, not repeated by BSA |
| The issue that let `.claude/settings.local.json` switch off managed hooks, fixed in 2.1.49 | RESULTS, RELATED_WORK | R22 | Read in the issue. What BSA observed is in the version comparison in RESULTS |
| Before 2.1.302, `claude -p` could start in auto mode when it did not fetch feature flags | RESULTS | R11 | Quoted from the permission modes page |
| Published vulnerabilities in the threat model | THREAT_MODEL | R21 | Dates, weaknesses and affected versions as listed in each record |
| OWASP categories | THREAT_MODEL | R20 | The mapping to BSA's tests is BSA's own |
| Sizes, repetitions and success criteria of the four closest benchmarks | RELATED_WORK | R1 to R5 | Sizes and repetitions checked in each text. Success criteria for R3 and R5 come from summaries |
| IssueTrojanBench ran each configuration once, and its results behave like 144 combinations | PUBLISHED_DATA, README | R2 | BSA's recalculation from the spreadsheets. The archive's MD5 matches Zenodo's, and `python scripts/analyze_published.py issuetrojanbench.zip` repeats it |
| AIShellJack's payload count, labeling agreement and how its success label behaves | PUBLISHED_DATA | R4 | BSA's own reading of five files downloaded by hand. Their MD5 and size match figshare's listing |
| 262 of 314 equals the Cursor Auto figure the paper reports for one codebase | PUBLISHED_DATA | R4 | The paper's figure was read through a summary, so check the original |
| Dataset availability and licenses | PUBLISHED_DATA | R2 to R4, R12 to R14 | Each page or API entry was opened or queried on 2026-11-02 |
| `docs/EEM_CRITERIA.md`, linked by the README, is in neither the archive nor the authors' GitHub repository | PUBLISHED_DATA | R2 | Checked in the archive's file list and, on 2026-11-02, in the GitHub API listing, which shows only a README |
| The authors' statements about forks, packages and reversible payloads | PUBLISHED_DATA | R2 | From the GitHub README, which a BSA maintainer opened |
| `claude --no-input --print` fails in Claude Code 2.1.306 | PUBLISHED_DATA | None, BSA's own test | Repeatable offline: `python scripts/arena.py up`, then `docker run --rm --network none bsa/agent:2.1.306 claude --no-input --print hi` |
| Adaptive attacks beat defenses with near-zero reported success | LIMITATIONS | R10 | Abstract-level only |
| Benchmark choice can yield contradictory conclusions, and lower-fidelity evaluations tend to report lower unsafe rates | LIMITATIONS, RELATED_WORK | R9 | The first part is in the abstract. The second comes from a summary of the body |
| How Claude Code treats `disableAllHooks`, managed hooks and `-p` | RESULTS | R11 | Partly through summaries, see the note on R11 |
| Default container settings may give incomplete isolation, alone or with kernel vulnerabilities, and WSL 2 distributions share one kernel | LIMITATIONS, arena README | R15 | Quoted from Docker's security and WSL pages |

Measurements in [RESULTS.md](RESULTS.md) are BSA's own and can be repeated with the commands shown there.
