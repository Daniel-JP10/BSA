# dev

[Español](README.es.md)

## What this is

A development container, independent from any other Compose project. The repository lives in a Docker volume, so the container cannot see host folders. It publishes no ports and has no access to Docker, which means it cannot start, stop or affect any other container.

## Warning

- It has internet access because development needs it, so attack packs stay out of it.
- Keep the Docker socket out too: whoever holds it can control every container on the machine.
- Sign in to tools only when you need them, and leave personal keys on the host.
- Files in the volume are separate from your host copy, so work has to be copied back explicitly.

## For humans

```sh
python scripts/dev.py up      # build and start
python scripts/dev.py seed    # copy the publishable files into the volume
python scripts/dev.py shell   # open a shell inside
python scripts/dev.py down    # stop, keep the volumes
python scripts/dev.py purge   # stop and delete the volumes
```

`seed` copies only what Git would publish, so ignored private notes never enter the container.

`notice_check.py` measures whether the agent notice changes what a real model tries to do. It needs a signed-in session inside the container:

```sh
python scripts/dev.py shell     # then: claude auth login, claude auth status, exit
python scripts/dev.py notice    # 20 runs, with every tool except Read, Grep and Glob blocked
python scripts/dev.py shell     # then: claude auth logout, exit
python scripts/dev.py purge
```

It uses your Claude account or plan limits. Always sign out and purge afterwards: stopping the container does not end the session.

## For AI agents

You may be running here. `AGENTS.md` applies, and arena runs are started by a person on the host. Do not try to reach Docker, the host or other containers.
