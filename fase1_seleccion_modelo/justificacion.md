# Fase 1: Selección y Justificación del Modelo de IA

> Contexto: EcoMarket recibe miles de consultas diarias (chat, correo, redes sociales). El 80%
> son repetitivas (estado de pedido, devoluciones, características de producto) y el 20% son
> complejas y requieren empatía (quejas, problemas técnicos, sugerencias). El tiempo de
> respuesta promedio actual es de 24 horas.

## ¿Qué tipo de modelo de IA generativa es el más adecuado?

Proponemos una solución híbrida: un LLM de propósito general de tamaño pequeño, sin fine-tuning inicial, combinado con recuperación de datos estructurados (tool-calling contra el sistema de pedidos). Desde nuestra perspectiva para definir esto se hace necesario poder evaluar un piloto que inicie con un modelo que no sea muy potente y poder ir escalando la prueba con modelos que lo superen en potencia para poder entender hasta que punto se justifica esa potencia agregada frente al beneficio marginal de hacerlo. Para nuestra prueba, nosotros planteamos hacer el testing inicial con modelos libres y gratis de ollama:  `qwen2.5:7b` y `Qwen2.5-1.5B-Instruct` . Tras ejecutar distintas pruebas, si los dos modelos no son suficientes, se plantea la posibilidad de usar un modelo mas potente, que incluso requiera pagar, y hacer la prueba con este nuevo modelo para identificar si definitivamente resuelve el problema o el proyecto simplemente no se resuelve correctamente con inteligencia artificial generativa.

## ¿Por qué este modelo y no otro?

Partimos de la idea de que  un modelo pequeño no necesita ser potente en "conocimiento memorizado" porque la precisión la garantiza la inyección de contexto real (el pedido consultado desde pedidos.json/futura BD), no el tamaño del modelo , el modelo solo necesita ser lo bastante bueno para redactar con fluidez y empatía sobre datos correctos.

Dado que la mayoria de consultas que recibe la empresa son repetitivas, estos modelos que no generan una gran demanda de recursos, y sin embargo, son lo suficientemente potente para ejecutar herramientas dentro de su contexto, y una vez organizados teniendo como respaldo para su contexto una wiki con las preguntas y respuestas mas frecuentes, podría ser suficiente para atender o al menos organizar y priorizar y asi lograr evaluar si la implementación funciona buscando una victoria temprana.

Esta selección es inicial, dado que consideramos importante que teniendo en cuenta los altos costos de contratar servicios de software de inteligencia artificial de los modelos mas potentes, es importante iniciar con un modelo que sea barato de implementar y que permite confirmar la hipotesis de que nuestra implementación mejora el tiempo promedio actual de las respuestas. 

## ¿Cuál sería la arquitectura propuesta?

La arquitectura se organiza en una capa de **enrutamiento/clasificación** que separa el 80% de
consultas repetitivas del 20% complejas, y una capa de **modelo intercambiable** (el mismo patrón
que implementamos en `fase3_prompts/src/backends.py`, donde `ModelBackend` permite cambiar de
Ollama a Transformers, o en el futuro a una API de pago, sin tocar la lógica de negocio).

**1. Capa de entrada**
Unifica los canales (chat, correo, redes sociales) en un solo punto de ingesta, normalizando cada
mensaje entrante a un formato común (texto del cliente + metadatos: canal, cliente, si aplica un
número de seguimiento).

**2. Capa de clasificación/enrutamiento**
Un primer paso (puede ser el propio LLM con un prompt de clasificación, o un modelo/heurística más
liviana) determina si la consulta es:

- **Repetitiva y estructurada** (estado de pedido, devolución, características de producto) → sigue
el flujo automatizado.
- **Compleja o sensible** (queja, problema técnico, sugerencia, o cualquier caso donde el modelo
reporte baja confianza) → se escala a un agente humano, opcionalmente con un borrador de
respuesta generado por el LLM como apoyo (human-in-the-loop), no como respuesta final automática.

**3. Capa de recuperación de contexto (grounding)**
Para las consultas estructuradas, en vez de confiar en lo que el modelo "recuerda", se recupera el
dato real antes de generar la respuesta:

