# dev

[English](README.md)

## Qué es

Un contenedor de desarrollo, independiente de cualquier otro proyecto de Compose. El repositorio vive en un volumen de Docker, así que el contenedor no puede ver carpetas del host. No publica puertos ni tiene acceso a Docker, por lo que no puede arrancar, detener ni afectar ningún otro contenedor.

## Advertencia

- Tiene acceso a internet porque el desarrollo lo necesita, así que los paquetes de ataques se quedan fuera.
- El socket de Docker también: quien lo tiene puede controlar todos los contenedores de la máquina.
- Inicia sesión en herramientas solo cuando haga falta, y deja las claves personales en el host.
- Los archivos del volumen están separados de tu copia en el host, así que el trabajo hay que copiarlo de vuelta de forma explícita.

## Para personas

```sh
python scripts/dev.py up      # construye y arranca
python scripts/dev.py seed    # copia al volumen los archivos publicables
python scripts/dev.py shell   # abre una shell dentro
python scripts/dev.py down    # detiene y conserva los volúmenes
python scripts/dev.py purge   # detiene y borra los volúmenes
```

`seed` copia solo lo que Git publicaría, así que las notas privadas ignoradas nunca entran al contenedor.

## Para agentes de IA

Puede que te estés ejecutando aquí. `AGENTS.md` aplica, y las corridas de la arena las lanza una persona desde el host. No intentes llegar a Docker, al host ni a otros contenedores.
