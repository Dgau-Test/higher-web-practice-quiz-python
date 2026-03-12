from __future__ import annotations

import os
import sys
from pathlib import Path

import django
import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')


def pytest_configure() -> None:
    """Инициализирует Django для тестов."""
    try:
        django.setup()
    except ModuleNotFoundError as error:
        missing_module = error.name or 'unknown module'
        raise pytest.UsageError(
            'Missing dependency during Django startup: '
            f'"{missing_module}". '
            'Install project dependencies first, e.g.: '
            '`pip install -e .` or `uv sync`.'
        ) from error


@pytest.fixture
def categories_batch() -> list:
    """Создает набор категорий для проверок ordering."""
    from quiz.models import Category

    return [
        Category.objects.create(title=f'Category {index:02d}')
        for index in range(10, 0, -1)
    ]


@pytest.fixture
def quizzes_batch() -> list:
    """Создает набор квизов для проверок ordering."""
    from quiz.models import Quiz

    return [
        Quiz.objects.create(title=f'Quiz {index:02d}')
        for index in range(10, 0, -1)
    ]


@pytest.fixture
def questions_batch() -> list:
    """Создает набор вопросов для проверок ordering."""
    from quiz.models import Category, Difficulty, Question, Quiz

    category = Category.objects.create(title='Ordering category')
    quiz = Quiz.objects.create(title='Ordering quiz')
    return [
        Question.objects.create(
            quiz=quiz,
            category=category,
            text=f'Question {index:02d}',
            options=['1', '2'],
            correct_answer='1' if index % 2 == 0 else '2',
            difficulty=Difficulty.EASY,
        )
        for index in range(10, 0, -1)
    ]
