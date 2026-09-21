"""CLI para ejecutar los prompts de la Fase 3 contra uno o ambos backends.

Ejemplos:
    python src/run_chat.py --ejercicio pedido --tracking ECM-1004 \
        --mensaje "¿Dónde está mi pedido?" --backend ollama

    python src/run_chat.py --ejercicio devolucion --tracking ECM-1001 \
        --mensaje "Quiero devolver este producto" --backend ambos
"""
import argparse

from backends import get_backend
from pedidos_tool import buscar_pedido, pedido_a_contexto
from prompts import PROMPT_DEVOLUCION, PROMPT_ESTADO_PEDIDO

PROMPTS_POR_EJERCICIO = {
    "pedido": PROMPT_ESTADO_PEDIDO,
    "devolucion": PROMPT_DEVOLUCION,
}


def construir_prompt(ejercicio: str, tracking: str, mensaje: str) -> str:
    pedido = buscar_pedido(tracking)
    contexto = pedido_a_contexto(pedido)
    plantilla = PROMPTS_POR_EJERCICIO[ejercicio]
    return plantilla.format(contexto_pedido=contexto, mensaje_cliente=mensaje)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ejercicio", choices=["pedido", "devolucion"], required=True)
    parser.add_argument("--tracking", required=True, help="Número de seguimiento, ej. ECM-1001")
    parser.add_argument("--mensaje", required=True, help="Mensaje del cliente")
    parser.add_argument(
        "--backend", choices=["ollama", "transformers", "ambos"], default="ambos"
    )
    args = parser.parse_args()

    prompt_final = construir_prompt(args.ejercicio, args.tracking, args.mensaje)
    print("=" * 80)
    print("PROMPT ENVIADO AL MODELO:")
    print("=" * 80)
    print(prompt_final)

    backends_a_ejecutar = ["ollama", "transformers"] if args.backend == "ambos" else [args.backend]

    for nombre_backend in backends_a_ejecutar:
        backend = get_backend(nombre_backend)
        print("\n" + "=" * 80)
        print(f"RESPUESTA ({backend.name}):")
        print("=" * 80)
        try:
            print(backend.generate(prompt_final))
        except Exception as e:
            print(f"[Error ejecutando {backend.name}: {e}]")


if __name__ == "__main__":
    main()
