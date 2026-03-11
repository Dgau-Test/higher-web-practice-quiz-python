"""Тесты сериализаторов."""

import pytest

from quiz.models import Category, Difficulty, Quiz
from quiz.serializers import QuestionSerializer


@pytest.mark.django_db
class TestQuestionSerializer:
    """Тесты валидации QuestionSerializer."""

    def setup_method(self) -> None:
        """Подготавливает связанные объекты."""
        self.category = Category.objects.create(title='Serializer category')
        self.quiz = Quiz.objects.create(title='Serializer quiz')

    def _base_payload(self) -> dict:
        """Возвращает валидный базовый payload."""
        return {
            'quiz': self.quiz.id,
            'category': self.category.id,
            'text': 'What is Python?',
            'description': 'base question',
            'options': ['Language', 'Snake'],
            'correct_answer': 'Language',
            'explanation': 'It is both, but context is programming language',
            'difficulty': Difficulty.EASY,
        }

    def test_serializer_accepts_valid_payload(self) -> None:
        """Проверяет, что валидный payload проходит валидацию."""
        serializer = QuestionSerializer(data=self._base_payload())
        assert serializer.is_valid(), serializer.errors

    def test_serializer_rejects_options_with_single_value(self) -> None:
        """Проверяет ошибку при options меньше двух значений."""
        payload = self._base_payload()
        payload['options'] = ['Only one']

        serializer = QuestionSerializer(data=payload)
        assert serializer.is_valid() is False
        assert 'options' in serializer.errors

    def test_serializer_rejects_correct_answer_not_in_options(self) -> None:
        """Проверяет ошибку, если correct_answer отсутствует в options."""
        payload = self._base_payload()
        payload['correct_answer'] = 'Not in options'

        serializer = QuestionSerializer(data=payload)
        assert serializer.is_valid() is False
        assert 'correct_answer' in serializer.errors
