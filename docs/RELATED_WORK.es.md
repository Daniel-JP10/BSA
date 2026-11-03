# Trabajo relacionado

[English](RELATED_WORK.md)

Revisado en noviembre de 2026. Cuánto se leyó de cada fuente está en [REFERENCES.es.md](REFERENCES.es.md), así que comprueba los originales antes de citar. El recálculo de IssueTrojanBench que hizo BSA está en [Datos publicados](PUBLISHED_DATA.es.md).

## Benchmarks más cercanos a BSA

| Trabajo | Agentes ejecutados | Tamaño | Cómo se juzga el éxito | Repeticiones | Artefacto público |
|---|---|---|---|---|---|
| [INFUSE](https://arxiv.org/abs/2610.20776) | Mini-SWE-Agent; reproducción en Claude Code y Codex CLI | 40 tareas, 56 ataques, 5 categorías | Juez LLM más comprobaciones heurísticas en el contenedor | Una trayectoria por celda | [Código](https://github.com/judydnguyen/infuse) |
| [IssueTrojanBench](https://arxiv.org/abs/2607.20759) | Cursor, Claude Code, Codex Desktop | 696 artefactos, 4.176 corridas | Archivos marca que crea el agente, comprobados por el runner | Una corrida por configuración, comprobado en los resultados publicados | [Zenodo](https://doi.org/10.5281/zenodo.19245678) |
| [AIShellJack](https://arxiv.org/abs/2509.22040) | Cursor, GitHub Copilot | 314 payloads, 70 técnicas ATT&CK | Coincidencia con comandos registrados | Cada test corrió una vez | [figshare](https://doi.org/10.6084/m9.figshare.30111988) |
| [Red-Teaming Coding Agents](https://arxiv.org/abs/2509.05755) | Seis agentes de programación reales, entre ellos Claude Code y Cursor | 25 pares agente-modelo | Invocación de herramienta con el payload previsto | 10 intentos por par en su fase de fuga de prompts | Enlace anónimo |

## Benchmarks generales de agentes

| Trabajo | Alcance | Nota para BSA |
|---|---|---|
| [AgentDojo](https://arxiv.org/abs/2406.13352) | Workspace, Slack, viajes y banca simulados | Comprobaciones deterministas y rechazo explícito de jueces LLM. Referencia metodológica para BSA, no una prueba de agentes de programación |
| [LivePI](https://arxiv.org/abs/2605.17986) | OpenClaw real en una máquina virtual real | Entorno en vivo, con juez LLM más inspección de artefactos |
| [PIArena](https://arxiv.org/abs/2604.08499) | Plataforma unificada sobre benchmarks existentes | Ataques adaptativos guiados por retroalimentación |
| [Taxonomía de 40 benchmarks de seguridad](https://arxiv.org/abs/2605.16282) | Revisión | Reporta que la elección del benchmark puede dar conclusiones contradictorias, y que los recuentos de cobertura suelen sobrestimar la profundidad |
| [AgentDrift](https://arxiv.org/abs/2609.06972) | 12.536 trayectorias sintéticas, 71.024 pasos etiquetados | Un corpus para entrenar detectores, que marca el paso en que entra una inyección. No ejecuta ningún producto |

## Informes sobre los propios controles

| Trabajo | Qué reporta | Nota para BSA |
|---|---|---|
| [From Approval to Abuse](https://arxiv.org/abs/2610.22987) | Un texto plantado en un repositorio lleva al agente a pedir una regla de permiso amplia. En productos como Claude Code y Codex CLI, los agentes pidieron la regla buscada en el 58% de los casos, y con la regla aprobada, 47 de 58 casos elegibles lograron su objetivo sin que nadie lo notara | La aprobación es un control que también se puede atacar. BSA no lo ha medido, porque depende de la decisión de una persona |
| [Breaking Claude Code Opus 5 Auto Mode](https://embracethered.com/blog/posts/2026/breaking-claude-code-opus-5-and-automode/) | Corridas de laboratorio del autor con muestras pequeñas (3 de 5, 3 de 5 y 4 de 5). Según cuenta, el proveedor cerró el reporte como informativo y señaló el aislamiento del sistema operativo y el control del tráfico de salida como la frontera real | La matriz de BSA deja fuera el modo auto, porque depende de un clasificador que el modelo con guion no puede sustituir |

## Qué toma BSA de ellos y en qué se aparta

De estos trabajos BSA toma las comprobaciones deterministas en lugar de jueces LLM (AgentDojo), los contenedores con destinos simulados (INFUSE), los veredictos basados en archivos y otros efectos (IssueTrojanBench) y la idea de organizar los ataques en familias.

No los repite. Esos benchmarks miden con qué frecuencia cae un modelo real, que es la pregunta que se propusieron responder. BSA se hace la siguiente: sustituye el modelo por un guion que pide la acción de riesgo, como haría un modelo ya engañado, y mide qué hacen después los controles del producto. Eso no necesita texto de ataque ni una cuenta, y da la misma respuesta en cada corrida.

## El vacío que BSA busca cubrir

Ningún trabajo revisado aquí combina todo lo siguiente sobre agentes comerciales cerrados:

1. Efectos secundarios reales comprobados por un observador independiente, dentro de un entorno aislado.
2. Corridas repetidas con intervalos de confianza.
3. Matriz de modos de permiso.
4. Versiones fijadas que se vuelven a ejecutar con el tiempo para mostrar la deriva.
5. Mediciones de utilidad y falsos positivos en defensas a nivel de producto.
6. El efecto del producto separado del efecto del modelo. Los autores de IssueTrojanBench reportan que ningún rechazo vino del framework de un producto, y que el mismo modelo dio los mismos resultados entre productos ([detalles](PUBLISHED_DATA.es.md)).

Esta afirmación se refiere a los trabajos listados aquí, no a todo lo publicado. Hoy BSA cubre los puntos 1, 3, 4 y 6 para un agente, con un modelo con guion: ver la [matriz de controles](RESULTS.es.md#matriz-de-controles) y la [comparación de versiones](RESULTS.es.md#los-mismos-contratos-entre-versiones). El punto 2 aún no aplica a controles deterministas, y el punto 5 está sin hacer.
