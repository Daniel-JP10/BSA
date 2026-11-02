# Referencias

[English](REFERENCES.md)

Toda afirmación de este repositorio que venga de fuera debería poder rastrearse hasta una entrada de aquí. Todas las fuentes se comprobaron el 2026-11-02. La columna "Cómo se leyó" indica cuánto de cada fuente se leyó de verdad, para que nadie confunda un resumen con una verificación.

## Fuentes

| ID | Fuente | Enlace | Licencia o acceso | Cómo se leyó |
|---|---|---|---|---|
| R1 | *IssueTrojanBench: Benchmarking AI Coding Agents Against Malicious Issue Requests* (arXiv 2607.20759) | [arxiv.org/abs/2607.20759](https://arxiv.org/abs/2607.20759) | Paper: CC BY-NC-ND 4.0 | HTML leído completo, salvo un final resumido |
| R2 | Artefacto de IssueTrojanBench, versión 1.0.0, de "software-artifacts" | [Registro de Zenodo](https://zenodo.org/records/22983053), DOI `10.5281/zenodo.22983053`. El DOI de la nota del paper, `10.5281/zenodo.19245678`, redirigió a este registro. Código: [github.com/software-artifacts/IssueTrojanBench](https://github.com/software-artifacts/IssueTrojanBench) | CC BY 4.0 en Zenodo. GitHub no detecta licencia en el repositorio de código, que solo contiene un README | Archivo descargado por una persona del proyecto BSA, y su MD5 coincide con el que lista Zenodo. Hojas de cálculo leídas sin descomprimir, en un contenedor sin red. El README de GitHub lo abrió una persona del proyecto BSA, BSA no lo descargó |
| R3 | *INFUSE: A Unified Surface Benchmark for Indirect Prompt Injection in Agentic Systems* (arXiv 2610.20776), su [código](https://github.com/judydnguyen/infuse) y sus trayectorias en [Hugging Face](https://huggingface.co/datasets/judynguyen16/infuse-bench-trajectories) | [arxiv.org/abs/2610.20776](https://arxiv.org/abs/2610.20776) | Código: MIT. Trayectorias: no disponibles (la dirección responde 401) | HTML leído hasta la sección 3.2, el resto mediante un resumen. El encabezado del script de descarga se leyó directamente |
| R4 | *"Your AI, My Shell": Demystifying Prompt Injection Attacks on Agentic AI Coding Editors* (arXiv 2509.22040) y su [paquete de replicación](https://doi.org/10.6084/m9.figshare.30111988) | [arxiv.org/abs/2509.22040](https://arxiv.org/abs/2509.22040) | Paquete: CC BY 4.0, autor anónimo | HTML leído hasta la sección V-A, el resto mediante un resumen. La página de figshare se abrió en un navegador |
| R5 | *Red-Teaming Coding Agents from a Tool-Invocation Perspective* (arXiv 2509.05755) | [arxiv.org/abs/2509.05755](https://arxiv.org/abs/2509.05755) | El enlace al artefacto es anónimo | HTML leído hasta unos 39.000 caracteres, el resto mediante un resumen. El enlace al artefacto no se abrió |
| R6 | *AgentDojo* (arXiv 2406.13352) | [arxiv.org/abs/2406.13352](https://arxiv.org/abs/2406.13352) | Código en github.com/ethz-spylab/agentdojo, licencia sin comprobar | HTML leído en parte, el resto mediante un resumen |
| R7 | *LivePI* (arXiv 2605.17986) | [arxiv.org/abs/2605.17986](https://arxiv.org/abs/2605.17986) | Sin comprobar | Resumen y HTML, salvo los últimos 1.100 caracteres |
| R8 | *PIArena* (arXiv 2604.08499) | [arxiv.org/abs/2604.08499](https://arxiv.org/abs/2604.08499) | Código: MIT | Solo el resumen |
| R9 | *Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents* (arXiv 2605.16282) | [arxiv.org/abs/2605.16282](https://arxiv.org/abs/2605.16282) | Sin comprobar | Resumen leído directamente, el cuerpo mediante un resumen |
| R10 | *The Attacker Moves Second* (arXiv 2510.09023) | [arxiv.org/abs/2510.09023](https://arxiv.org/abs/2510.09023) | Sin comprobar | Solo a nivel de resumen, mediante un resultado de búsqueda. El paper no se leyó |
| R11 | Documentación de Claude Code: [hooks](https://code.claude.com/docs/en/hooks), [configuración](https://code.claude.com/docs/en/settings), [seguridad](https://code.claude.com/docs/en/security), [permisos](https://code.claude.com/docs/en/permissions), [sandbox](https://code.claude.com/docs/en/sandboxing) | | Documentación pública | Páginas de configuración y seguridad leídas de forma literal. Las de hooks y permisos en parte mediante resúmenes, y dos afirmaciones de esas páginas se contradicen (ver la nota de abajo) |
| R12 | Coding Agent Security Benchmark, Rogue Security | [huggingface.co/datasets/rogue-security/coding-agent-security-benchmark](https://huggingface.co/datasets/rogue-security/coding-agent-security-benchmark) | CC BY-NC 4.0 | Página abierta en un navegador y ficha leída. Existe una segunda copia en otra cuenta con la misma licencia, y no se verificó su relación con la primera |
| R13 | Nemotron RL Agentic Indirect Prompt Injection v1, NVIDIA | [huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1](https://huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1) | CC BY 4.0 | Ficha y lista de archivos leídas mediante la API pública |
| R14 | ClawTrojan | [huggingface.co/datasets/zstanjj/ClawTrojan](https://huggingface.co/datasets/zstanjj/ClawTrojan) | "other", términos no especificados | Ficha leída mediante la API pública |
| R15 | *The Magic Behind the Scenes of Docker Desktop*, blog de Docker | [docker.com/blog](https://www.docker.com/blog/the-magic-behind-the-scenes-of-docker-desktop/) | Entrada pública de blog, fecha sin comprobar | Texto leído mediante un script. Dice que Docker Desktop tiene una máquina virtual LinuxKit ligera que Docker gestiona, y que en Windows usa el backend WSL 2 |

**Cómo citar los datos de IssueTrojanBench.** software-artifacts. *IssueTrojanBench*, versión 1.0.0. Zenodo. DOI 10.5281/zenodo.22983053. CC BY 4.0. La entrada de cita del propio artefacto nombra la 41.ª Conferencia Internacional IEEE/ACM de Ingeniería de Software Automatizada (2026) y autores anonimizados, así que este repositorio trata el paper como un preprint.

**Sobre R11.** La página de configuración no incluye los hooks entre los ajustes que esperan la confianza en la carpeta, mientras que la de hooks dice que las sesiones interactivas los retienen hasta que se confía en la carpeta. BSA no resolvió esa diferencia.

## Afirmaciones que dependen de estas fuentes

| Afirmación | Dónde | Fuentes | Estado |
|---|---|---|---|
| Los benchmarks publicados dirigen estos ataques contra agentes comerciales como Cursor y Claude Code | README, RELATED_WORK | R1, R5 | R1 nombra Cursor, Claude Code y Codex Desktop. R5 nombra Claude Code y Cursor entre seis agentes |
| Tamaños, repeticiones y criterios de éxito de los cuatro benchmarks más cercanos | RELATED_WORK | R1 a R5 | Tamaños y repeticiones comprobados en cada texto. Los criterios de éxito de R3 y R5 vienen de resúmenes |
| IssueTrojanBench ejecutó cada configuración una vez, y sus resultados se comportan como 144 combinaciones | PUBLISHED_DATA, README | R2 | Recálculo de BSA a partir de las hojas de cálculo. El MD5 del archivo coincide con el de Zenodo, y `python scripts/analyze_published.py issuetrojanbench.zip` lo repite |
| Disponibilidad y licencias de los datasets | PUBLISHED_DATA | R2 a R4, R12 a R14 | Cada página o entrada de la API se abrió o consultó el 2026-11-02 |
| `docs/EEM_CRITERIA.md`, que enlaza el README, no está ni en el archivo ni en el repositorio de GitHub de los autores | PUBLISHED_DATA | R2 | Comprobado en la lista de archivos del archivo y, el 2026-11-02, en el listado de la API de GitHub, que solo muestra un README |
| Las afirmaciones de los autores sobre bifurcaciones, paquetes y payloads reversibles | PUBLISHED_DATA | R2 | Del README de GitHub, que abrió una persona del proyecto BSA |
| `claude --no-input --print` falla en Claude Code 2.1.306 | PUBLISHED_DATA | Ninguna, prueba propia de BSA | Repetible sin conexión: `python scripts/arena.py up` y luego `docker run --rm --network none bsa/agent:local claude --no-input --print hi` |
| Los ataques adaptativos vencen defensas con éxito de ataque casi nulo en su evaluación original | LIMITATIONS | R10 | Solo a nivel de resumen |
| La elección del benchmark puede dar conclusiones contradictorias, y las evaluaciones de menor fidelidad tienden a mostrar menos inseguridad | LIMITATIONS, RELATED_WORK | R9 | La primera parte está en el resumen. La segunda sale de un resumen del cuerpo |
| Cómo trata Claude Code `disableAllHooks`, los hooks administrados y `-p` | RESULTS | R11 | En parte mediante resúmenes, ver la nota sobre R11 |
| En Docker Desktop los contenedores corren en una máquina virtual de Linux gestionada por Docker | LIMITATIONS | R15 | Leído en la fuente. Es una entrada antigua: aún describe HyperKit en Mac, y Docker ha cambiado de backend desde entonces |
| Los contenedores comparten el kernel del host | LIMITATIONS, README de arena | Ninguna | Un hecho general sobre contenedores, **sin fuente aquí** |

Las mediciones de [RESULTS.es.md](RESULTS.es.md) son propias de BSA y se pueden repetir con los comandos que allí aparecen.
