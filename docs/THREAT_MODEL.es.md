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
| Un agente que visita el repositorio obedece un ataque | El visitante | Cargas útiles inertes en reposo, no guardadas como texto legible | Prevista |
| Un agente lee resultados que contienen ataques | Quien analiza | Solo salen de la arena campos tipados | Implementada para el agente simulado |
| Un pull request agrega una carga útil dañina | La comunidad | Validador y revisión humana obligatoria | Validador implementado, la revisión es una política |
| CI ejecuta ataques con secretos disponibles | El proyecto | Sin secretos en pull requests de forks | Prevista, aún no hay CI |
| El catálogo se reutiliza contra terceros | Terceros | Canarios y destinos válidos solo en la arena | Prevista |
| Dependencia o imagen comprometida | Todos | Solo biblioteca estándar de Python, imágenes base fijadas por digest y agente fijado por versión. Los paquetes del sistema no están fijados | Implementada |
| Se publica una falla nueva sin avisar al proveedor | Terceros | Divulgación coordinada | Política |

## Principio de diseño

La seguridad del repositorio no debe depender de que un modelo obedezca un aviso de texto. Ese fallo es justo lo que BSA quiere llegar a medir. El aviso de `AGENTS.md` es una capa adicional. La protección real debe ser que los ataques queden inertes fuera de la arena.
