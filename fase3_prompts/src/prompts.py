"""Plantillas de prompt para los dos ejercicios de la Fase 3.

*** ESTA ES LA PARTE QUE DEBES ESCRIBIR TÚ ***
La rúbrica del taller (1 punto) califica directamente la calidad de estos
prompts: la estructura, el rol que le das al modelo, y cómo usas el contexto
del pedido para lograr una respuesta clara y (cuando aplica) empática.

Guía del enunciado (ver PDF, Fase 3):
- Ejercicio 1: el modelo debe informar el estado de un pedido dado un
  tracking_number, incluyendo fecha estimada de entrega y, si hay retraso,
  una disculpa y una breve explicación.
- Ejercicio 2: el modelo debe guiar una devolución, distinguiendo productos
  devolvibles de los que no (perecederos, higiene), con una respuesta clara
  y empática incluso cuando la devolución no es posible.

Las variables {contexto_pedido} y {mensaje_cliente} se rellenan en
run_chat.py con los datos reales de data/pedidos.json antes de enviarse al
modelo. No cambies esos nombres de variable si quieres que run_chat.py siga
funcionando; si quieres otros nombres, ajusta también run_chat.py.
"""

# TODO: Ejercicio 1 — Prompt de Solicitud de Pedido.
# Reemplaza este placeholder por tu propio prompt (system + instrucciones).
PROMPT_ESTADO_PEDIDO = """
TODO: escribe aquí tu prompt para el ejercicio de estado de pedido.

Contexto del pedido (datos reales, no inventes nada fuera de esto):
{contexto_pedido}

Mensaje del cliente:
{mensaje_cliente}
"""

# TODO: Ejercicio 2 — Prompt de Devolución de Producto.
# Reemplaza este placeholder por tu propio prompt (system + instrucciones).
PROMPT_DEVOLUCION = """
TODO: escribe aquí tu prompt para el ejercicio de devolución de producto.

Contexto del pedido (datos reales, no inventes nada fuera de esto):
{contexto_pedido}

Mensaje del cliente:
{mensaje_cliente}
"""
