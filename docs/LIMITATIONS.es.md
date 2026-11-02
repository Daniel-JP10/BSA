# Limitaciones

[English](LIMITATIONS.md)

Lo que BSA todavía no puede hacer y lo que quizá nunca pueda demostrar.

- **Aún no hay catálogo de ataques.** El único escenario es una prueba de humo del flujo.
- **Aún no hay corridas con modelos reales.** El binario del agente solo ha corrido con un modelo con guion, y el modo con modelo real del proxy no está implementado.
- **Sin resultados de ataques.** Nada aquí dice cómo se comporta un agente ante ataques.
- **El runner aún no maneja el agente real.** El binario real solo corre en los tests de contrato. Las corridas de escenarios usan un agente simulado, y los resultados `GATED` y `BLOCKED` nunca se producen.
- **La contención se ha puesto a prueba, pero no está demostrada.** Las comprobaciones cubren vías de escape conocidas en el [entorno registrado](RESULTS.es.md). Los contenedores comparten el kernel del host de Docker. En Docker Desktop ese host es una máquina virtual; en Linux es tu propia máquina.
- **Solo contenedores Linux.** La arena no puede reproducir agentes que corren de forma nativa en Windows o macOS.
- **Un solo agente.** Solo Claude Code está integrado, fijado a una versión. Su comportamiento puede cambiar en cualquier lanzamiento.
- **Solo modo no interactivo (headless).** Como las corridas no son interactivas, nadie responde a las confirmaciones y no aparecen los diálogos de confianza de carpetas.
- **Las imágenes no son idénticas byte a byte.** Las imágenes base están fijadas por digest y el agente por versión, pero los paquetes del sistema no están fijados.
- **Probado en una sola plataforma.** Los resultados se registraron en Windows 11 con Docker Desktop. No se ha probado en hosts Linux ni macOS.
- **El validador no es una garantía.** Detecta errores de buena fe. La revisión humana sigue siendo necesaria.
- **La auditoría de exposición se ejecuta a mano.** Nada la impone, y no puede encontrarlo todo.
- **El aviso a agentes es una mitigación.** Un agente puede ignorarlo o no leerlo nunca, y aún no se ha evaluado.
- **Todavía no hay ataques adaptativos.** Son importantes: [The Attacker Moves Second](https://arxiv.org/abs/2510.09023) reporta ataques adaptativos que vencen defensas cuyas evaluaciones originales indicaban un éxito de ataque cercano a cero.
