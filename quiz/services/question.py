"""Модуль с реализацией сервиса вопросов."""

from django.db.models import QuerySet
from django.db.models.functions import Random
from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuestionService
from quiz.filters import QuestionFilter
from quiz.models import Difficulty, Question, Quiz


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов."""

    @staticmethod
    def _base_queryset() -> QuerySet[Question]:
        """Базовый queryset для вопросов с заранее подтянутыми связями."""
        return Question.objects.select_related(
            'quiz', 'category', 'difficulty'
        ).prefetch_related('answer_options')

    def list_questions(self) -> list[Question]:
        """Возвращает все вопросы."""
        return list(self._base_queryset().all())

    def filter_questions(self, params: dict) -> list[Question]:
        """Возвращает список вопросов с учетом query-параметров."""
        filterset = QuestionFilter(
            params, queryset=self._base_queryset().all()
        )
        filterset.is_valid()
        return list(filterset.qs)

    def get_question(self, question_id: int) -> Question:
        """Возвращает вопрос по id."""
        return get_object_or_404(self._base_queryset(), id=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        """Возвращает список вопросов по части текста."""
        return list(self._base_queryset().filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        """Возвращает вопросы квиза."""
        return list(self._base_queryset().filter(quiz_id=quiz_id))

    def create_question(self, quiz_id: int, data: dict) -> Question:
        """Создаёт вопрос в квизе."""
        get_object_or_404(Quiz, id=quiz_id)
        category_id = data.get('category_id', data.get('category'))
        difficulty = data['difficulty']
        difficulty_id = (
            difficulty.code
            if isinstance(difficulty, Difficulty)
            else difficulty
        )
        return Question.objects.create(
            quiz_id=quiz_id,
            category_id=category_id,
            text=data['text'],
            description=data.get('description', ''),
            options=data['options'],
            correct_answer=data['correct_answer'],
            explanation=data.get('explanation', ''),
            difficulty_id=difficulty_id,
        )

    def update_question(self, question_id: int, data: dict) -> Question:
        """Обновляет вопрос."""
        question = self.get_question(question_id)
        update_fields = []
        for field in (
            'quiz_id',
            'category_id',
            'text',
            'description',
            'correct_answer',
            'explanation',
        ):
            if field in data:
                setattr(question, field, data[field])
                update_fields.append(field)

        if 'difficulty' in data:
            difficulty = data['difficulty']
            question.difficulty_id = (
                difficulty.code
                if isinstance(difficulty, Difficulty)
                else difficulty
            )
            update_fields.append('difficulty')

        if update_fields:
            question.save(update_fields=update_fields)

        if 'options' in data:
            question.replace_options(data['options'])
        return question

    def delete_question(self, question_id: int) -> None:
        """Удаляет вопрос."""
        question = self.get_question(question_id)
        question.delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        """Проверяет ответ пользователя."""
        question = self.get_question(question_id)
        return (
            question.correct_answer.strip().lower()
            == answer.strip().lower()
        )

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        """Возвращает случайный вопрос квиза."""
        get_object_or_404(Quiz, id=quiz_id)
        random_question_id = (
            Question.objects.filter(quiz_id=quiz_id)
            .order_by(Random())
            .values_list('id', flat=True)[:1]
            .get()
        )
        return self._base_queryset().get(id=random_question_id)
