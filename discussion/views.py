from rest_framework import generics, permissions
from .models import Question, Answer
from .permissions import IsOwnerOrReadOnly
from .serializers import QuestionSerializer, AnswerSerializer
from typing import List
from .services.answers import AnswerService
from rest_framework.exceptions import NotFound, ValidationError


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self) -> List[permissions.BasePermission]:
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer: QuestionSerializer) -> None:
        user = self.request.user
        serializer.save(user=user)

class QuestionRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrReadOnly]


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer) -> None:
        question_id: int = self.kwargs["pk"]
        user = self.request.user
        text: str = serializer.validated_data["text"]
        try:
            answer: Answer = AnswerService.create_answer(
                question_id=question_id,
                user=user,
                text=text
            )
            serializer.instance = answer
        except Question.DoesNotExist:
            raise NotFound(detail=f"Question with id={question_id} not found.")
        except Exception as e:
            raise ValidationError({"detail": str(e)})

class AnswerRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrReadOnly]
