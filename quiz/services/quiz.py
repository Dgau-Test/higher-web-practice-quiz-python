"""Модуль с реализацией сервиса квизов."""

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuizService
from quiz.filters import QuizFilter
from quiz.models import Quiz


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза."""

    @staticmethod
    def _base_queryset() -> QuerySet[Quiz]:
        """Базовый queryset квизов."""
        return Quiz.objects.all()

    def list_quizzes(self) -> list[Quiz]:
        """Возвращает список квизов."""
        return list(self._base_queryset())

    def filter_quizzes(self, params: dict) -> list[Quiz]:
        """Возвращает список квизов с учетом query-параметров."""
        filterset = QuizFilter(params, queryset=self._base_queryset())
        filterset.is_valid()
        return list(filterset.qs)

    def get_quiz(self, quiz_id: int) -> Quiz:
        """Возвращает квиз по идентификатору."""
        return get_object_or_404(self._base_queryset(), id=quiz_id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """Возвращает список квизов по части названия."""
        return list(self._base_queryset().filter(title__icontains=title))

    def create_quiz(self, data: dict) -> Quiz:
        """Создаёт квиз."""
        return Quiz.objects.create(
            title=data['title'],
            description=data.get('description', ''),
        )

    def update_quiz(self, quiz_id: int, data: dict) -> Quiz:
        """Обновляет квиз."""
        quiz = self.get_quiz(quiz_id)
        update_fields = []

        if 'title' in data:
            quiz.title = data['title']
            update_fields.append('title')
        if 'description' in data:
            quiz.description = data['description']
            update_fields.append('description')

        if update_fields:
            quiz.save(update_fields=update_fields)
        return quiz

    def delete_quiz(self, quiz_id: int) -> None:
        """Удаляет квиз."""
        self.get_quiz(quiz_id).delete()
