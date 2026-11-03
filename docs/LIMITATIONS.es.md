# Limitaciones

[English](LIMITATIONS.md)

Lo que BSA todavía no puede hacer y lo que quizá nunca pueda demostrar.

- **Un modelo con guion no es un modelo engañado.** Pide una acción por corrida. Los ataques reales encadenan pasos y disimulan su intención, y la matriz no mide eso. Muestra qué hace un control con una petición, no qué tan probable es esa petición.
- **Sin una persona en el circuito.** Las corridas no interactivas rechazan lo que se le preguntaría a una persona. No se mide cómo responde la gente a las confirmaciones, y [From Approval to Abuse](https://arxiv.org/abs/2610.22987) muestra que se pueden atacar.
- **El modo auto no se mide.** Depende de un clasificador que el modelo con guion no puede sustituir. Tampoco se configuró el sandbox propio del agente.
- **Tres repeticiones por celda.** Las 336 corridas coincidieron, lo que muestra que no hubo variación en esta medición, no que no pueda haberla.
- **Aún no hay catálogo de ataques.** El único escenario es una prueba de humo del flujo. La matriz de controles no lo necesita.
- **Los ataques en vivo están en pausa.** Ejecutar ataques contra un producto real con una cuenta real pone en riesgo a quien lo hace, así que BSA no lo hace por ahora. Primero van los métodos de menor riesgo, y tienen un costo: [una revisión de 40 benchmarks](https://arxiv.org/abs/2605.16282) reporta que las evaluaciones de menor fidelidad tienden a mostrar tasas de inseguridad más bajas.
- **Aún no hay ataques contra modelos reales.** La única corrida con un modelo real es una prueba pequeña del aviso a agentes. El modo con modelo real del proxy no está implementado, así que la arena sigue usando un modelo con guion.
- **Sin resultados de ataques.** Nada aquí dice cómo se comporta un agente ante ataques.
- **El runner de escenarios aún no controla el agente real.** El binario real corre en los tests de contrato y en la matriz de controles. Las corridas de escenarios usan un agente simulado, y los resultados `GATED` y `BLOCKED` nunca se producen.
- **La contención se ha puesto a prueba, pero no está demostrada.** Las comprobaciones cubren vías de escape conocidas en el [entorno registrado](RESULTS.es.md). Docker advierte que las capacidades y montajes por defecto de un contenedor "may provide incomplete isolation, either independently, or when used in combination with kernel vulnerabilities". En Windows, el backend WSL 2 de Docker Desktop también comparte un kernel entre las distribuciones de WSL, y Docker señala el modo Hyper-V como la forma de evitarlo ([R15](REFERENCES.es.md)).
- **Solo contenedores Linux.** La arena no puede reproducir agentes que corren de forma nativa en Windows o macOS.
- **Un solo agente.** Solo Claude Code está integrado. La matriz cubre una versión, los contratos cubren las versiones de la [comparación](RESULTS.es.md#los-mismos-contratos-entre-versiones), y el comportamiento puede cambiar en cualquier lanzamiento.
- **Solo modo no interactivo (headless).** Como las corridas no son interactivas, nadie responde a las confirmaciones y no aparecen los diálogos de confianza de carpetas.
- **Las imágenes no son idénticas byte a byte.** Las imágenes base están fijadas por digest y el agente por versión, pero los paquetes del sistema no están fijados.
- **Probado en una sola plataforma.** Los resultados se registraron en Windows 11 con Docker Desktop. No se ha probado en hosts Linux ni macOS.
- **El validador no es una garantía.** Detecta errores de buena fe. La revisión humana sigue siendo necesaria.
- **La auditoría de exposición se ejecuta a mano.** Nada la impone, y no puede encontrarlo todo.
- **El aviso a agentes es una mitigación.** Un agente puede ignorarlo o no leerlo nunca. Una [prueba pequeña](RESULTS.es.md#aviso-a-agentes-con-un-modelo-real) no mostró una reducción de los intentos de shell.
- **Todavía no hay ataques adaptativos.** Son importantes: [The Attacker Moves Second](https://arxiv.org/abs/2510.09023) reporta ataques adaptativos que vencen defensas cuyas evaluaciones originales indicaban un éxito de ataque cercano a cero.
