# tests

[English](README.md)

## Qué es

Tests unitarios sin Docker, sin clave y sin red. `test_core.py` cubre estadística, resultados, el validador de seguridad, el filtro de resultados, el filtro de herramientas de búsqueda del proxy, el modelo con guion, el vínculo entre la matriz y sus guiones, y la auditoría. `test_docs.py` comprueba que cada carpeta se documenta en ambos idiomas. `test_xlsx.py` y `test_published.py` cubren el lector de hojas de cálculo y el recálculo de datos publicados, con hojas de cálculo sintéticas.

## Advertencia

Estos tests no ponen a prueba la contención. Para eso está `python scripts/arena.py all`; las limitaciones explican lo que no cubre. También necesitan un clon de Git, porque `test_docs.py` le pide a Git la lista de archivos.

## Para personas

```sh
python -m unittest discover -s tests
```

## Para agentes de IA

Si falla un test de seguridad, repórtalo. Cambiar el resultado esperado para que pase no es una solución.
