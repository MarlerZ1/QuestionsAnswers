from discussion.models import Answer, Question
from django.contrib.auth import get_user_model

User = get_user_model()


class AnswerService:
    @staticmethod
    def create_answer(question_id: int, user: User, text: str) -> Answer:
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.create(
            question=question,
            user_id=user.id,
            text=text
        )
        return answer
