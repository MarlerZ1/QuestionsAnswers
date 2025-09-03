from rest_framework import serializers
from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True,
        min_length=1,
        max_length=2000,
    )

    class Meta:
        model = Answer
        fields = ["id", "question", "user_id", "text", "created_at"]
        read_only_fields = ["id", "user_id", "created_at", "question"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    text = serializers.CharField(
        required=True,
        min_length=1,
        max_length=2000,
    )

    class Meta:
        model = Question
        fields = ["id", "text", "created_at", "answers"]
        read_only_fields = ["id", "created_at", "answers"]
