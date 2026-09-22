# Fase 3 — Ingeniería de Prompts (código ejecutable)

## Qué hay aquí

- `data/pedidos.json` — base de datos mock con 11 pedidos (roles de prueba para los prompts).
- `src/pedidos_tool.py` — búsqueda de pedidos por número de seguimiento.
- `src/backends.py` — dos motores de modelo intercambiables: Ollama (local) y Transformers (local).
- `src/prompts.py` — **plantillas de prompt a completar** (ver TODOs, esta es la parte que escribe el estudiante).
- `src/run_chat.py` — script que arma el prompt final con datos reales del pedido y lo ejecuta contra uno o ambos backends.
- `comparacion_resultados.md` — plantilla para documentar tus observaciones al comparar los dos backends.

## Instalación

```bash
cd fase3_prompts
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Backend Ollama (opcional, si quieres usarlo)

1. Instala Ollama: https://ollama.com/download
2. Descarga un modelo, ej.: `ollama pull qwen2.5:7b`
3. Asegúrate de que el servicio esté corriendo (`ollama serve`, normalmente arranca solo).

> En esta máquina ya está instalado Ollama 0.34.0 con los modelos `qwen2.5:7b` (por defecto en
> `backends.py`), `gemma4:26b`, `llama2` y `abhinema/gpt2-wikitext`. Puedes cambiar el modelo
> pasando otro nombre a `OllamaBackend(model_name=...)`.

### Backend Transformers

No requiere instalación adicional: la primera vez que lo uses, descargará el modelo
`Qwen/Qwen2.5-1.5B-Instruct` (~3GB) automáticamente desde Hugging Face.
Puedes cambiar el modelo en `src/backends.py` (`TransformersBackend.__init__`).

## Cómo ejecutar

Primero completa tus prompts en `src/prompts.py` (los TODOs). Luego:

```bash
cd src
python run_chat.py --ejercicio pedido --tracking ECM-1004 \
  --mensaje "¿Dónde está mi pedido?" --backend ollama

python run_chat.py --ejercicio devolucion --tracking ECM-1001 \
  --mensaje "Quiero devolver este producto" --backend transformers

# Comparar ambos backends con el mismo prompt:
python run_chat.py --ejercicio pedido --tracking ECM-1004 \
  --mensaje "¿Dónde está mi pedido?" --backend ambos
```

Números de tracking de prueba disponibles: ECM-1001 a ECM-1011 (ver `data/pedidos.json`
para casos con retraso, producto perecedero, producto de higiene, devuelto, etc.).

## Qué documentar en `comparacion_resultados.md`

Corre tus dos prompts (pedido y devolución) contra ambos backends con al menos dos casos
distintos cada uno (ej. un pedido normal y uno retrasado; un producto devolvible y uno que no)
y registra tus observaciones: diferencias de calidad, alucinaciones, y en qué escenario
justificarías pasar a un modelo más potente (ej. vía Hugging Face Inference API o un modelo
de pago como GPT-4).
