"""Модуль c сериализаторами"""

from rest_framework import serializers

from quiz.constants import (
    CORRECT_ANSWER_NOT_IN_OPTIONS_ERROR,
    MIN_OPTIONS_COUNT,
    OPTIONS_MIN_COUNT_ERROR,
    QUESTION_OPTION_MAX_LENGTH,
)
from quiz.models import Category, Difficulty, Question, Quiz


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        model = Category
        fields = ('id', 'title')


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов"""

    options = serializers.ListField(
        child=serializers.CharField(max_length=QUESTION_OPTION_MAX_LENGTH)
    )
    difficulty = serializers.SlugRelatedField(
        slug_field='code', queryset=Difficulty.objects.all()
    )

    class Meta:
        model = Question
        fields = (
            'id',
            'quiz',
            'category',
            'text',
            'description',
            'options',
            'correct_answer',
            'explanation',
            'difficulty',
        )

    def to_representation(self, instance: Question) -> dict:
        """Возвращает объект вопроса вместе со списком вариантов ответа."""
        data = super().to_representation(instance)
        data['options'] = instance.options
        return data

    def validate_options(self, value: list[str]) -> list[str]:
        """Проверяет, что options содержит минимум два варианта."""
        if len(value) < MIN_OPTIONS_COUNT:
            raise serializers.ValidationError(OPTIONS_MIN_COUNT_ERROR)
        return value

    def validate(self, attrs: dict) -> dict:
        """Проверяет согласованность correct_answer и options."""
        options = attrs.get('options')
        correct_answer = attrs.get('correct_answer')
        if (
            options is not None
            and correct_answer is not None
            and correct_answer not in options
        ):
            raise serializers.ValidationError(
                {'correct_answer': CORRECT_ANSWER_NOT_IN_OPTIONS_ERROR}
            )
        return attrs


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для квизов"""

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description')
