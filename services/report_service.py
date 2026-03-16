from repositories.report_repository import ReportRepository
from repositories.recommendation_repository import RecommendationRepository


class ReportService:

    @staticmethod
    def get_progress_summary(user_id):

        data = ReportRepository.get_progress_data(user_id)

        if not data:
            return {
                "data": [],
                "first_phq9": None,
                "last_phq9": None,
                "first_who5": None,
                "last_who5": None,
                "latest_mood": None
            }

        first_phq9 = None
        last_phq9 = None
        first_who5 = None
        last_who5 = None

        for row in data:
            if row["CODIGO"] == "PHQ-9":

                if first_phq9 is None:
                    first_phq9 = row

                last_phq9 = row

            elif row["CODIGO"] == "WHO-5":

                if first_who5 is None:
                    first_who5 = row

                last_who5 = row

        latest_mood = RecommendationRepository.get_latest_mood(user_id)

        return {
            "data": data,
            "first_phq9": first_phq9,
            "last_phq9": last_phq9,
            "first_who5": first_who5,
            "last_who5": last_who5,
            "latest_mood": latest_mood
        }