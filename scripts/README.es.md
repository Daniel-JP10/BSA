# scripts

[English](README.md)

## Qué es

Comandos que corren en el host.

| Script | Función |
|---|---|
| `arena.py` | Construye, verifica, ejecuta y elimina la arena, y comprueba que no cambiaron contenedores, redes ni volúmenes de otros proyectos |
| `dev.py` | Gestiona el contenedor de desarrollo |
| `exposure_audit.py` | Revisa lo que Git publicaría y todo el historial de commits en busca de secretos, datos personales, caracteres ocultos, metadatos de imágenes y archivos prohibidos |

## Advertencia

- Ejecútalos en el host: ningún contenedor de este proyecto tiene acceso a Docker.
- Nunca ejecutan `docker system prune` ni otro comando que cambie recursos fuera de este proyecto. Debe seguir así.
- **Ejecuta la auditoría antes de cada push.** El historial de Git es permanente una vez enviado, así que un secreto borrado después sigue expuesto.
- La auditoría se ejecuta a mano y no puede encontrarlo todo. Complementa la revisión de una persona.

## Para personas

```sh
python scripts/exposure_audit.py
```

Para buscar tu nombre, usuario o correo sin publicarlos, escríbelos en `.bsa-audit-terms`, uno por línea. Git ignora ese archivo, y la auditoría avisa si no encontró términos que cargar. Los resultados muestran regla y ubicación, nunca el texto encontrado.

## Para agentes de IA

Ejecuta la auditoría y muestra su resultado antes de decir que pasó. No agregues comandos amplios de Docker a estos scripts.
