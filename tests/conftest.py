"""Bootstrap Django for pytest runs with and without pytest-django."""

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
