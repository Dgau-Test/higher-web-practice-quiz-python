from __future__ import annotations

from django.db import models


class QuestionManager(models.Manager):
    """Менеджер вопроса с поддержкой удобного `options` при create."""

    def create(self, **kwargs) -> Question:
        """Создаёт вопрос и связанные варианты ответов."""
        options = kwargs.pop('options', None)
        difficulty = kwargs.get('difficulty')

        if isinstance(difficulty, str):
            kwargs.pop('difficulty')
            kwargs['difficulty_id'] = difficulty

        question = super().create(**kwargs)

        if options is not None:
            question.replace_options(options)

        return question
