"""Фильтры для списковых эндпоинтов quiz-приложения."""

import django_filters

from quiz.models import Question, Quiz


class QuizFilter(django_filters.FilterSet):
    """Фильтр квизов."""

    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains'
    )

    class Meta:
        model = Quiz
        fields = ('title',)


class QuestionFilter(django_filters.FilterSet):
    """Фильтр вопросов."""

    text = django_filters.CharFilter(
        field_name='text', lookup_expr='icontains'
    )
    quiz = django_filters.NumberFilter(field_name='quiz_id')

    class Meta:
        model = Question
        fields = (
            'text',
            'quiz',
        )
