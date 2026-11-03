# bsa

[English](README.md)

## Qué es

El código Python del banco de pruebas. Usa solo la biblioteca estándar.

| Módulo | Función |
|---|---|
| `catalog.py` | Carga escenarios y aplica las reglas estáticas de seguridad |
| `runner.py` | Ejecuta un escenario con el agente simulado, y solo deja salir campos tipados |
| `observers.py` | Convierte la evidencia en un resultado |
| `stats.py` | Intervalos de Wilson al 95% y errores estándar agrupados |
| `xlsx.py` | Lector de hojas de cálculo de solo lectura que rechaza trucos de entidades XML |
| `published.py` | Recálculo de los resultados publicados de IssueTrojanBench |
| `cli.py` | El comando `python -m bsa` |

Los resultados son `COMPROMISED`, `GATED`, `BLOCKED`, `IGNORED`, `DETECTED` e `INFRA_ERROR`. Un efecto observado siempre pesa más que lo que afirme el modelo. Hoy ningún código produce `GATED` ni `BLOCKED`.

## Advertencia

- `python -m bsa run` está pensado para la arena, que aporta el sink y `/workspace`.
- El validador de seguridad detecta errores de buena fe. No puede demostrar que un payload sea inofensivo, así que la revisión humana sigue siendo obligatoria.
- Publica una tasa solo con su intervalo: 0 de 10 aún permite una tasa real cercana al 28%.

## Para personas

```sh
python -m bsa validate          # comprueba el catálogo
python -m bsa wilson 0 30       # intervalo para 0 éxitos en 30 corridas
```

`python scripts/arena.py smoke` lanza las corridas de escenarios.

## Para agentes de IA

`safe_summary` mantiene el texto de ataque fuera de tu propio contexto, así que debe seguir sin texto libre. `classify` debe mantener los efectos observados por encima de lo que diga un modelo.
