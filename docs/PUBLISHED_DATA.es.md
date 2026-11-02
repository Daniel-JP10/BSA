# Datos publicados

[English](PUBLISHED_DATA.md)

Qué datos públicos hay sobre ataques a agentes de programación, qué encontró BSA al recalcular uno de ellos y cómo puede usarse cada fuente aquí. Todo se comprobó el 2026-11-02. Las fuentes llevan la numeración de [REFERENCES.es.md](REFERENCES.es.md).

La regla para todas: enlazar y citar, nunca copiar. Estos conjuntos contienen texto de ataque, y el texto de ataque no debe entrar en este repositorio.

## Qué hay disponible

| Fuente | Acceso | Licencia | Qué contiene | Uso en BSA |
|---|---|---|---|---|
| IssueTrojanBench, Zenodo [R2] | Abierto | CC BY 4.0 | Un archivo de 325,2 kB: payloads, scripts y resultados por corrida en Excel de 4.176 corridas | Recalculado abajo |
| Paquete de replicación de AIShellJack, figshare [R4] | Abierto | CC BY 4.0 | 91 archivos, 1,57 GB (versión 4, publicada el 2025-09-13): datos, código y resultados. Midió Cursor v1.2.2 y Copilot v1.102 | Aún sin analizar |
| Trayectorias de INFUSE, Hugging Face [R3] | **No disponible.** La dirección responde 401, y el perfil público de los autores lista otros dos datasets | No indicada | Su script de descarga dice que el repositorio es privado hasta que se publique | Ninguno |
| Coding Agent Security Benchmark, Hugging Face [R12] | Abierto | **CC BY-NC 4.0** | 332 mensajes de sesiones de agentes, etiquetados en 13 categorías de violación por un juez LLM. Solo 9 están etiquetados como inyección de prompts | La lista de categorías, como referencia. La licencia no comercial impide copiarlo a un repositorio Apache-2.0 |
| Nemotron RL Agentic Indirect Prompt Injection, Hugging Face [R13] | Abierto | CC BY 4.0 | Registros sintéticos en 9 dominios de empresa, 45 MB. Hecho para entrenar agentes, y no específico de programación | Referencia de categorías de ataque |
| ClawTrojan, Hugging Face [R14] | Abierto | "other": su ficha dice que los términos no están especificados y pide confirmar el uso permitido antes de redistribuir | 362 muestras por trayectoria y 1.676 entornos de pasos | Ninguno hasta que los términos estén claros |

Una búsqueda de texto completo de "prompt injection agent" en Hugging Face devuelve más de 36.000 coincidencias, y la mayoría son colecciones de entrenamiento sin relación. Los nombres también engañan: al buscar "infuse" aparecen datasets de otro proyecto.

## IssueTrojanBench: qué muestran los resultados publicados

BSA recalculó las tres hojas de cálculo de la versión 1.0.0 [R2], que tienen licencia CC BY 4.0. Los autores no respaldan este análisis. Los archivos se leyeron dentro de un contenedor sin red, y no se ejecutó ningún script del dataset.

### Los números coinciden con el resumen de los autores

- 4.176 filas en seis hojas de 696, una por issue semilla. Ninguna configuración aparece dos veces, así que **cada configuración se ejecutó una sola vez**.
- Los totales recalculados coinciden con las hojas `Metrics` de los autores: general (2.776 de 4.176, 66,5%), por modelo, por producto, por categoría de ataque, por vector de entrega y el reparto de rechazos.
- Las hojas de cálculo no contienen macros, vínculos externos ni fórmulas.

### Las 4.176 corridas son 144 combinaciones

Cada combinación de issue semilla, categoría de ataque, producto y modelo (6 × 4 × 6 = 144) tiene 29 corridas, una por vector de entrega y perturbación. Dentro de una combinación, el resultado nunca depende de la perturbación (posición, idioma, mayúsculas o tamaño de letra):

| Forma de la combinación | Cantidad |
|---|---|
| Tiene éxito en las 29 corridas | 24 |
| Falla en las 29 corridas | 40 |
| Mixta | 80 |

En las 80 combinaciones mixtas solo decide una cosa: si el vector de entrega es el texto alternativo de una imagen. Allí tuvo éxito en 0 de 240 corridas, y los otros cinco vectores en 2.080 de 2.080.

Por eso un intervalo calculado sobre 4.176 corridas las trata como independientes cuando no lo son. Por ejemplo, Claude Code con Sonnet 4.6 tuvo éxito en 286 de 696 corridas (41,1%), y un intervalo de Wilson sobre esas corridas va de 37,5% a 44,8%. Contando combinaciones, 11 de sus 24 tuvieron al menos un éxito, con un intervalo de 28% a 65%. Los archivos de los autores no dan intervalos.

### Decide el modelo, y el producto no muestra un efecto aparte

Con el mismo modelo, los tres productos dieron el mismo resultado en todas las corridas emparejadas:

| Modelo | Productos comparados | Corridas emparejadas | Mismo resultado |
|---|---|---|---|
| Sonnet 4.6 | Cursor y Claude Code | 696 | 696 |
| GPT-5.4 | Cursor y Codex Desktop | 696 | 696 |
| GPT-5.3 Codex | Cursor y Codex Desktop | 696 | 696 |

Las tasas por producto de la hoja de resumen (Claude Code 41,1%, Cursor 66,5%, Codex Desktop 79,2%) reflejan entonces a los modelos: Cursor solo mezcla los tres. Con modelos que no son deterministas y productos distintos, coincidir en todas las corridas es poco habitual, y estos archivos no lo explican. Puede ser un comportamiento estable, o que los resultados no se midieron de forma independiente. Los archivos no permiten distinguirlo: cita estas cifras como resultados por modelo y pregunta a los autores antes de apoyarte en ellas.

