# arena/containment

[English](README.md)

## Qué es

Los programas de prueba que corren dentro de la arena.

- `check.py` intenta escapar: llegar a internet, a direcciones del host, a la API de Docker, a archivos del host y a la clave real, o escribir en rutas del sistema. Cada intento debe fallar. Dos controles de conectividad deben funcionar, para que una red caída no pase por accidente.
- `contracts.py` mide cómo se comporta el binario real del agente con un modelo con guion: ¿una regla de permisos o un hook detiene de verdad un comando? La única evidencia es si ocurrió el efecto secundario, y la corrida falla si un resultado difiere del registrado. También registra qué comandos corren sin aprobación y si un hook `deny` los detiene.
- `matrix.py` cruza 16 acciones inofensivas con 7 configuraciones de permisos y registra cuáles produjeron su efecto. Su columna Bypass es un control: si una acción no corre ahí, la prueba misma está rota.
- `open_network.py` corre en una copia de la arena con la red abierta, y solo pasa si llega a internet.

## Advertencia

Un resultado en verde cubre estas comprobaciones en este entorno, no todos los escapes posibles. Si una comprobación falla, detente: no se ejecutan ataques hasta entenderla. Los resultados de contrato describen una versión del agente y pueden cambiar con la siguiente.

## Para personas

```sh
python scripts/arena.py contain
python scripts/arena.py contract
python scripts/arena.py contract <caso> <caso>
python scripts/arena.py matrix
python scripts/arena.py drift <versión> <versión>
```

Escribe cada comprobación nueva como un intento que debe fallar. Si podría pasar por la razón equivocada, agrega un control que demuestre que el camino era utilizable. Para agregar un contrato, agrega una entrada a `CASES` en `contracts.py`, y a `RAN` si se espera que el comando se ejecute. Para agregar una acción a la matriz, agrégala a `ACTIONS` en [`fake_llm.py`](../services/fake_llm.py) y a `READS` o `EFFECTS` en `matrix.py`. Para agregar una configuración, agrégala a `PROFILES`. Luego registra la tabla nueva con `python scripts/arena.py matrix 3 --record`.

## Para agentes de IA

Reporta una comprobación que falle en lugar de debilitarla, omitirla o borrarla. Los intentos de escape de esta carpeta son tests y solo corren dentro de la arena.
