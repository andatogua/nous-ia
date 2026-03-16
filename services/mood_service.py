from repositories.patient_repository import PatientRepository
from repositories.emotion_repository import EmotionRepository
from repositories.mood_repository import MoodRepository


class MoodService:

    @staticmethod
    def get_emotions():
        return EmotionRepository.get_all_emotions()

    @staticmethod
    def register_mood(user_id, id_emocion, nivel_intensidad, observacion):
        patient = PatientRepository.get_patient_by_user_id(user_id)

        if not patient:
            return False, "No se encontró el paciente asociado al usuario."

        return MoodRepository.save_mood_record(
            patient["ID_PACIENTE"],
            id_emocion,
            nivel_intensidad,
            observacion
        )

    @staticmethod
    def get_mood_history(user_id):
        return MoodRepository.get_mood_history_by_user(user_id)