### Claude Code con Sonnet 4.6

| Categoría de ataque | Éxitos | Corridas |
|---|---|---|
| Supply Chain | 156 | 174 |
| Policy Bypass | 130 | 174 |
| Persistence Hook | 0 | 174 |
| Resource Exhaustion | 0 | 174 |

El issue original (SymPy #29421) solo tuvo éxito en Supply Chain. El texto alternativo de imagen tuvo éxito en 0 de 72 corridas. Entre los dos productos que usaron Sonnet 4.6, sus 820 fallos se etiquetan como rechazo del modelo 754 veces y como clasificación de confianza 66 veces. Los autores definen `EEM_Score` 0 como que el agente rechazó, ignoró o no pudo interpretar el payload [R2], y los archivos añaden las etiquetas "Model Refusal" y "Trust Classification" solo para esas corridas.

### Lo que los archivos no dicen

- **Versiones y modo de permisos.** Ninguno se registra para ningún producto.
- **El ejecutor de Claude Code.** `scripts/run_benchmark.py` lo lanza con `claude --no-input --print`. En Claude Code 2.1.306 eso falla con `error: unknown option '--no-input'` (probado sin conexión el 2026-11-02), así que el script no se puede usar tal cual con esa versión.
- **Tiempo de espera.** Los scripts de Cursor y Codex Desktop escriben en la aplicación y esperan un tiempo fijo, 300 segundos por defecto, sin comprobar si el agente terminó. Una corrida lenta cuenta como fallo.
- **Spotlighting.** La hoja de la defensa trae agregados de 144 corridas de PDF, sin filas por corrida, y la columna "con Spotlighting" repite cada porcentaje de la columna "sin defensa". La conclusión de que no añade protección puede ser correcta, pero no se puede comprobar con estos archivos.
- **Los criterios de éxito.** El README enlaza `docs/EEM_CRITERIA.md` para los criterios detallados por ataque, pero ese archivo no está en el archivo publicado (comprobado en su lista de archivos). Los comandos de una línea del README son los únicos criterios disponibles.

### Cómo se juzga el éxito

Con archivos marca, no por lo que diga el modelo: `dependency_status.txt` para la cadena de suministro, `.validate_refactor.sh` para persistencia, `CLAUDE.md`, `AGENTS.md` o `.cursorrules` para el salto de políticas, y `diagnostic_stress.sh` para el agotamiento de recursos. Cada archivo de payload lleva su propio indicador de éxito. Es el mismo principio que usa BSA.

### Lo que dicen los autores sobre la seguridad [R2]

Todos los experimentos corrieron en repositorios bifurcados bajo control de los investigadores, no se publicó ningún paquete en registros públicos, ningún desarrollador real estuvo expuesto a contenido adversarial, y los payloads se diseñaron para ser detectables y reversibles. BSA no ha verificado estas afirmaciones.

### Compruébalo a mano

Abre los dos archivos `*_Results_final.xlsx`. Cada hoja de issue tiene las columnas `Issue_ID`, `Attack_Category`, `Agent_Framework`, `Model`, `Delivery_Vector`, `Perturbation`, `EEM_Score` y `Rejection_Attribution`. En una tabla dinámica:

1. Cuenta las filas: 696 por hoja.
2. Agrupa por agente y modelo y suma `EEM_Score`: Cursor y Claude Code deben dar el mismo total para Sonnet 4.6 (286).
3. Filtra `Agent_Framework` por Claude Code y agrupa por `Attack_Category`.
4. Filtra una combinación (issue, categoría, agente, modelo) y compara `EEM_Score` entre `Delivery_Vector` y `Perturbation`.

### Repítelo con el script de BSA

```sh
python scripts/analyze_published.py issuetrojanbench.zip
```

Descarga primero el archivo del registro de Zenodo [R2]. El script comprueba su MD5 contra el que Zenodo lista para la versión 1.0.0 (`3e335d29585764f054029b7f43b4f4cb`) y se niega a seguir si difiere. Copia el archivo en un contenedor desechable sin red, con el sistema de archivos de solo lectura y sin capacidades, lee las hojas de cálculo sin descomprimir nada, imprime los números de esta página y elimina el contenedor. Añade `--json` para ver los valores en bruto. Hace falta Docker, y nunca se ejecuta nada del archivo. Mantén el archivo descargado fuera del repositorio, o exclúyelo en local con `.git/info/exclude`: la auditoría de exposición señala cualquier archivo `.zip` que encuentre.

### Límites de este recálculo

- Usa solo las hojas de cálculo de los autores. No se comparó con el PDF del paper.
- El archivo lo descargó una persona del proyecto BSA. Su MD5 coincide con el que lista el registro de Zenodo, y su SHA-256 es `be705afb3f4dbffc806e476d00a6ca64c3f00783435ccc70945594276a17383b`. El script de arriba reproduce con él todos los números de esta página.
- No se leyó ningún texto de payload.

## Qué toma BSA de esto

- Reportar resultados por combinación y calcular los intervalos sobre combinaciones.
- Mantener el modelo fijo, como hace el modelo con guion, para ver qué hace el producto por sí solo.
- Registrar la versión del producto, el modo de permisos, el tiempo máximo y cómo se detecta el fin de una corrida, y comprobar que cada opción de línea de comandos que use un ejecutor exista en esa versión.
- Las cuatro categorías sirven de referencia para pruebas basadas en acciones: instalar un paquete, un script nuevo, un archivo de configuración del agente y la cantidad de procesos.
