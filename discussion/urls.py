from typing import List

from django.urls import path
from .views import (
    QuestionListCreateView,
    QuestionRetrieveDestroyView,
    AnswerCreateView,
    AnswerRetrieveDestroyView,
)

app_name: str = 'discussion'

urlpatterns: List = [
    path("questions/", QuestionListCreateView.as_view(), name="questions-list-create"),
    path("questions/<int:pk>/", QuestionRetrieveDestroyView.as_view(), name="questions-retrieve-destroy"),
    path("questions/<int:pk>/answers/", AnswerCreateView.as_view(), name="answers-create"),
    path("answers/<int:pk>/", AnswerRetrieveDestroyView.as_view(), name="answers-retrieve-destroy"),
]
