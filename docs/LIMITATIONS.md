# Limitations

[Español](LIMITATIONS.es.md)

What BSA cannot do yet, and what it may never prove.

- **No attack catalog yet.** The only scenario is a pipeline smoke test.
- **No real model runs yet.** The agent binary has only run against a scripted model, and the proxy's mode for real models is not implemented.
- **No attack results.** Nothing here says how any agent performs against attacks.
- **The runner does not drive the real agent yet.** The real binary runs only in the contract tests. Scenario runs use a scripted fake agent, and the `GATED` and `BLOCKED` outcomes are never produced.
- **Containment has been tested, not proven.** The checks cover known escape paths on the [recorded setup](RESULTS.md). Containers share the Docker host's kernel. On Docker Desktop that host is a virtual machine; on Linux it is your machine.
- **Linux containers only.** The arena cannot reproduce agents running natively on Windows or macOS.
- **One agent.** Only Claude Code is integrated, pinned to one version. Behaviour may change in any release.
- **Headless only.** Runs are non-interactive, so nobody answers confirmation prompts and folder trust dialogs do not appear.
- **Images are not byte-identical.** Base images are pinned by digest and the agent by version, but system packages are not pinned.
- **Tested on one platform.** Results were recorded on Windows 11 with Docker Desktop. Linux and macOS hosts have not been tried.
- **The validator is not a guarantee.** It catches mistakes made in good faith. Human review stays necessary.
- **The exposure audit is run by hand.** Nothing enforces it, and it cannot find everything.
- **The agent notice is a mitigation.** An agent may ignore it or never read it, and it has not been evaluated.
- **No adaptive attacks yet.** They matter: [The Attacker Moves Second](https://arxiv.org/abs/2510.09023) reports adaptive attacks defeating defences whose original evaluations reported near-zero attack success.
