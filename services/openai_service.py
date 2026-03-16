import json
import re
from openai import OpenAI
from config.settings import Settings


class OpenAIService:

    @staticmethod
    def clean_text(value):
        """
        Elimina etiquetas HTML y espacios innecesarios.
        """
        if not value:
            return ""

        text = re.sub(r"<[^>]+>", "", str(value))
        text = text.replace("&nbsp;", " ")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def generate_recommendations(context_data):
        client = OpenAI(api_key=Settings.OPENAI_API_KEY)

        prompt = f"""
Eres un asistente de apoyo educativo en salud mental.

Tu tarea es generar exactamente 3 recomendaciones breves, empáticas, prácticas y fáciles de entender.

Reglas obligatorias:
- No des diagnósticos clínicos.
- No escribas textos largos.
- No uses lenguaje alarmista.
- Adapta el contenido a la edad del usuario.
- NO uses HTML.
- NO uses etiquetas como <div>, <span>, <br>, <p>.
- NO uses markdown.
- Devuelve SOLO texto plano dentro de cada campo.
- Cada campo debe contener una sola idea breve y clara.

Devuelve ÚNICAMENTE un JSON válido con esta estructura exacta:

{{
  "recomendaciones": [
    {{
      "titulo": "...",
      "descripcion": "...",
      "actividad_diaria": "...",
      "ejercicio_guiado": "...",
      "meta_semanal": "..."
    }},
    {{
      "titulo": "...",
      "descripcion": "...",
      "actividad_diaria": "...",
      "ejercicio_guiado": "...",
      "meta_semanal": "..."
    }},
    {{
      "titulo": "...",
      "descripcion": "...",
      "actividad_diaria": "...",
      "ejercicio_guiado": "...",
      "meta_semanal": "..."
    }}
  ]
}}

Datos del usuario:
{json.dumps(context_data, ensure_ascii=False)}
"""

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        text = response.output_text.strip()
        result = json.loads(text)

        # Limpieza extra por si la IA devuelve HTML o texto raro
        recomendaciones = result.get("recomendaciones", [])

        for rec in recomendaciones:
            rec["titulo"] = OpenAIService.clean_text(rec.get("titulo", ""))
            rec["descripcion"] = OpenAIService.clean_text(rec.get("descripcion", ""))
            rec["actividad_diaria"] = OpenAIService.clean_text(rec.get("actividad_diaria", ""))
            rec["ejercicio_guiado"] = OpenAIService.clean_text(rec.get("ejercicio_guiado", ""))
            rec["meta_semanal"] = OpenAIService.clean_text(rec.get("meta_semanal", ""))

        return {"recomendaciones": recomendaciones}