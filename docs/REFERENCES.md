# References

[Español](REFERENCES.es.md)

Every claim in this repository that comes from outside should trace back to an entry here. All sources were checked on 2026-11-02. The "How it was read" column says how much of each source was actually read, so nobody mistakes a summary for a verification.

## Sources

| ID | Source | Link | License or access | How it was read |
|---|---|---|---|---|
| R1 | *IssueTrojanBench: Benchmarking AI Coding Agents Against Malicious Issue Requests* (arXiv 2607.20759) | [arxiv.org/abs/2607.20759](https://arxiv.org/abs/2607.20759) | Paper: CC BY-NC-ND 4.0 | HTML read in full, apart from a summarized tail |
| R2 | IssueTrojanBench artifact, version 1.0.0, by "software-artifacts" | [Zenodo record](https://zenodo.org/records/22983053), DOI `10.5281/zenodo.22983053`. The paper's footnote DOI `10.5281/zenodo.19245678` redirected to this record. Code: [github.com/software-artifacts/IssueTrojanBench](https://github.com/software-artifacts/IssueTrojanBench) | CC BY 4.0 on Zenodo. GitHub detects no license in the code repository, which holds only a README | Archive downloaded by a BSA maintainer, and its MD5 matches the one Zenodo lists. Spreadsheets read without extraction in a container with no network. The GitHub README was opened by a BSA maintainer, not fetched by BSA |
| R3 | *INFUSE: A Unified Surface Benchmark for Indirect Prompt Injection in Agentic Systems* (arXiv 2610.20776), its [code](https://github.com/judydnguyen/infuse) and its trajectories on [Hugging Face](https://huggingface.co/datasets/judynguyen16/infuse-bench-trajectories) | [arxiv.org/abs/2610.20776](https://arxiv.org/abs/2610.20776) | Code: MIT. Trajectories: not available (the address answers 401) | HTML read up to section 3.2, the rest through a summary. The download script's header was read directly |
| R4 | *"Your AI, My Shell": Demystifying Prompt Injection Attacks on Agentic AI Coding Editors* (arXiv 2509.22040) and its [replication package](https://doi.org/10.6084/m9.figshare.30111988) | [arxiv.org/abs/2509.22040](https://arxiv.org/abs/2509.22040) | Package: CC BY 4.0, anonymous author | HTML read up to section V-A, the rest through a summary. The figshare page was opened in a browser |
| R5 | *Red-Teaming Coding Agents from a Tool-Invocation Perspective* (arXiv 2509.05755) | [arxiv.org/abs/2509.05755](https://arxiv.org/abs/2509.05755) | Artifact link is anonymous | HTML read to about 39,000 characters, the rest through a summary. The artifact link was not opened |
| R6 | *AgentDojo* (arXiv 2406.13352) | [arxiv.org/abs/2406.13352](https://arxiv.org/abs/2406.13352) | Code at github.com/ethz-spylab/agentdojo, license not checked | HTML read in part, the rest through a summary |
| R7 | *LivePI* (arXiv 2605.17986) | [arxiv.org/abs/2605.17986](https://arxiv.org/abs/2605.17986) | Not checked | Abstract and HTML, apart from the last 1,100 characters |
| R8 | *PIArena* (arXiv 2604.08499) | [arxiv.org/abs/2604.08499](https://arxiv.org/abs/2604.08499) | Code: MIT | Abstract only |
| R9 | *Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents* (arXiv 2605.16282) | [arxiv.org/abs/2605.16282](https://arxiv.org/abs/2605.16282) | Not checked | Abstract read directly, the body through a summary |
| R10 | *The Attacker Moves Second* (arXiv 2510.09023) | [arxiv.org/abs/2510.09023](https://arxiv.org/abs/2510.09023) | Not checked | Abstract-level only, through a search result. The paper itself was not read |
| R11 | Claude Code documentation: [hooks](https://code.claude.com/docs/en/hooks), [settings](https://code.claude.com/docs/en/settings), [security](https://code.claude.com/docs/en/security), [permissions](https://code.claude.com/docs/en/permissions), [sandboxing](https://code.claude.com/docs/en/sandboxing) | | Public documentation | Settings and security pages read verbatim. The hooks and permissions pages partly through summaries, and two statements on those pages disagree (see the note below) |
| R12 | Coding Agent Security Benchmark, Rogue Security | [huggingface.co/datasets/rogue-security/coding-agent-security-benchmark](https://huggingface.co/datasets/rogue-security/coding-agent-security-benchmark) | CC BY-NC 4.0 | Page opened in a browser and its card read. A second copy exists under another account with the same license, and its relation to the first was not verified |
| R13 | Nemotron RL Agentic Indirect Prompt Injection v1, NVIDIA | [huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1](https://huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1) | CC BY 4.0 | Card and file list read through the public API |
| R14 | ClawTrojan | [huggingface.co/datasets/zstanjj/ClawTrojan](https://huggingface.co/datasets/zstanjj/ClawTrojan) | "other", terms not specified | Card read through the public API |
| R15 | *The Magic Behind the Scenes of Docker Desktop*, Docker blog | [docker.com/blog](https://www.docker.com/blog/the-magic-behind-the-scenes-of-docker-desktop/) | Public blog post, date not checked | Text read through a script. It states that Docker Desktop has a lightweight LinuxKit VM that Docker manages, and that on Windows it uses the WSL 2 backend |

**Citing the IssueTrojanBench data.** software-artifacts. *IssueTrojanBench*, version 1.0.0. Zenodo. DOI 10.5281/zenodo.22983053. CC BY 4.0. The artifact's own citation entry names the 41st IEEE/ACM International Conference on Automated Software Engineering (2026) and anonymized authors, so this repository treats the paper as a preprint.

**About R11.** The settings page does not list hooks among the settings that wait for folder trust, while the hooks page says that interactive sessions hold hooks back until the folder is trusted. BSA did not resolve that difference.

## Claims that depend on these sources

| Claim | Where | Sources | Status |
|---|---|---|---|
| Published benchmarks aim these attacks at commercial agents such as Cursor and Claude Code | README, RELATED_WORK | R1, R5 | R1 names Cursor, Claude Code and Codex Desktop. R5 names Claude Code and Cursor among six agents |
| Sizes, repetitions and success criteria of the four closest benchmarks | RELATED_WORK | R1 to R5 | Sizes and repetitions checked in each text. Success criteria for R3 and R5 come from summaries |
| IssueTrojanBench ran each configuration once, and its results behave like 144 combinations | PUBLISHED_DATA, README | R2 | BSA's recalculation from the spreadsheets. The archive's MD5 matches Zenodo's, and `python scripts/analyze_published.py issuetrojanbench.zip` repeats it |
| Dataset availability and licenses | PUBLISHED_DATA | R2 to R4, R12 to R14 | Each page or API entry was opened or queried on 2026-11-02 |
| `docs/EEM_CRITERIA.md`, linked by the README, is in neither the archive nor the authors' GitHub repository | PUBLISHED_DATA | R2 | Checked in the archive's file list and, on 2026-11-02, in the GitHub API listing, which shows only a README |
| The authors' statements about forks, packages and reversible payloads | PUBLISHED_DATA | R2 | From the GitHub README, which a BSA maintainer opened |
| `claude --no-input --print` fails in Claude Code 2.1.306 | PUBLISHED_DATA | None, BSA's own test | Repeatable offline: `python scripts/arena.py up`, then `docker run --rm --network none bsa/agent:local claude --no-input --print hi` |
| Adaptive attacks beat defences with near-zero reported success | LIMITATIONS | R10 | Abstract-level only |
| Benchmark choice can yield contradictory conclusions, and lower-fidelity evaluations tend to report lower unsafe rates | LIMITATIONS, RELATED_WORK | R9 | The first part is in the abstract. The second comes from a summary of the body |
| How Claude Code treats `disableAllHooks`, managed hooks and `-p` | RESULTS | R11 | Partly through summaries, see the note on R11 |
| On Docker Desktop the containers run in a Linux virtual machine managed by Docker | LIMITATIONS | R15 | Read in the source. It is an older post: it still describes HyperKit on Mac, and Docker has changed backends since |
| Containers share the host's kernel | LIMITATIONS, arena README | None | A general fact about containers, **not sourced here** |

Measurements in [RESULTS.md](RESULTS.md) are BSA's own and can be repeated with the commands shown there.
