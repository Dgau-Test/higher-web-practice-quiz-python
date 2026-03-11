"""Тесты роутинга API (versioned routes)."""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import resolve, reverse

from quiz.views.category import CategoryDetailView, CategoryListCreateView
from quiz.views.question import (
    QuestionByTextView,
    QuestionCheckAnswerView,
    QuestionDetailView,
    QuestionListCreateView,
)
from quiz.views.quiz import (
    QuizByTitleView,
    QuizDetailView,
    QuizListCreateView,
    QuizRandomQuestionView,
)


@pytest.mark.django_db
class TestApiRoutes:
    """Проверяет корректную сборку и резолв API маршрутов."""

    def test_reverse_builds_v1_paths(self) -> None:
        """Проверяет, что reverse строит URL с префиксом /api/v1/."""
        assert reverse('category-list-create') == '/api/v1/category'
        assert (
            reverse('category-detail', kwargs={'id': 1})
            == '/api/v1/category/1'
        )
        assert reverse('quiz-list-create') == '/api/v1/quiz'
        assert reverse('quiz-detail', kwargs={'id': 1}) == '/api/v1/quiz/1'
        assert (
            reverse('quiz-random-question', kwargs={'id': 1})
            == '/api/v1/quiz/1/random_question'
        )
        assert (
            reverse('quiz-by-title', kwargs={'title': 'Python'})
            == '/api/v1/quiz/by_title/Python'
        )
        assert reverse('question-list-create') == '/api/v1/question'
        assert (
            reverse('question-detail', kwargs={'id': 1})
            == '/api/v1/question/1'
        )
        assert (
            reverse('question-by-text', kwargs={'text': 'orm'})
            == '/api/v1/question/by_text/orm'
        )
        assert (
            reverse('question-check', kwargs={'id': 1})
            == '/api/v1/question/1/check'
        )

    def test_v1_urls_resolve_expected_views(self) -> None:
        """Проверяет соответствие URL и view-классов в v1."""
        assert (
            resolve('/api/v1/category').func.view_class
            is CategoryListCreateView
        )
        assert (
            resolve('/api/v1/category/1').func.view_class
            is CategoryDetailView
        )

        assert resolve('/api/v1/quiz').func.view_class is QuizListCreateView
        assert resolve('/api/v1/quiz/1').func.view_class is QuizDetailView
        assert (
            resolve('/api/v1/quiz/1/random_question').func.view_class
            is QuizRandomQuestionView
        )
        assert (
            resolve('/api/v1/quiz/by_title/Python').func.view_class
            is QuizByTitleView
        )

        assert (
            resolve('/api/v1/question').func.view_class
            is QuestionListCreateView
        )
        assert (
            resolve('/api/v1/question/1').func.view_class
            is QuestionDetailView
        )
        assert (
            resolve('/api/v1/question/by_text/orm').func.view_class
            is QuestionByTextView
        )
        assert (
            resolve('/api/v1/question/1/check').func.view_class
            is QuestionCheckAnswerView
        )

    def test_legacy_unversioned_paths_are_not_available(
        self, client: Client
    ) -> None:
        """Проверяет, что старые пути без версии не обслуживаются."""
        assert client.get('/api/category').status_code == HTTPStatus.NOT_FOUND
        assert client.get('/api/quiz').status_code == HTTPStatus.NOT_FOUND
        assert client.get('/api/question').status_code == HTTPStatus.NOT_FOUND

    def test_v2_placeholder_returns_404(self, client: Client) -> None:
        """Проверяет, что v2 пока заготовка без endpoint-ов."""
        assert (
            client.get('/api/v2/category').status_code
            == HTTPStatus.NOT_FOUND
        )
        assert (
            client.get('/api/v2/quiz').status_code == HTTPStatus.NOT_FOUND
        )
        assert (
            client.get('/api/v2/question').status_code
            == HTTPStatus.NOT_FOUND
        )
