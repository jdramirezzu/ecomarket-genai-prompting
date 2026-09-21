# Comparación de resultados: Ollama vs. Transformers local

> Completa esta tabla corriendo `src/run_chat.py --backend ambos` con al menos dos casos por
> ejercicio (ver tracking numbers en `data/pedidos.json`).

## Ejercicio 1: Estado de pedido

| Tracking | Caso | Respuesta Ollama (resumen) | Respuesta Transformers (resumen) | Observaciones |
|----------|------|------------------------------|-------------------------------------|----------------|
| ECM-1002 | Pedido en tránsito normal | | | |
| ECM-1004 | Pedido retrasado | | | |

## Ejercicio 2: Devolución de producto

| Tracking | Caso | Respuesta Ollama (resumen) | Respuesta Transformers (resumen) | Observaciones |
|----------|------|------------------------------|-------------------------------------|----------------|
| ECM-1005 | Producto devolvible | | | |
| ECM-1001 | Producto de higiene (no devolvible) | | | |

## Análisis

### ¿Qué diferencias notaste en calidad, precisión o empatía entre los dos backends?

_(Tu respuesta aquí)_

### ¿En qué casos alucinó o falló alguno de los modelos?

_(Tu respuesta aquí)_

### ¿En qué escenario se justificaría usar un modelo más potente (ej. Hugging Face Inference con un modelo grande, o un modelo de pago como GPT-4)?

<!-- Conecta esto con tu justificación de la Fase 1: costo vs. calidad vs. escalabilidad. -->

_(Tu respuesta aquí)_
