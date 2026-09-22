"""Backends de modelos open-source intercambiables.

Permite ejecutar el mismo prompt contra dos motores distintos para comparar
resultados (ver comparacion_resultados.md):

- OllamaBackend: modelo local servido por Ollama (https://ollama.com).
- TransformersBackend: modelo pequeño descargado y ejecutado con la
  librería `transformers` de Hugging Face, sin servicios externos.
"""
from abc import ABC, abstractmethod


class ModelBackend(ABC):
    name: str

    @abstractmethod
    def generate(self, prompt: str, max_new_tokens: int = 300) -> str:
        ...


class OllamaBackend(ModelBackend):
    """Requiere tener Ollama corriendo localmente (`ollama serve`) y el modelo
    descargado, ej.: `ollama pull llama3.2`.
    """

    def __init__(self, model_name: str = "qwen2.5:7b"):
        self.name = f"ollama:{model_name}"
        self.model_name = model_name

    def generate(self, prompt: str, max_new_tokens: int = 300) -> str:
        import ollama

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            options={"num_predict": max_new_tokens},
        )
        return response["response"].strip()


class TransformersBackend(ModelBackend):
    """Descarga y ejecuta un modelo pequeño localmente con `transformers`.

    Modelo por defecto: Qwen2.5-1.5B-Instruct (abierto, liviano, corre en CPU).
    Puedes cambiarlo por otro modelo instruct pequeño si tu máquina lo permite.
    """

    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        self.name = f"transformers:{model_name}"
        self.model_name = model_name
        self._pipe = None

    def _load(self):
        if self._pipe is None:
            from transformers import pipeline

            self._pipe = pipeline(
                "text-generation",
                model=self.model_name,
                device_map="auto",
            )
        return self._pipe

    def generate(self, prompt: str, max_new_tokens: int = 300) -> str:
        pipe = self._load()
        messages = [{"role": "user", "content": prompt}]
        output = pipe(messages, max_new_tokens=max_new_tokens, do_sample=False)
        return output[0]["generated_text"][-1]["content"].strip()


def get_backend(name: str) -> ModelBackend:
    if name == "ollama":
        return OllamaBackend()
    if name == "transformers":
        return TransformersBackend()
    raise ValueError(f"Backend desconocido: {name}")
