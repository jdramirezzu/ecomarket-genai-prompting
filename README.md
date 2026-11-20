> **English summary** — Coursework for the Master's in Applied AI (Generative AI course), by Juan Diego Ramírez and Mike Martínez. Designs an LLM-based customer-service assistant for a fictional e-commerce company: model selection and justification, ethical-risk analysis, and prompt engineering for order-status and returns requests. Continued in [ecomarket-rag-assistant](https://github.com/jdramirezzu/ecomarket-rag-assistant). The original deliverables below are in Spanish.

# Taller Práctico #1 — Optimización de la Atención al Cliente en EcoMarket

Repositorio de entrega para el caso de estudio de EcoMarket (Maestría en Inteligencia Artificial Generativa).

## Contenido

| Fase | Carpeta | Descripción |
|------|---------|-------------|
| Fase 1 — Selección y justificación del modelo | [`fase1_seleccion_modelo/justificacion.md`](fase1_seleccion_modelo/justificacion.md) | Qué modelo de IA generativa se propone y por qué |
| Fase 2 — Fortalezas, limitaciones y riesgos éticos | [`fase2_riesgos_eticos/evaluacion.md`](fase2_riesgos_eticos/evaluacion.md) | Análisis crítico de la solución propuesta |
| Fase 3 — Ingeniería de prompts | [`fase3_prompts/`](fase3_prompts/) | Código ejecutable con la cadena de prompts contra una base de datos mock de pedidos |

## Cómo está organizada la Fase 3

La Fase 3 compara dos backends de modelos **open-source** para evidenciar el impacto real de
los prompts y de la elección de modelo:

- **Ollama** (modelo local vía servidor Ollama, ej. Llama 3.2 / Qwen2.5)
- **Transformers** (modelo pequeño descargado y ejecutado directamente en Python)

Instrucciones de instalación y ejecución en [`fase3_prompts/README.md`](fase3_prompts/README.md).

## Estado de la entrega

- [x] Fase 1 respondida (`justificacion.md`) — borrador completo, pendiente ajustar con palabras propias
- [x] Fase 2 respondida (`evaluacion.md`) — borrador completo, pendiente ajustar con palabras propias
- [x] Prompts escritos en `fase3_prompts/src/prompts.py`
- [x] Comparación de resultados documentada (`fase3_prompts/comparacion_resultados.md`) — 9 casos de prueba corridos contra ambos backends
