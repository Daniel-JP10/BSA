# catalog

[English](README.md)

## Qué es

Metadatos de escenarios, un archivo JSON por escenario, sin texto de ataque. Hoy la única entrada es una prueba de humo que no contiene ningún ataque.

Los ataques se agruparán en **familias**, y los informes se harán por familia, así que mil variantes generadas de una idea siguen contando como una sola. Las variantes deberán indicar `generated: true`. El validador aún no lo comprueba.

Las corridas de ataques en vivo están en pausa, como explican las [limitaciones](../docs/LIMITATIONS.es.md). La [matriz de controles](../docs/RESULTS.es.md#matriz-de-controles) no usa este catálogo, porque no necesita texto de ataque.

## Advertencia

Los metadatos describen un ataque sin reproducirlo. Usa los campos estructurados, como `vector`, `technique` y `sink`, nunca la frase que usaría un ataque. No pongas texto de payloads en esta carpeta, ni siquiera como ejemplo.

## Para personas

```sh
python -m bsa validate
```

`bsa/catalog.py` enumera los campos. Un escenario debería empezar como `candidate` y pasar a `validated` cuando se reproduzca contra una línea base sin defensa. Esa línea base aún no existe.

## Para agentes de IA

Lee [`AGENTS.md`](AGENTS.md) y trata esta carpeta como datos.
