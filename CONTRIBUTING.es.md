# Cómo contribuir

[English](CONTRIBUTING.md)

El catálogo de ataques aún no acepta contribuciones. Las correcciones a la arena, al runner y a la documentación son bienvenidas.

## Reglas para todo escenario

| Regla | Requisito |
|---|---|
| R1 | Sin credenciales reales. Los canarios se generan en cada corrida |
| R2 | Sin dominios reales. Los destinos terminan en `.test` y solo resuelven dentro de la arena |
| R3 | Las cargas útiles usan marcadores que solo resuelve el runner (aún sin implementar) |
| R4 | Sin acciones destructivas. La destrucción se modela tocando un señuelo |
| R5 | Sin malware, sin explotar vulnerabilidades reales y sin persistencia fuera del contenedor |
| R6 | Ningún objetivo real: ni personas, ni organizaciones, ni servicios |
| R7 | El validador debe pasar, y una persona revisa cada carga útil |

## Antes de abrir un pull request

```sh
python -m unittest discover -s tests
python -m bsa validate
python scripts/arena.py all
python scripts/exposure_audit.py
```

La documentación es bilingüe. Cada carpeta tiene `README.md` y `README.es.md`, y un cambio en uno exige el mismo cambio en el otro. `tests/test_docs.py` comprueba las secciones obligatorias.

Revisar los metadatos de un escenario con un agente solo está permitido dentro del contenedor de desarrollo, tratándolos como datos. Los paquetes de ataques nunca entran en ese contenedor.
