"""Acceso a la base de datos mock de pedidos (data/pedidos.json).

Simula la integración con el sistema de pedidos de EcoMarket que se discute
en la Fase 1 (justificacion.md).
"""
import json
from pathlib import Path
from typing import Optional

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "pedidos.json"


def cargar_pedidos() -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def buscar_pedido(tracking_number: str) -> Optional[dict]:
    tracking_number = tracking_number.strip().upper()
    for pedido in cargar_pedidos():
        if pedido["tracking_number"].upper() == tracking_number:
            return pedido
    return None


def pedido_a_contexto(pedido: dict) -> str:
    """Serializa un pedido a texto plano para inyectarlo como contexto en un prompt."""
    if pedido is None:
        return "No se encontró ningún pedido con ese número de seguimiento."
    campos = [
        f"Número de seguimiento: {pedido['tracking_number']}",
        f"Cliente: {pedido['customer_name']}",
        f"Producto: {pedido['product']} (categoría: {pedido['product_category']})",
        f"¿Es devolvible?: {'sí' if pedido['returnable'] else 'no'}",
        f"Estado: {pedido['status']}",
        f"Fecha de pedido: {pedido['order_date']}",
        f"Entrega estimada: {pedido['estimated_delivery']}",
        f"Entrega real: {pedido['actual_delivery']}",
        f"Ciudad de entrega: {pedido['delivery_city']}",
    ]
    if pedido.get("notes"):
        campos.append(f"Notas internas: {pedido['notes']}")
    return "\n".join(campos)
