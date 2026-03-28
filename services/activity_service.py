from repositories.activity_repository import ActivityRepository
from repositories.activity_emotional_tracking_repository import ActivityEmotionalTrackingRepository


class ActivityService:

    @staticmethod
    def extract_action_from_description(description):
        if not description:
            return ""

        text = str(description)

        if "Acción sugerida:" in text:
            parts = text.split("Acción sugerida:", 1)
            return parts[1].strip()

        return text.strip()

    @staticmethod
    def get_user_recommended_activities(user_id):
        recommendations = ActivityRepository.get_latest_recommendations_with_tracking(user_id, limit=15)
        emotional_tracking = ActivityEmotionalTrackingRepository.get_activity_emotional_tracking_by_user(user_id)

        tracking_map = {
            item["ID_RECOMENDACION"]: item
            for item in emotional_tracking
        }

        formatted = []
        for item in recommendations:
            tracking = tracking_map.get(item["ID_RECOMENDACION"])

            formatted.append({
                "id_recomendacion": item["ID_RECOMENDACION"],
                "titulo": item["TITULO"],
                "actividad": ActivityService.extract_action_from_description(item["DESCRIPCION"]),
                "realizada": tracking["REALIZADA"] if tracking else item["REALIZADA"],
                "ya_registrada": tracking is not None,
                "emocion_guardada": tracking["NOMBRE_EMOCION"] if tracking else None,
                "id_emocion_guardada": tracking["ID_EMOCION"] if tracking else None,
                "intensidad_guardada": tracking["NIVEL_INTENSIDAD"] if tracking else 3,
                "observacion_guardada": tracking["OBSERVACION"] if tracking else "",
                "ESTADO": item.get("ESTADO", "PENDIENTE")
            })

        return formatted

    @staticmethod
    def save_activity_emotional_tracking(
        user_id,
        id_recomendacion,
        id_emocion,
        nivel_intensidad,
        observacion,
        realizada
    ):
        ok_emotional, message_emotional = ActivityEmotionalTrackingRepository.save_activity_emotional_tracking(
            user_id,
            id_recomendacion,
            id_emocion,
            nivel_intensidad,
            observacion,
            realizada
        )

        if not ok_emotional:
            return False, message_emotional

        ok_tracking, message_tracking = ActivityRepository.save_tracking(
            user_id,
            id_recomendacion,
            realizada
        )

        if not ok_tracking:
            return False, message_tracking

        return True, "Actividad y estado emocional guardados correctamente."

    @staticmethod
    def get_activity_progress_summary(user_id):
        activities = ActivityService.get_user_recommended_activities(user_id)
        from models.recommendation import EstadoRecomendacion

        if not activities:
            return {
                "total": 0,
                "realizadas": 0,
                "no_realizadas": 0,
                "porcentaje_cumplimiento": 0
            }

        approved_activities = [a for a in activities if a.get("ESTADO", "PENDIENTE") == EstadoRecomendacion.APROBADO]
        total = len(approved_activities)
        realizadas = sum(1 for item in approved_activities if item["realizada"] in [True, 1])
        no_realizadas = total - realizadas
        porcentaje = round((realizadas / total) * 100, 2) if total > 0 else 0

        return {
            "total": total,
            "realizadas": realizadas,
            "no_realizadas": no_realizadas,
            "porcentaje_cumplimiento": porcentaje
        }