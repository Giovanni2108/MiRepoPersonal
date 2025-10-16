import os
try:
    import requests
except Exception:
    requests = None

def get_response(user_text: str) -> str:
    """
    Devuelve la respuesta del chatbot.
    Si existe CHATBOT_API_URL en las variables de entorno, intenta llamar a esa API.
    Si falla o no está configurada, usa respuestas locales simples (fallback).
    """
    api_url = os.environ.get("CHATBOT_API_URL")
    api_key = os.environ.get("CHATBOT_API_KEY")

    # Si hay URL y requests disponible, intenta llamar a la API
    if api_url and requests is not None:
        try:
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            payload = {"message": user_text}
            resp = requests.post(api_url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Extrae respuesta en estructuras comunes
            if isinstance(data, dict):
                for key in ("answer", "response", "text", "message"):
                    if key in data and isinstance(data[key], str):
                        return data[key]
                if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                    ch = data["choices"][0]
                    return ch.get("text") or ch.get("message", {}).get("content") or str(ch)
            return str(data)
        except Exception as e:
            return f"(chatbot api error) {e}"

    # Fallback local simple por reglas
    txt = (user_text or "").strip()
    low = txt.lower()
    # Saludo
    if any(w in low for w in ("hola", "buenas", "buenos", "buenos dias", "buenas tardes")):
        return "¡Hola! Soy tu asistente financiero. ¿En qué puedo ayudarte hoy? Puedes preguntarme sobre presupuesto, ahorro, inversión o impuestos."

    # Finanzas generales
    if "finanzas" in low:
        return (
            "Aquí tienes algunos pasos prácticos:\n"
            "1) Registra tus ingresos y gastos durante 1 mes.\n"
            "2) Crea un presupuesto simple (50/30/20 es un comienzo).\n"
            "3) Automatiza transferencias hacia tu ahorro cada vez que cobres.\n"
            "Si quieres, puedo ayudarte a crear un esquema de presupuesto."
        )

    # Impuestos
    if "impuesto" in low or "impuestos" in low:
        return (
            "Consejos rápidos sobre impuestos:\n"
            "- Mantén ordenados tus comprobantes y facturas.\n"
            "- Revisa deducciones y beneficios fiscales aplicables.\n"
            "- Si tu situación es compleja, consulta a un contador.\n"
            "¿Quieres que te explique cómo preparar un paquete de documentos para un contador?"
        )

    # Inversiones
    if "invers" in low or "invertir" in low:
        return (
            "Principios básicos de inversión:\n"
            "- Define tu horizonte temporal y tolerancia al riesgo.\n"
            "- Diversifica (fondos indexados son una opción eficiente).\n"
            "- Evita decisiones impulsivas basadas en noticias.\n"
            "¿Te interesa ver opciones de inversión a largo plazo o corto plazo?"
        )

    # Emprendimiento
    if "emprend" in low or "negocio" in low:
        return (
            "Si estás emprendiendo, te recomiendo:\n"
            "1) Validar tu idea con potenciales clientes.\n"
            "2) Calcular costos fijos y variables mínimos.\n"
            "3) Probar un MVP de bajo costo antes de escalar.\n"
            "Puedo ayudarte a estructurar un plan sencillo de 1 página si quieres."
        )

    # Pregunta de clarificación por defecto
    return (
        "No estoy seguro de entender completamente. ¿Puedes darme más detalles sobre lo que necesitas?\n"
        "Por ejemplo: 'quiero ahorrar para X', 'cómo declaro mis impuestos', o 'cómo invertir 1000 USD'."
    )
