from http import HTTPStatus
from typing import Any

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

    @pytest.mark.parametrize(
        ('route_name', 'kwargs', 'expected_path'),
        [
            ('category-list-create', None, '/api/v1/category'),
            ('category-detail', {'id': 1}, '/api/v1/category/1'),
            ('quiz-list-create', None, '/api/v1/quiz'),
            ('quiz-detail', {'id': 1}, '/api/v1/quiz/1'),
            (
                'quiz-random-question',
                {'id': 1},
                '/api/v1/quiz/1/random_question',
            ),
            (
                'quiz-by-title',
                {'title': 'Python'},
                '/api/v1/quiz/by_title/Python',
            ),
            ('question-list-create', None, '/api/v1/question'),
            ('question-detail', {'id': 1}, '/api/v1/question/1'),
            (
                'question-by-text',
                {'text': 'orm'},
                '/api/v1/question/by_text/orm',
            ),
            ('question-check', {'id': 1}, '/api/v1/question/1/check'),
        ],
    )
    def test_reverse_builds_v1_paths(
        self,
        route_name: str,
        kwargs: dict | None,
        expected_path: str,
    ) -> None:
        """Проверяет, что reverse строит URL с префиксом /api/v1/."""
        if kwargs is None:
            assert reverse(route_name) == expected_path
            return
        assert reverse(route_name, kwargs=kwargs) == expected_path

    @pytest.mark.parametrize(
        ('path', 'view_class'),
        [
            ('/api/v1/category', CategoryListCreateView),
            ('/api/v1/category/1', CategoryDetailView),
            ('/api/v1/quiz', QuizListCreateView),
            ('/api/v1/quiz/1', QuizDetailView),
            ('/api/v1/quiz/1/random_question', QuizRandomQuestionView),
            ('/api/v1/quiz/by_title/Python', QuizByTitleView),
            ('/api/v1/question', QuestionListCreateView),
            ('/api/v1/question/1', QuestionDetailView),
            ('/api/v1/question/by_text/orm', QuestionByTextView),
            ('/api/v1/question/1/check', QuestionCheckAnswerView),
        ],
    )
    def test_v1_urls_resolve_expected_views(
        self, path: str, view_class: type[Any]
    ) -> None:
        """Проверяет соответствие URL и view-классов в v1."""
        assert resolve(path).func.view_class is view_class

    def test_legacy_unversioned_paths_are_not_available(
        self, client: Client
    ) -> None:
        """Проверяет, что старые пути без версии не обслуживаются."""
        assert client.get('/api/category').status_code == HTTPStatus.NOT_FOUND
        assert client.get('/api/quiz').status_code == HTTPStatus.NOT_FOUND
        assert client.get('/api/question').status_code == HTTPStatus.NOT_FOUND
