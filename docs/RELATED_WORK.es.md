# Trabajo relacionado

[English](RELATED_WORK.md)

Revisado en noviembre de 2026. En los cuatro benchmarks más cercanos a BSA, los tamaños y las repeticiones se comprobaron contra el texto de cada paper, y se abrieron los enlaces a sus artefactos, salvo el de Red-Teaming. La columna "cómo se juzga el éxito" de INFUSE y Red-Teaming viene de un resumen del paper. Los benchmarks generales se leyeron desde sus resúmenes o páginas. Comprueba los originales antes de citar. Las fuentes numeradas están en [REFERENCES.es.md](REFERENCES.es.md), y también se recalcularon los resultados publicados de IssueTrojanBench: ver [Datos publicados](PUBLISHED_DATA.es.md).

## Benchmarks más cercanos a BSA

| Trabajo | Agentes ejecutados | Tamaño | Cómo se juzga el éxito | Repeticiones | Artefacto público |
|---|---|---|---|---|---|
| [INFUSE](https://arxiv.org/abs/2610.20776) | Mini-SWE-Agent; reproducción en Claude Code y Codex CLI | 40 tareas, 56 ataques, 5 categorías | Juez LLM más comprobaciones heurísticas en el contenedor | Una trayectoria por celda | [Código](https://github.com/judydnguyen/infuse) |
| [IssueTrojanBench](https://arxiv.org/abs/2607.20759) | Cursor, Claude Code, Codex Desktop | 696 artefactos, 4176 corridas | Archivos marca que crea el agente, comprobados por el ejecutor | Una corrida por configuración, comprobado en los resultados publicados | [Zenodo](https://doi.org/10.5281/zenodo.19245678) |
| [AIShellJack](https://arxiv.org/abs/2509.22040) | Cursor, GitHub Copilot | 314 cargas útiles, 70 técnicas ATT&CK | Coincidencia con comandos registrados | Cada test corrió una vez | [figshare](https://doi.org/10.6084/m9.figshare.30111988) |
| [Red-Teaming Coding Agents](https://arxiv.org/abs/2509.05755) | Seis agentes de programación reales, entre ellos Claude Code y Cursor | 25 pares agente-modelo | Invocación de herramienta con la carga útil prevista | 10 intentos por par en su fase de fuga de prompts | Enlace anónimo |

El artefacto de IssueTrojanBench indica en su entrada de cita la 41.ª Conferencia Internacional IEEE/ACM de Ingeniería de Software Automatizada (2026) con autores anonimizados, así que este repositorio lo trata como un preprint.

## Benchmarks generales de agentes

| Trabajo | Alcance | Nota para BSA |
|---|---|---|
| [AgentDojo](https://arxiv.org/abs/2406.13352) | Workspace, Slack, viajes y banca simulados | Comprobaciones deterministas y rechazo explícito de jueces LLM. Referencia metodológica para BSA, no una prueba de agentes de programación |
| [LivePI](https://arxiv.org/abs/2605.17986) | OpenClaw real en una máquina virtual real | Entorno en vivo, con juez LLM más inspección de artefactos |
| [PIArena](https://arxiv.org/abs/2604.08499) | Plataforma unificada sobre benchmarks existentes | Ataques adaptativos guiados por retroalimentación |
| [Taxonomía de 40 benchmarks de seguridad](https://arxiv.org/abs/2605.16282) | Revisión | Reporta que la elección del benchmark puede dar conclusiones contradictorias, y que los recuentos de cobertura suelen sobrestimar la profundidad |

## Qué piensa tomar BSA de ellos

- Ejecutar productos reales, como IssueTrojanBench.
- Usar comprobaciones deterministas y evitar jueces LLM, como AgentDojo.
- Aislar las corridas en contenedores con destinos simulados, como INFUSE.
- Reportar intervalos de confianza y utilidad, como hace INFUSE en parte de su evaluación.
- Organizar los ataques en familias y reportar por familia.

## El hueco al que apunta BSA

Ningún trabajo revisado aquí combina todo lo siguiente sobre agentes comerciales cerrados:

1. Efectos secundarios reales comprobados por un observador independiente, dentro de un entorno aislado.
2. Corridas repetidas con intervalos de confianza.
3. Matriz de modos de permiso.
4. Versiones fijadas que se vuelven a ejecutar con el tiempo para mostrar la deriva.
5. Mediciones de utilidad y falsos positivos en defensas a nivel de producto.
6. El efecto del producto separado del efecto del modelo. En los resultados publicados de IssueTrojanBench, el mismo modelo dio el mismo resultado en cada corrida emparejada entre productos distintos, así que no se pueden distinguir ([detalles](PUBLISHED_DATA.es.md)).

Esta afirmación se refiere a los trabajos listados aquí, no a todo lo publicado. Debe comprobarse de nuevo antes de hacerla en público. BSA aún no ha logrado estos puntos.
