from repositories.statistics_repository import StatisticsRepository


class StatisticsService:

    @staticmethod
    def get_user_statistics(user_id):

        data = StatisticsRepository.get_user_statistics(user_id)

        phq_scores = []
        who_scores = []

        for row in data:

            if row["CODIGO"] == "PHQ-9":
                phq_scores.append(row["PUNTAJE_TOTAL"])

            elif row["CODIGO"] == "WHO-5":

                if row["PUNTAJE_ESCALADO"]:
                    who_scores.append(row["PUNTAJE_ESCALADO"])

        total = len(data)

        avg_phq = sum(phq_scores)/len(phq_scores) if phq_scores else 0
        avg_who = sum(who_scores)/len(who_scores) if who_scores else 0

        return {
            "data": data,
            "total": total,
            "avg_phq": round(avg_phq,2),
            "avg_who": round(avg_who,2)
        }

    @staticmethod
    def get_global_statistics():
        patient_count = StatisticsRepository.get_global_patient_count()
        rec_stats = StatisticsRepository.get_global_recommendation_stats()
        eval_averages = StatisticsRepository.get_global_evaluation_averages()
        emotions = StatisticsRepository.get_emotions_frequency()
        activity_rate = StatisticsRepository.get_activity_completion_rate()
        evaluations_period = StatisticsRepository.get_evaluations_by_period(30)
        recent_users = StatisticsRepository.get_recent_users(10)
        
        return {
            "patients": patient_count,
            "recommendations": rec_stats,
            "evaluations": eval_averages,
            "emotions": emotions,
            "activity_rate": activity_rate,
            "evaluations_period": evaluations_period,
            "recent_users": recent_users
        }