- Consultas de pedido/devolución → *tool call* a la base de pedidos (en el prototipo, `pedidos_tool.py`
sobre `data/pedidos.json`; en producción, una llamada a la API del sistema de pedidos/envíos de
EcoMarket).
- Preguntas generales de producto/políticas → recuperación tipo RAG contra una base de conocimiento
(wiki de preguntas frecuentes, políticas de devolución, catálogo), en lugar de tool-calling exacto,
porque aquí la consulta es semántica y no por clave exacta.

**4. Capa de generación**
El contexto recuperado se inyecta en la plantilla de prompt (como en `prompts.py`) junto con
instrucciones explícitas de no inventar datos fuera del contexto entregado, y de responder con
empatía cuando el caso lo amerite (retraso, producto no devolvible). El LLM solo redacta la
respuesta en lenguaje natural; los datos "duros" (fechas, estados, políticas) siempre vienen de la
capa de recuperación, no del modelo.

**5. Capa de modelo (intercambiable)**
Se abstrae el backend del modelo para poder empezar con modelos abiertos/locales (Ollama,
Transformers) de bajo costo y, si las pruebas muestran que la calidad no es suficiente para
producción, migrar a un modelo más potente (API de Hugging Face Inference o un modelo de pago tipo
GPT-4) cambiando solo esta capa, sin rediseñar el resto del sistema.

**6. Capa de observabilidad/feedback**
Se registran los casos escalados a humano y las respuestas de baja confianza, como insumo para
ampliar la base de conocimiento o, más adelante, evaluar un fine-tuning con datos reales de
EcoMarket.

```
Cliente (chat/correo/redes)
        │
        ▼
  Clasificador de intención
        │
   ┌────┴─────┐
   ▼          ▼
Repetitiva   Compleja/sensible
   │              │
   ▼              ▼
Recuperación   Escalamiento a
de contexto    agente humano
(tool-calling  (+ borrador LLM
 o RAG)         opcional)
   │
   ▼
Generación (LLM + prompt +
contexto grounded)
   │
   ▼
Respuesta al cliente
```



## Justificación (costo, escalabilidad, integración, calidad de respuesta)

**Costo**: partir de modelos abiertos/locales que son gratis permite validar la hipótesis de mejora en tiempo de respuesta sin comprometer presupuesto antes de tener evidencia. Sin embargo, la comparación empírica mostró que el costo "cero" del modelo más pequeño (`Qwen2.5-1.5B-Instruct`) no es gratis en términos de riesgo: en el caso donde el modelo alucinó que un producto "ya había sido instalado" y usó ese dato inventado para **negar una devolución que debía proceder**. Este es un error de negocio con costo directo que puede superar fácilmente el ahorro de no pagar por un modelo más grande. Esto sugiere que el costo real debe evaluarse no solo en cómputo, sino en frecuencia de errores de negocio.

**Escalabilidad**: la arquitectura propuesta está diseñada para escalar en dos sentidos: 

(1) horizontalmente, atendiendo más volumen de las consultas repetitivas sin depender de agentes humanos, y

(2) en calidad, permitiendo subir de modelo backend sin rediseñar el resto del sistema. La evidencia de la Fase 3 apunta a una escalabilidad que puede diferenciarse por ejercicio: el ejercicio de estado de pedido funcionó de forma aceptable incluso con el modelo pequeño, mientras que el ejercicio de devolución mostró más fallas, sugiriendo escalar el modelo primero donde el riesgo de negocio es mayor, no de forma uniforme.

**Integración**: el prototipo demuestra que la integración con el sistema de pedidos puede
resolverse con un patrón simple de recuperación de contexto (tool-calling exacto por
`tracking_number`) sin necesidad de fine-tuning ni de una base vectorial, lo cual reduce fricción de implementación inicial. La complejidad adicional puede incorporarse de forma incremental sobre la misma arquitectura.

**Calidad de respuesta**: fue el criterio donde se encontró la diferencia más significativa entre
opciones. `qwen2.5:7b` respetó de forma consistente las reglas del prompt, mientras que `Qwen2.5-1.5B-Instruct` tuvo fallas repetidas de instrucción y al menos una alucinación con impacto directo en la decisión de negocio. Esto valida el enfoque de piloto iterativo planteado en la primera pregunta: el modelo pequeño ya muestra que el punto de beneficio marginal de un modelo más potente se alcanza rápido para el ejercicio de devolución, y sería la señal para justificar el paso a un modelo más grande o de pago en ese flujo específico, manteniendo el modelo económico donde sí demostró ser suficiente.