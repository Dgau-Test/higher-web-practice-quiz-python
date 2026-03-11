"""Тесты моделей и их мета-параметров."""

import pytest

from quiz.constants import (
    CATEGORY_TITLE_MAX_LENGTH,
    QUESTION_CORRECT_ANSWER_MAX_LENGTH,
    QUESTION_DESCRIPTION_MAX_LENGTH,
    QUESTION_EXPLANATION_MAX_LENGTH,
    QUESTION_OPTION_MAX_LENGTH,
    QUESTION_TEXT_MAX_LENGTH,
    QUIZ_DESCRIPTION_MAX_LENGTH,
    QUIZ_TITLE_MAX_LENGTH,
)
from quiz.models import Category, Difficulty, Question, QuestionOption, Quiz


@pytest.mark.django_db
class TestModelOrdering:
    """Тесты ordering из Meta."""

    def test_category_default_ordering_by_id(self) -> None:
        """Проверяет ordering категорий по id."""
        category_1 = Category.objects.create(title='Category B')
        category_2 = Category.objects.create(title='Category A')

        categories = list(Category.objects.all())
        assert [item.id for item in categories] == [
            category_1.id,
            category_2.id,
        ]

    def test_quiz_default_ordering_by_id(self) -> None:
        """Проверяет ordering квизов по id."""
        quiz_1 = Quiz.objects.create(title='Quiz B')
        quiz_2 = Quiz.objects.create(title='Quiz A')

        quizzes = list(Quiz.objects.all())
        assert [item.id for item in quizzes] == [quiz_1.id, quiz_2.id]

    def test_question_default_ordering_by_id(self) -> None:
        """Проверяет ordering вопросов по id."""
        category = Category.objects.create(title='Ordering category')
        quiz = Quiz.objects.create(title='Ordering quiz')
        question_1 = Question.objects.create(
            quiz=quiz,
            category=category,
            text='Question B',
            options=['1', '2'],
            correct_answer='1',
            difficulty=Difficulty.EASY,
        )
        question_2 = Question.objects.create(
            quiz=quiz,
            category=category,
            text='Question A',
            options=['1', '2'],
            correct_answer='2',
            difficulty=Difficulty.MEDIUM,
        )

        questions = list(Question.objects.all())
        assert [item.id for item in questions] == [
            question_1.id,
            question_2.id,
        ]


@pytest.mark.django_db
class TestModelFieldLengths:
    """Тесты граничных значений длины полей через full_clean."""

    def test_category_title_max_length_boundary(self) -> None:
        """Проверяет границу длины title категории."""
        category = Category(title='a' * CATEGORY_TITLE_MAX_LENGTH)
        category.full_clean()

    def test_quiz_field_max_length_boundaries(self) -> None:
        """Проверяет границы длины title/description квиза."""
        quiz = Quiz(
            title='a' * QUIZ_TITLE_MAX_LENGTH,
            description='b' * QUIZ_DESCRIPTION_MAX_LENGTH,
        )
        quiz.full_clean()

    def test_question_field_max_length_boundaries(self) -> None:
        """Проверяет границы длины текстовых полей вопроса."""
        category = Category.objects.create(title='Lengths category')
        quiz = Quiz.objects.create(title='Lengths quiz')
        question = Question(
            quiz=quiz,
            category=category,
            text='t' * QUESTION_TEXT_MAX_LENGTH,
            description='d' * QUESTION_DESCRIPTION_MAX_LENGTH,
            correct_answer='c' * QUESTION_CORRECT_ANSWER_MAX_LENGTH,
            explanation='e' * QUESTION_EXPLANATION_MAX_LENGTH,
            difficulty_id=Difficulty.HARD,
        )
        question.full_clean()

    def test_difficulty_lookup_seeded(self) -> None:
        """Проверяет заполнение справочника сложностей."""
        assert set(Difficulty.objects.values_list('code', flat=True)) == {
            Difficulty.EASY,
            Difficulty.MEDIUM,
            Difficulty.HARD,
        }

    def test_question_options_are_stored_in_separate_table(self) -> None:
        """Проверяет, что варианты ответа нормализованы в QuestionOption."""
        category = Category.objects.create(title='Options category')
        quiz = Quiz.objects.create(title='Options quiz')
        question = Question.objects.create(
            quiz=quiz,
            category=category,
            text='Question with many options',
            options=['opt1', 'opt2', 'opt3'],
            correct_answer='opt1',
            difficulty=Difficulty.EASY,
        )

        options = list(question.answer_options.values_list('text', flat=True))
        assert options == ['opt1', 'opt2', 'opt3']
        assert QuestionOption.objects.filter(question=question).count() == 3

    def test_question_option_text_max_length_boundary(self) -> None:
        """Проверяет граничную длину текста варианта ответа."""
        category = Category.objects.create(title='Option length category')
        quiz = Quiz.objects.create(title='Option length quiz')
        question = Question.objects.create(
            quiz=quiz,
            category=category,
            text='Question',
            options=['ok', 'also ok'],
            correct_answer='ok',
            difficulty=Difficulty.EASY,
        )
        option = QuestionOption(
            question=question,
            text='o' * QUESTION_OPTION_MAX_LENGTH,
            position=99,
        )
        option.full_clean()
