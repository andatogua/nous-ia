import json
import re
from openai import OpenAI
from config.settings import Settings


class OpenAIService:

    @staticmethod
    def clean_text(value):
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

        Tu tarea es generar exactamente 15 recomendaciones personalizadas, breves, empáticas, prácticas y fáciles de entender.

        Debes construir las recomendaciones obligatoriamente en función de:
        - nombre del usuario
        - edad
        - puntaje, nivel e interpretación del PHQ-9
        - puntaje, nivel e interpretación del WHO-5
        - último estado emocional registrado, si existe

        Además, debes tomar como referencia general criterios educativos y de apoyo basados en NICE NG222, entendida como una guía clínica basada en evidencia para la evaluación y manejo de la depresión.

        Objetivo:
        Brindar sugerencias educativas y de autocuidado que ayuden al usuario a reflexionar sobre su bienestar emocional, fortalecer hábitos saludables y realizar actividades sencillas de seguimiento emocional.

        Reglas obligatorias:
        - No des diagnósticos clínicos.
        - No reemplaces atención psicológica o psiquiátrica profesional.
        - No uses lenguaje alarmista, extremo o amenazante.
        - No menciones autolesión, suicidio ni contenidos de crisis, salvo sugerir de forma general buscar apoyo profesional cuando corresponda.
        - Adapta el contenido a la edad del usuario.
        - Usa un tono cálido, respetuoso, claro, humano y motivador.
        - Cada recomendación debe ser distinta.
        - Cada recomendación debe ser breve, útil, realista y aplicable en la vida diaria.
        - Las sugerencias deben enfocarse en autocuidado, descanso, organización personal, regulación emocional, apoyo social, rutinas saludables y seguimiento emocional.
        - También puedes incluir pequeñas actividades prácticas como respiración, pausas activas, caminatas breves, registro emocional, organización del sueño, contacto social positivo y hábitos de bienestar.
        - Las recomendaciones deben ser coherentes con los resultados del usuario, pero también alineadas de forma general con el enfoque educativo de NICE NG222.
        - No cites textualmente la guía.
        - No inventes tratamientos clínicos ni medicación.
        - Todas las acciones sugeridas deben tener enfoque diario.
        - Cada accion_sugerida debe ser una actividad que el usuario pueda realizar hoy o durante el día actual.
        - Evita acciones semanales, mensuales, indefinidas o de largo plazo.
        - Evita frases como "esta semana", "durante el mes", "con el tiempo" o "más adelante".
        - Prioriza acciones pequeñas, claras y realizables en el mismo día.
        - La accion_sugerida debe iniciar preferiblemente con expresiones como "Hoy", "Durante el día de hoy", "Esta noche" o "En este momento", cuando tenga sentido natural.
        - NO uses HTML.
        - NO uses markdown.
        - Devuelve SOLO texto plano.
        - Devuelve exactamente 15 recomendaciones.
        - Cada recomendación debe tener únicamente estos 3 campos:
          - titulo
          - descripcion
          - accion_sugerida

        Indicaciones sobre el contenido:
        - "titulo" debe ser corto, claro y motivador.
        - "descripcion" debe explicar brevemente por qué esa recomendación puede ayudar al usuario.
        - "accion_sugerida" debe ser una acción concreta, sencilla y realizable por el usuario en el día actual, útil también para el seguimiento emocional del sistema.

        Devuelve ÚNICAMENTE un JSON válido con esta estructura exacta:

        {{
          "recomendaciones": [
            {{
              "titulo": "...",
              "descripcion": "...",
              "accion_sugerida": "..."
            }}
          ]
        }}

        Asegúrate de que el arreglo contenga exactamente 15 objetos.

        Datos del usuario:
        {json.dumps(context_data, ensure_ascii=False)}
        """

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        text = response.output_text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        result = json.loads(text)
        recomendaciones = result.get("recomendaciones", [])

        cleaned_recommendations = []
        for rec in recomendaciones:
            cleaned_recommendations.append({
                "titulo": OpenAIService.clean_text(rec.get("titulo", "")),
                "descripcion": OpenAIService.clean_text(rec.get("descripcion", "")),
                "accion_sugerida": OpenAIService.clean_text(rec.get("accion_sugerida", ""))
            })

        return {"recomendaciones": cleaned_recommendations}