from repositories.history_repository import HistoryRepository


class HistoryService:

    @staticmethod
    def get_user_history(user_id):
        return HistoryRepository.get_user_evaluation_history(user_id)