# arena/agent

[English](README.md)

## Qué es

La imagen donde corre el agente. Lleva Claude Code fijado a una versión exacta, además de `curl`, `git` y Python a propósito: la contención debe venir del entorno, así que las herramientas siguen disponibles.

| Archivo | Función |
|---|---|
| `Dockerfile` | La imagen, con su base fijada por digest |
| `managed-settings.json` | Hook de nivel administrado que usan los tests de contrato |
| `deny_hook.py` | Hook de prueba que solo actúa cuando un test crea su archivo de marca |

## Advertencia

Esta imagen es un sujeto de prueba: mantenla lejos del trabajo diario y de credenciales reales. El archivo de configuración administrada existe para los tests de contrato y no protege nada.

## Para personas

`python scripts/arena.py up` construye la imagen. Para mirar otra versión del agente sin cambiar nada, ejecuta `python scripts/arena.py drift <versión>`. Para mover la versión fijada, cambia el valor por defecto en `Dockerfile` y `compose.yml`, vuelve a ejecutar `python scripts/arena.py all` y registra de nuevo la matriz. Los resultados valen para una sola versión, así que una versión nueva puede requerir nuevos valores registrados en `contracts.py`.

## Para agentes de IA

Conserva la versión fijada y no copies esta configuración ni este hook a un entorno real.
