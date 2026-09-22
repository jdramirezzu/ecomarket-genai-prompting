# Fase 2: Evaluación de Fortalezas, Limitaciones y Riesgos Éticos

> Evalúa críticamente la solución que propusiste en la Fase 1.

## Fortalezas

- **Disponibilidad 24/7 y reducción del tiempo de respuesta**: el 80% de consultas repetitivas (estado de pedido, devoluciones, características de producto) puede resolverse en minutos en vez de las 24 horas actuales, porque el dato ya existe en el sistema de pedidos y el modelo solo necesita redactarlo con claridad.
- **Respuestas grounded, no memorizadas**: al inyectar el contexto real del pedido en cada prompt y exigir explícitamente que el modelo no invente datos fuera de ese contexto, la precisión no depende del tamaño del modelo sino de la calidad de la recuperación de datos.
- **Costo bajo para la victoria temprana**: al usar modelos abiertos/locales (Ollama, Transformers)
desde el piloto, se valida la hipótesis de mejora en tiempos de respuesta sin comprometer
presupuesto en una API de pago antes de confirmar que el enfoque funciona.
- **Arquitectura con camino de escalamiento claro**: la capa de modelo intercambiable permite subir a un modelo más potente sin rediseñar el resto del sistema si las pruebas muestran que el modelo pequeño no alcanza.



## Limitaciones

- **No resuelve el 20% complejo**: quejas, problemas técnicos y sugerencias requieren juicio,
negociación o autoridad para tomar decisiones (reembolsos excepcionales, compensaciones) que un
LLM pequeño sin fine-tuning no debería tener; la arquitectura los escala a un humano, no los
automatiza.
- **Depende completamente de la calidad de los datos de origen**: si el sistema de pedidos tiene un
estado desactualizado o incorrecto, el modelo va a comunicar ese error con total seguridad y tono
profesional, lo cual puede ser peor que no responder, porque suena confiable.
- **Modelos pequeños son frágiles ante instrucciones complejas**: en las pruebas de la Fase 3 se
observó que `Qwen2.5-1.5B-Instruct` (Transformers) ignoró reglas explícitas del prompt con más
frecuencia que `qwen2.5:7b` (Ollama) — por ejemplo, no respetó el guardrail contra preguntas fuera
de tema y en un caso llegó a negar una devolución válida basándose en un dato inventado (ver
`comparacion_resultados.md`).
- **No cubre canales o idiomas fuera del alcance probado**: el prototipo solo valida texto en
español sobre pedidos y devoluciones; preguntas de catálogo/políticas generales necesitarían la
capa de RAG que se describe en la arquitectura (Fase 1) y que aún no está implementada.



## Riesgos Éticos

### Alucinaciones

En nuestro testeo y analisis encontramos que este es el riesgo más directo de este caso de uso. Un modelo generativo puede inventar una fecha de entrega, confirmar una devolución que no aplica, o inventar una política que no existe, y decirlo con el mismo tono seguro que una respuesta correcta. Se mitiga en dos niveles:

1. **Arquitectónico**: nunca se le pide al modelo que "sepa" el estado de un pedido; siempre se le
  entrega el dato real recuperado de `pedidos_tool.py`  como  contexto, y el prompt exige explícitamente no usar información fuera de ese contexto.
2. **De prompt**: las reglas de `PROMPT_ESTADO_PEDIDO` y `PROMPT_DEVOLUCION` instruyen al modelo a
  decir "no encontrado" cuando el contexto lo indica, en vez de completar el vacío con una
   suposición razonable pero falsa.

Aun así, ningún prompt elimina el riesgo al 100% con modelos pequeños — por eso en la Fase 3 se compararon dos backends, precisamente para medir con qué frecuencia cada uno se desvía del contexto entregado .

### Sesgo

En nuestra opinión, el riesgo de sesgo aquí es más sutil que en casos de decisión , pero existe, el modelo podría variar el tono de empatía o la disposición a "ayudar más" según el nombre del cliente, la ciudad de entrega, o el tipo de producto, si esos patrones estuvieran presentes en sus datos de entrenamiento. Por ejemplo, podría ser menos empático en una queja si el nombre del cliente "suena" de cierto origen, o asumir menor poder adquisitivo según la ciudad. Se mitiga estandarizando la instrucción de tono en el prompt  y auditando periódicamente respuestas reales para detectar variaciones no justificadas por el caso.

### Privacidad de datos

El contexto de cada pedido incluye datos personales y, en el prototipo, un campo explícitamente llamado **"notas internas"** que hoy se inyecta completo en el prompt. Esto es un riesgo real, si esa nota interna contuviera algo no apto para el cliente, el modelo podría repetirla textualmente en la respuesta. Por eso el prompt instruye a parafrasear esas notas en lenguaje de cliente en vez de citarlas litera pero consideramos la mitigación robusta es de diseño, no solo de prompt: en producción, ese campo no debería ni llegar al prompt si no está aprobado para cara al cliente. Además, si en el futuro se usa historial de conversaciones para fine-tuning, se debe anonimizar o excluir datos personales identificables, y limitar cuánto tiempo se retiene el contexto de cada conversación.

### Impacto laboral

El diseño propuesto en la Fase 1 no reemplaza al equipo de atención al cliente, automatiza específicamente el 80% repetitivo y escala el 20% complejo a un agente humano, incluso con un borrador de respuesta generado por el LLM como apoyo (human-in-the-loop). El objetivo es **redistribuir el trabajo humano** hacia los casos que sí requieren juicio y empatía genuina, en vez de que el equipo pase la mayoría de su tiempo respondiendo "¿dónde está mi pedido?". Aun así, es honesto reconocer el riesgo, si el volumen de consultas repetitivas cae drásticamente, la empresa podría necesitar menos agentes en el rol actual, y ese impacto en dotación debe gestionarse con transparencia.