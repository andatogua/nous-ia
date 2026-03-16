from repositories.patient_repository import PatientRepository
from repositories.questionnaire_repository import QuestionnaireRepository
from repositories.evaluation_repository import EvaluationRepository


class EvaluationService:

    @staticmethod
    def get_questionnaire_data(code):
        questionnaire = QuestionnaireRepository.get_questionnaire_by_code(code)

        if not questionnaire:
            return None, [], []

        questions = QuestionnaireRepository.get_questions_by_questionnaire(
            questionnaire["ID_CUESTIONARIO"]
        )
        options = QuestionnaireRepository.get_options_by_questionnaire(
            questionnaire["ID_CUESTIONARIO"]
        )

        return questionnaire, questions, options

    @staticmethod
    def interpret_phq9(score):
        if score <= 4:
            return "Mínima", "Presencia mínima de síntomas depresivos.", False
        elif score <= 9:
            return "Leve", "Presencia leve de síntomas depresivos.", False
        elif score <= 14:
            return "Moderada", "Presencia moderada de síntomas depresivos.", True
        elif score <= 19:
            return "Moderadamente severa", "Presencia importante de síntomas depresivos.", True
        else:
            return "Severa", "Presencia severa de síntomas depresivos. Se recomienda atención profesional.", True

    @staticmethod
    def interpret_who5(score):
        score_scaled = score * 4

        if score_scaled >= 80:
            return "Bienestar alto", "El usuario presenta un nivel alto de bienestar emocional.", False, score_scaled
        elif score_scaled >= 52:
            return "Bienestar medio", "El usuario presenta un nivel intermedio de bienestar emocional.", False, score_scaled
        else:
            return "Bienestar bajo", "El usuario presenta bajo bienestar emocional. Se recomienda seguimiento.", True, score_scaled

    @staticmethod
    def save_single_evaluation(user_id, questionnaire_code, selected_answers):
        patient = PatientRepository.get_patient_by_user_id(user_id)

        if not patient:
            return False, "No se encontró el paciente asociado al usuario.", None

        questionnaire = QuestionnaireRepository.get_questionnaire_by_code(questionnaire_code)

        if not questionnaire:
            return False, "No se encontró el cuestionario.", None

        total_score = sum(answer["valor"] for answer in selected_answers)

        if questionnaire_code == "PHQ-9":
            nivel, interpretacion, requiere_atencion = EvaluationService.interpret_phq9(total_score)
            puntaje_escalado = None
        else:
            nivel, interpretacion, requiere_atencion, puntaje_escalado = EvaluationService.interpret_who5(total_score)

        ok_eval, id_evaluacion, msg_eval = EvaluationRepository.create_evaluation(
            patient["ID_PACIENTE"],
            questionnaire["ID_CUESTIONARIO"]
        )

        if not ok_eval:
            return False, msg_eval, None

        ok_answers, msg_answers = EvaluationRepository.save_answers(id_evaluacion, selected_answers)

        if not ok_answers:
            return False, msg_answers, None

        ok_result, msg_result = EvaluationRepository.save_result(
            id_evaluacion,
            total_score,
            puntaje_escalado,
            nivel,
            interpretacion,
            requiere_atencion
        )

        if not ok_result:
            return False, msg_result, None

        result_data = {
            "puntaje_total": total_score,
            "puntaje_escalado": puntaje_escalado,
            "nivel": nivel,
            "interpretacion": interpretacion,
            "requiere_atencion": requiere_atencion
        }

        return True, "Evaluación guardada correctamente.", result_data