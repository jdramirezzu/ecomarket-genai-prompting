# Comparación de resultados: Ollama vs. Transformers local



## Ejercicio 1: Estado de pedido


| Tracking | Caso                                                                                        | Respuesta Ollama (qwen2.5:7b) (resumen)                                                                                                               | Respuesta Transformers (Qwen2.5-1.5B) (resumen)                                                                                                                                                                                         | Observaciones                                                                                                                                       |
| -------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| ECM-1002 | En tránsito, normal                                                                         | Correcta y concisa: estado + fecha estimada.                                                                                                          | Correcta, algo más larga, personaliza con el nombre del cliente.                                                                                                                                                                        | Ambos bien.                                                                                                                                         |
| ECM-1004 | Retrasado                                                                                   | Correcta: disculpa breve, motivo parafraseado ("congestión en centro de distribución"), sin inventar fecha nueva.                                     | **Alucinación**: inventa una fecha de entrega nueva ("2026-09-17") que no está en el contexto, violando la regla de no prometer fechas no confirmadas. También escribe mal el tracking ("EC-MARKET-1004").                              | Diferencia clara a favor de Ollama en seguir instrucciones.                                                                                         |
| ECM-1006 | Cancelado                                                                                   | Correcta en contenido, pero menciona literalmente "nuestras notas internas" al cliente — filtra terminología interna que el prompt pedía parafrasear. | Correcta y sin mencionar "notas internas".                                                                                                                                                                                              | Aquí Transformers respetó mejor la regla de privacidad del prompt.                                                                                  |
| ECM-1007 | Ya devuelto                                                                                 | Correcta, breve, tono apropiado (no habla de retraso ni tránsito).                                                                                    | Verbosa (~6 frases, excede el límite de 2-4 pedido en el prompt), mezcla estado de entrega y devolución de forma algo confusa.                                                                                                          | Ollama respetó mejor el formato pedido.                                                                                                             |
| ECM-1002 | Fuera de tema ("¿Cuál es la capital de Francia?") — prueba del guardrail agregado al prompt | Sigue el guardrail exactamente: "No podemos ayudarte con eso."                                                                                        | **Falla el guardrail y alucina**: ignora la pregunta fuera de tema y responde sobre el pedido diciendo que "ha sido entregado correctamente" el 22 de septiembre, cuando el contexto dice `Estado: en tránsito` y `Entrega real: None`. | El hallazgo más claro de todo el set: el modelo pequeño no solo ignora una regla explícita, sino que inventa un dato factual falso sobre el pedido. |




## Ejercicio 2: Devolución de producto


| Tracking | Caso                                                            | Respuesta Ollama (qwen2.5:7b) (resumen)                                                                                                            | Respuesta Transformers (Qwen2.5-1.5B) (resumen)                                                                                                                                                                                                                                                    | Observaciones                                                                                                                         |
| -------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| ECM-1001 | No devolvible (higiene)                                         | Correcta y empática, motivo bien parafraseado.                                                                                                     | Correcta, pero **inventa una alternativa no autorizada** ("solicitar un cambio o un regalo similar") que no existe en el contexto ni en ninguna política dada.                                                                                                                                     | Ambos con buen tono, pero Transformers se excede inventando una solución.                                                             |
| ECM-1008 | No devolvible (perecedero)                                      | Correcta, concisa, motivo claro.                                                                                                                   | Correcta y concisa también.                                                                                                                                                                                                                                                                        | Caso más simple, ambos backends lo resolvieron bien.                                                                                  |
| ECM-1005 | Devolvible, entregado, dentro de ventana                        | Correcta en el fondo, pero **inventa un correo de contacto** ("[soporte@ecomarket.com](mailto:soporte@ecomarket.com)") que no está en el contexto. | **Alucinación grave**: inventa que el producto "ya ha sido instalado y utilizado" (dato que no existe en el contexto) y usa esa invención para **negar una devolución que sí debería proceder** (returnable=sí, dentro de ventana). Además ignora el formato pedido (usa saludo/firma tipo carta). | El caso más grave del set: Transformers no solo alucina un dato, sino que ese dato lo lleva a dar la respuesta de negocio incorrecta. |
| ECM-1002 | Devolvible pero **aún no entregado** (caso especial del prompt) | Correcta: identifica que no puede iniciarse la devolución porque el pedido no ha llegado, y explica el siguiente paso.                             | Maneja mal el caso especial: dice "es devolvible" y da pasos numerados para iniciar la devolución, mencionando la condición de "si no ha llegado" solo como nota al margen en vez de bloquear el proceso. También usa una lista numerada, violando la regla de formato.                            | Ollama manejó correctamente la regla 3 del prompt; Transformers la aplicó de forma débil.                                             |




