# arena/services

[English](README.md)

## Qué es

Los tres servicios de apoyo de la arena, escritos con la biblioteca estándar de Python y con una imagen compartida.

| Archivo | Función |
|---|---|
| `llm_proxy.py` | Solo permite rutas del modelo, descarta el token del agente, agrega una clave real si existe, aplica un presupuesto de peticiones y elimina las herramientas de búsqueda del lado del proveedor |
| `fake_llm.py` | Implementa la API del modelo con respuestas de guion, para que un agente real corra sin clave y sin costo |
| `sink.py` | Guarda lo que llega a un destino simulado del atacante, accesible como `sink.bsa.test` |

## Advertencia

- El proxy es el único componente que puede tener una clave real. Si se agregan corridas con modelos reales, los tests de contención deben demostrar que la clave queda fuera de `agent`.
- Estos servicios recibirán texto controlado por el atacante, así que nunca registran el cuerpo de las peticiones.
- Lo que guarda el sink es salida de ataques y debe quedarse en la arena.

## Para personas

Compose arranca estos servicios, así que no hay nada que ejecutar a mano. El proxy lee `BSA_UPSTREAM`, `BSA_KEY_FILE`, `BSA_MAX_REQUESTS` y `BSA_ALLOWED_MODELS`. Para agregar una acción al guion, agrega una entrada a `SCRIPTS` en `fake_llm.py`. La matriz de controles guarda sus acciones en `ACTIONS`, en el mismo archivo.

## Para agentes de IA

Deja la lista de rutas como está, mantén los prompts y el contenido del sink fuera de cualquier registro, y apunta `BSA_UPSTREAM` solo a la API del modelo o a `fake-llm`.
