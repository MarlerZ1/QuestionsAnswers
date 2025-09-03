import pytest
from django.contrib.auth import get_user_model
from discussion.models import Answer, Question
from discussion.permissions import IsOwnerOrReadOnly
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

User = get_user_model()


@pytest.fixture
def users(db) -> tuple[User, User]:
    user1 = User.objects.create_user(username="owner", password="pass1234")
    user2 = User.objects.create_user(username="another", password="pass1234")
    return user1, user2


@pytest.fixture
def question(db) -> Question:
    return Question.objects.create(text="Тестовый вопрос")


@pytest.fixture
def answer(users: tuple[User, User], question: Question) -> Answer:
    user1, _ = users
    return Answer.objects.create(
        question=question,
        user_id=user1.id,
        text="Ответ владельца"
    )


@pytest.fixture
def factory() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.fixture
def permission() -> IsOwnerOrReadOnly:
    return IsOwnerOrReadOnly()


def test_safe_method_allowed(
    factory: APIRequestFactory,
    users: tuple[User, User],
    answer: Answer,
    permission: IsOwnerOrReadOnly
) -> None:
    _, user2 = users
    request: Request = factory.get("/fake-url/")
    request.user = user2

    assert permission.has_object_permission(request, None, answer)


def test_owner_can_modify(
    factory: APIRequestFactory,
    users: tuple[User, User],
    answer: Answer,
    permission: IsOwnerOrReadOnly
) -> None:
    user1, _ = users
    request: Request = factory.delete("/fake-url/")
    request.user = user1

    assert permission.has_object_permission(request, None, answer)


def test_non_owner_cannot_modify(
    factory: APIRequestFactory,
    users: tuple[User, User],
    answer: Answer,
    permission: IsOwnerOrReadOnly
) -> None:
    _, user2 = users
    request: Request = factory.delete("/fake-url/")
    request.user = user2

    assert not permission.has_object_permission(request, None, answer)
