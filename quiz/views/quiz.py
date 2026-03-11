"""Модуль с контроллерами для квизов."""

from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Question, Quiz
from quiz.serializers import QuestionSerializer, QuizSerializer
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


class QuizListCreateView(APIView):
    """Создание и список квизов."""

    service = QuizService()

    def get(self, request: Request) -> Response:
        """Возвращает список квизов."""
        quizzes = self.service.filter_quizzes(request.GET)
        return Response(QuizSerializer(quizzes, many=True).data)

    def post(self, request: Request) -> Response:
        """Создаёт квиз."""
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = self.service.create_quiz(serializer.validated_data)
        return Response(QuizSerializer(quiz).data, status=HTTPStatus.CREATED)


class QuizDetailView(APIView):
    """Операции с конкретным квизом."""

    service = QuizService()

    def get(self, request: Request, id: int) -> Response:
        """Возвращает квиз."""
        quiz = self.service.get_quiz(id)
        return Response(QuizSerializer(quiz).data)

    def put(self, request: Request, id: int) -> Response:
        """Обновляет квиз."""
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = self.service.update_quiz(id, serializer.validated_data)
        return Response(QuizSerializer(quiz).data)

    def delete(self, request: Request, id: int) -> Response:
        """Удаляет квиз."""
        self.service.delete_quiz(id)
        return Response(status=HTTPStatus.NO_CONTENT)


class QuizByTitleView(APIView):
    """Список квизов по названию."""

    service = QuizService()

    def get(self, request: Request, title: str) -> Response:
        """Возвращает список квизов по части названия."""
        quizzes = self.service.get_quizes_by_title(title)
        return Response(QuizSerializer(quizzes, many=True).data)


class QuizRandomQuestionView(APIView):
    """Случайный вопрос из квиза."""

    question_service = QuestionService()

    def get(self, request: Request, id: int) -> Response:
        """Возвращает случайный вопрос для квиза."""
        get_object_or_404(Quiz, id=id)
        get_object_or_404(Question.objects.filter(quiz_id=id)[:1])
        question = self.question_service.random_question_from_quiz(id)
        return Response(QuestionSerializer(question).data)
