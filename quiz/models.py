"""Модуль c моделями приложения quiz."""

from django.db import models

from quiz.constants import (
    CATEGORY_TITLE_MAX_LENGTH,
    DIFFICULTY_MAX_LENGTH,
    QUESTION_CORRECT_ANSWER_MAX_LENGTH,
    QUESTION_DESCRIPTION_MAX_LENGTH,
    QUESTION_EXPLANATION_MAX_LENGTH,
    QUESTION_OPTION_MAX_LENGTH,
    QUESTION_TEXT_MAX_LENGTH,
    QUIZ_DESCRIPTION_MAX_LENGTH,
    QUIZ_TITLE_MAX_LENGTH,
)


class Category(models.Model):
    """Модель категории вопросов."""

    title = models.CharField(
        max_length=CATEGORY_TITLE_MAX_LENGTH,
        verbose_name='Название категории',
        help_text='Краткое название категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.title


class Quiz(models.Model):
    """Модель квиза."""

    title = models.CharField(
        max_length=QUIZ_TITLE_MAX_LENGTH,
        verbose_name='Название квиза',
        help_text='Краткое название квиза',
    )
    description = models.CharField(
        max_length=QUIZ_DESCRIPTION_MAX_LENGTH,
        blank=True,
        default='',
        verbose_name='Описание квиза',
        help_text='Короткое описание квиза',
    )

    class Meta:
        verbose_name = 'Квиз'
        verbose_name_plural = 'Квизы'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.title


class Difficulty(models.Model):
    """Справочник сложностей вопросов."""

    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

    code = models.CharField(
        max_length=DIFFICULTY_MAX_LENGTH,
        primary_key=True,
        verbose_name='Код сложности',
    )
    title = models.CharField(max_length=32, verbose_name='Название сложности')

    class Meta:
        verbose_name = 'Сложность'
        verbose_name_plural = 'Сложности'
        ordering = ('code',)

    def __str__(self) -> str:
        return self.title


class QuestionManager(models.Manager):
    """Менеджер вопроса с поддержкой удобного `options` при create."""

    def create(self, **kwargs) -> 'Question':
        """Создает вопрос и связанные варианты ответов."""
        options = kwargs.pop('options', None)
        difficulty = kwargs.get('difficulty')
        if isinstance(difficulty, str):
            kwargs.pop('difficulty')
            kwargs['difficulty_id'] = difficulty

        question = super().create(**kwargs)
        if options is not None:
            question.replace_options(options)
        return question


class Question(models.Model):
    """Модель вопроса."""

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Квиз',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='questions',
        verbose_name='Категория',
    )
    text = models.CharField(
        max_length=QUESTION_TEXT_MAX_LENGTH,
        verbose_name='Текст вопроса',
    )
    description = models.CharField(
        max_length=QUESTION_DESCRIPTION_MAX_LENGTH,
        blank=True,
        default='',
        verbose_name='Описание вопроса',
    )
    correct_answer = models.CharField(
        max_length=QUESTION_CORRECT_ANSWER_MAX_LENGTH,
        verbose_name='Правильный ответ',
    )
    explanation = models.CharField(
        max_length=QUESTION_EXPLANATION_MAX_LENGTH,
        blank=True,
        default='',
        verbose_name='Объяснение ответа',
    )
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.PROTECT,
        related_name='questions',
        verbose_name='Сложность',
    )

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.text

    @property
    def options(self) -> list[str]:
        """Возвращает варианты ответа как список строк."""
        return list(
            self.answer_options.order_by('position').values_list(
                'text', flat=True
            )
        )

    def replace_options(self, options: list[str]) -> None:
        """Полностью заменяет набор вариантов ответа у вопроса."""
        self.answer_options.all().delete()
        QuestionOption.objects.bulk_create(
            [
                QuestionOption(
                    question=self,
                    text=option,
                    position=index,
                )
                for index, option in enumerate(options)
            ]
        )


class QuestionOption(models.Model):
    """Нормализованный вариант ответа для вопроса."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer_options',
        verbose_name='Вопрос',
    )
    text = models.CharField(
        max_length=QUESTION_OPTION_MAX_LENGTH,
        verbose_name='Текст варианта',
    )
    position = models.PositiveIntegerField(verbose_name='Позиция варианта')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ('position', 'id')
        constraints = [
            models.UniqueConstraint(
                fields=('question', 'position'),
                name='uniq_question_option_position',
            )
        ]

    def __str__(self) -> str:
        return self.text
