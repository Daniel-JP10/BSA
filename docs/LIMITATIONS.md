# Limitations

[Español](LIMITATIONS.es.md)

What BSA cannot do yet, and what it may never prove.

- **A scripted model is not a fooled model.** It asks for one action per run. Real attacks chain steps and hide their intent, and the matrix does not measure that. It shows what a control does with a request, not how likely that request is.
- **No person in the loop.** Non-interactive runs refuse what a person would be asked about. How people answer approval prompts, which [From Approval to Abuse](https://arxiv.org/abs/2610.22987) shows can be attacked, is not measured.
- **Auto mode is not measured.** It depends on a classifier the scripted model cannot stand in for. The agent's own sandbox was not configured either.
- **Three repetitions per cell.** All 336 runs agreed, which shows no variation in this measurement, not that none can exist.
- **No attack catalog yet.** The only scenario is a pipeline smoke test. The control matrix does not need a catalog.
- **Live attacks are on hold.** Running attacks against a real product with a real account puts the operator at risk, so BSA does not do it for now. Lower-risk methods come first, and they have a cost: [a survey of 40 benchmarks](https://arxiv.org/abs/2605.16282) reports that lower-fidelity evaluations tend to report lower unsafe rates.
- **No attacks against real models yet.** The only real model run is a small check of the agent notice. The proxy's mode for real models is not implemented, so the arena still uses a scripted model.
- **No attack results.** Nothing here says how any agent performs against attacks.
- **The scenario runner does not drive the real agent yet.** The real binary runs in the contract tests and the control matrix. Scenario runs use a scripted fake agent, and the `GATED` and `BLOCKED` outcomes are never produced.
- **Containment has been tested, not proven.** The checks cover known escape paths on the [recorded setup](RESULTS.md). Docker warns that a container's default capabilities and mounts "may provide incomplete isolation, either independently, or when used in combination with kernel vulnerabilities". On Windows, Docker Desktop's WSL 2 backend also shares one kernel across WSL distributions, and Docker names Hyper-V mode as the way to avoid that ([R15](REFERENCES.md)).
- **Linux containers only.** The arena cannot reproduce agents running natively on Windows or macOS.
- **One agent.** Only Claude Code is integrated. The matrix covers one version, the contracts cover the versions in the [comparison](RESULTS.md#the-same-contracts-across-versions), and behavior may change in any release.
- **Headless only.** Runs are non-interactive, so nobody answers confirmation prompts and folder trust dialogs do not appear.
- **Images are not byte-identical.** Base images are pinned by digest and the agent by version, but system packages are not pinned.
- **Tested on one platform.** Results were recorded on Windows 11 with Docker Desktop. Linux and macOS hosts have not been tried.
- **The validator is not a guarantee.** It catches mistakes made in good faith. Human review stays necessary.
- **The exposure audit is run by hand.** Nothing enforces it, and it cannot find everything.
- **The agent notice is a mitigation.** An agent may ignore it or never read it. A [small check](RESULTS.md#agent-notice-with-a-real-model) showed no reduction in shell attempts.
- **No adaptive attacks yet.** They matter: [The Attacker Moves Second](https://arxiv.org/abs/2510.09023) reports adaptive attacks defeating defenses whose original evaluations reported near-zero attack success.
