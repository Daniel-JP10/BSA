# Modelo de amenazas

[English](THREAT_MODEL.md)

Las defensas marcadas como previstas protegen un catálogo que aún no existe.

## Qué evalúa BSA

| Elemento | Definición |
|---|---|
| Atacante | Controla contenido que el agente leerá, pero no la máquina ni la cuenta |
| Víctima | Un agente de programación con acceso a archivos, terminal y red |
| Activos simulados | Secretos canario, código y configuración del agente |
| Fuera de alcance | Un atacante ya presente en la máquina, un usuario malicioso, fallas del proveedor del modelo |

## Qué amenaza al propio BSA

| Amenaza | Quién corre riesgo | Defensa principal | Estado |
|---|---|---|---|
| Un ataque escapa de la arena | Quien la opera | Red interna, sin montajes del host, tests de contención | Implementada |
| El agente roba la clave de API | Quien la opera | La clave se queda en el proxy | Prevista, hoy no se usa ninguna clave |
| Un agente que visita el repositorio obedece un ataque | El visitante | Payloads inertes en reposo, no guardados como texto legible | Prevista |
| Un agente lee resultados que contienen ataques | Quien analiza | Solo salen de la arena campos tipados | Implementada para el agente simulado |
| Un pull request agrega un payload dañino | La comunidad | Validador y revisión humana obligatoria | Validador implementado, la revisión es una política |
| CI ejecuta ataques con secretos disponibles | El proyecto | Sin secretos en pull requests de forks | Prevista, aún no hay CI |
| El catálogo se reutiliza contra terceros | Terceros | Canarios y destinos válidos solo en la arena | Prevista |
| Dependencia o imagen comprometida | Todos | Solo biblioteca estándar de Python, imágenes base fijadas por digest y agente fijado por versión. Los paquetes del sistema no están fijados | Implementada |
| Se publica una falla nueva sin avisar al proveedor | Terceros | Divulgación coordinada | Política |

## Por qué importan los controles: incidentes publicados

Cada registro describe un control de confirmación, confianza o aislamiento de un agente de programación que falló hasta que una versión posterior lo corrigió. Los datos vienen de los registros [R21]. BSA no los ha reproducido. Solo prueba Claude Code, en versiones posteriores a todos los arreglos de Claude Code de esta tabla.

| Registro | Producto | Afectado | Debilidad | Qué dice el registro | Publicado |
|---|---|---|---|---|---|
| CVE-2025-55284 | Claude Code | Antes de 1.0.4 | CWE-78 | Las confirmaciones se podían saltar por una lista demasiado amplia de comandos seguros | 2025-08-16 |
| CVE-2025-54135 | Cursor | Por debajo de 1.3.9 | CWE-78, CWE-829 | Crear un dotfile nuevo en el proyecto no pedía aprobación | 2025-08-05 |
| CVE-2025-61591 | Cursor | 1.7 y anteriores | CWE-78 | Un servidor MCP no confiable podía devolver comandos inyectados durante la configuración OAuth | 2025-10-03 |
| CVE-2025-62222 | Extensión Copilot Chat de VS Code | Ver el registro | CWE-20, CWE-77 | Inyección de comandos que permite ejecutar código por red | 2025-11-11 |
| CVE-2025-65099 (GHSA-5hhx-v7f6-x7gv) | Claude Code | Antes de 1.0.39 | CWE-94 | Ejecución de comandos antes del diálogo de confianza inicial | 2025-11-19 |
| CVE-2026-25725 (GHSA-ff64-7w26-62rf) | Claude Code | Antes de 2.1.2 | CWE-501, CWE-668 | Escape del sandbox mediante configuración inyectada en `settings.json` | 2026-02-06 |
| CVE-2026-31854 | Cursor | Antes de 2.0 | CWE-78 | Instrucciones en un sitio visitado, combinadas con un salto de la lista de comandos permitidos | 2026-03-11 |

## Relación con OWASP

| Categoría de OWASP [R20] | Lugar en BSA |
|---|---|
| LLM01:2025 Prompt Injection | La causa que BSA da por hecha. El modelo con guion se comporta como un modelo que ya fue engañado |
| LLM06:2025 Excessive Agency, que OWASP atribuye a funcionalidad, permisos o autonomía excesivos | Lo que mide la [matriz de controles](RESULTS.es.md#matriz-de-controles): qué acciones sigue permitiendo cada configuración de permisos |

## Principio de diseño

La seguridad del repositorio no debe depender de que un modelo obedezca un aviso de texto. Esa falla es justo lo que BSA quiere llegar a medir. El aviso de `AGENTS.md` es una capa adicional. La protección real debe ser que los ataques queden inertes fuera de la arena.
