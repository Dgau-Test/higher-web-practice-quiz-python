"""URL-маршруты API версии v1."""

from django.urls import path

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

urlpatterns = [
    path(
        'category',
        CategoryListCreateView.as_view(),
        name='category-list-create',
    ),
    path(
        'category/<int:id>',
        CategoryDetailView.as_view(),
        name='category-detail',
    ),
    path(
        'question',
        QuestionListCreateView.as_view(),
        name='question-list-create',
    ),
    path(
        'question/<int:id>',
        QuestionDetailView.as_view(),
        name='question-detail',
    ),
    path(
        'question/by_text/<str:text>',
        QuestionByTextView.as_view(),
        name='question-by-text',
    ),
    path(
        'question/<int:id>/check',
        QuestionCheckAnswerView.as_view(),
        name='question-check',
    ),
    path('quiz', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quiz/<int:id>', QuizDetailView.as_view(), name='quiz-detail'),
    path(
        'quiz/by_title/<str:title>',
        QuizByTitleView.as_view(),
        name='quiz-by-title',
    ),
    path(
        'quiz/<int:id>/random_question',
        QuizRandomQuestionView.as_view(),
        name='quiz-random-question',
    ),
]