## Análisis



### ¿Qué diferencias notaste en calidad, precisión o empatía entre los dos backends?

En tono y empatía ambos backends son comparables: los dos redactan con cortesía y explican los motivos de forma comprensible. La diferencia grande está en **la precisión y que tanto pueden seguir instrucciones**: `qwen2.5:7b` (Ollama) siguió consistentemente las reglas del prompt (formato,
guardrail, no inventar fechas/contactos, manejar el caso especial de devolución antes de entrega),
mientras que `Qwen2.5-1.5B-Instruct` (Transformers) las siguió de forma irregular; a veces correcto, a veces con fallas de formato (listas, saludos/firmas) o de contenido. El modelo más grande también fue, en general, más conciso, mientras el 1.5B tiende a extenderse más allá del límite de frases pedido.

### ¿En qué casos alucinó o falló alguno de los modelos?

Se registraron alucinaciones y fallas en varios casos, casi todas del lado de Transformers
(1.5B), aunque Ollama tampoco quedó completamente libre:

- **Transformers, ECM-1004**: inventó una fecha de entrega nueva no presente en el contexto.
- **Transformers, guardrail (ECM-1002 con pregunta fuera de tema)**: ignoró la instrucción de
rechazar preguntas no relacionadas y además inventó que el pedido "ya fue entregado" cuando el
estado real era "en tránsito" — la falla más seria porque combina incumplimiento de instrucción
con un dato factual falso.
- **Transformers, ECM-1001**: inventó una alternativa de resolución (cambio/regalo) no contemplada
en ninguna política del contexto.
- **Transformers, ECM-1005**: el caso más grave — inventó que el producto "ya fue instalado y
utilizado" y usó ese dato inventado para negar una devolución que, según los datos reales, sí
debía proceder. Esto es un error que en producción tendría impacto directo en la experiencia del
cliente (una devolución legítima siendo rechazada por una alucinación).
- **Transformers, ECM-1002 (devolución antes de entrega)**: no bloqueó con claridad el caso
especial de "producto aún no entregado", diluyendo una regla de negocio importante.
- **Ollama, ECM-1006**: mencionó literalmente "notas internas" al cliente, filtrando terminología
que el prompt pedía mantener interna.
- **Ollama, ECM-1005**: inventó un correo de contacto (`soporte@ecomarket.com`) que no estaba en el
contexto ni se le proporcionó — un recordatorio de que incluso el modelo más grande puede
alucinar detalles "plausibles" si el prompt no lo restringe explícitamente a no inventar canales
de contacto.



### ¿En qué escenario se justificaría usar un modelo más potente (ej. Hugging Face Inference con un modelo grande, o un modelo de pago como GPT-4)?

El caso de negar una devolución válida por un dato inventado con Transformers  es el tipo de error que puede ser grave y justificaría subir de modelo si se repitiera con frecuencia en producción: es un error de negocio con consecuencia directa al cliente, no solo un problema de estilo. Si al escalar las pruebas (más casos, más variaciones de mensaje del cliente) la tasa de alucinaciones de un modelo pequeño se mantiene alta, particularmente en el ejercicio de devolución, donde una alucinación puede traducirse en una decisión de negocio equivocada, se justificaría pasar a un modelo más potente (vía Hugging Face Inference API con un modelo mayor, o un modelo de pago tipo GPT-4) al menos para ese ejercicio específico, manteniendo el modelo barato para el caso más simple y de menor riesgo. Esto conecta con la arquitectura de la Fase 1: el objetivo del piloto era justo detectar en qué punto el beneficio marginal de un modelo más caro supera su costo, y esta comparación ya da evidencia concreta de que, para el ejercicio de devolución con el modelo 1.5B, ese punto se alcanzó.