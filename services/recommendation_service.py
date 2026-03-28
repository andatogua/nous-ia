from datetime import date
import re
import html

from repositories.recommendation_repository import RecommendationRepository
from repositories.profile_repository import ProfileRepository
from services.openai_service import OpenAIService


class RecommendationService:

    @staticmethod
    def calculate_age(birth_date):
        if not birth_date:
            return None

        today = date.today()
        age = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    @staticmethod
    def clean_text(text):
        if not text:
            return ""

        text = str(text)
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def generate_user_recommendations(user_id):
        profile = ProfileRepository.get_user_profile(user_id)
        latest_results = RecommendationRepository.get_latest_evaluation_results(user_id)
        latest_mood = RecommendationRepository.get_latest_mood(user_id)

        if not profile:
            return False, "No se pudo obtener el perfil del usuario.", []

        if "PHQ-9" not in latest_results or "WHO-5" not in latest_results:
            return False, "Se necesitan resultados recientes de PHQ-9 y WHO-5.", []

        age = RecommendationService.calculate_age(profile["FECHA_NACIMIENTO"])

        phq = latest_results["PHQ-9"]
        who = latest_results["WHO-5"]

        if latest_mood and latest_mood.get("FECHA_REGISTRO"):
            latest_mood["FECHA_REGISTRO"] = latest_mood["FECHA_REGISTRO"].isoformat()

        context_data = {
            "usuario": {
                "nombre": profile["NOMBRE"],
                "apellido": profile["APELLIDO"],
                "nombre_completo": f"{profile['NOMBRE']} {profile['APELLIDO']}"
            },
            "edad": int(age) if age is not None else None,
            "phq9": {
                "puntaje_total": int(phq["PUNTAJE_TOTAL"]),
                "nivel": phq["NIVEL_RESULTADO"],
                "interpretacion": phq["INTERPRETACION"]
            },
            "who5": {
                "puntaje_total": int(who["PUNTAJE_TOTAL"]),
                "puntaje_escalado": float(who["PUNTAJE_ESCALADO"]),
                "nivel": who["NIVEL_RESULTADO"],
                "interpretacion": who["INTERPRETACION"]
            },
            "ultimo_estado_emocional": latest_mood
        }

        result = OpenAIService.generate_recommendations(context_data)
        recommendations = result.get("recomendaciones", [])

        if not recommendations:
            return False, "La IA no devolvió recomendaciones válidas.", []

        saved = []
        target_result_id = phq["ID_RESULTADO"]

        for rec in recommendations:
            titulo = RecommendationService.clean_text(rec.get("titulo", ""))
            descripcion = RecommendationService.clean_text(rec.get("descripcion", ""))
            accion_sugerida = RecommendationService.clean_text(rec.get("accion_sugerida", ""))

            descripcion_completa = (
                f"Descripción: {descripcion}\n\n"
                f"Acción sugerida: {accion_sugerida}"
            )

            ok, _ = RecommendationRepository.save_recommendation(
                target_result_id,
                user_id,
                titulo if titulo else "Recomendación",
                descripcion_completa
            )

            if ok:
                saved.append({
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "accion_sugerida": accion_sugerida
                })

        if not saved:
            return False, "No se pudieron guardar las recomendaciones generadas.", []

        return True, "Recomendaciones generadas correctamente.", saved