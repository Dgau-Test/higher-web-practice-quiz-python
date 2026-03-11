"""Модуль с контроллерами для вопросов."""

from http import HTTPStatus
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.constants import CHECK_ANSWER_REQUIRED_ERROR
from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService


class QuestionBaseView(APIView):
    """Базовый класс для операций с вопросами."""

    service = QuestionService()

    def _build_question_payload(self, validated_data: dict) -> dict:
        """Собирает единый payload для сервисного слоя."""
        return {
            'quiz_id': validated_data['quiz'].id,
            'category_id': validated_data['category'].id,
            'text': validated_data['text'],
            'description': validated_data.get('description', ''),
            'options': validated_data['options'],
            'correct_answer': validated_data['correct_answer'],
            'explanation': validated_data.get('explanation', ''),
            'difficulty': validated_data['difficulty'],
        }


class QuestionListCreateView(QuestionBaseView):
    """Создание и список вопросов."""

    def get(self, request: Request) -> Response:
        """Возвращает список вопросов."""
        questions = self.service.filter_questions(request.GET)
        return Response(QuestionSerializer(questions, many=True).data)

    def post(self, request: Request) -> Response:
        """Создаёт вопрос."""
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = self._build_question_payload(serializer.validated_data)
        question = self.service.create_question(
            quiz_id=payload['quiz_id'], data=payload
        )
        return Response(
            QuestionSerializer(question).data, status=HTTPStatus.CREATED
        )


class QuestionDetailView(QuestionBaseView):
    """Операции с конкретным вопросом."""

    service = QuestionService()

    def get(self, request: Request, id: int) -> Response:
        """Возвращает вопрос по id."""
        question = self.service.get_question(id)
        return Response(QuestionSerializer(question).data)

    def put(self, request: Request, id: int) -> Response:
        """Обновляет вопрос."""
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self._build_question_payload(serializer.validated_data)
        question = self.service.update_question(id, data)
        return Response(QuestionSerializer(question).data)

    def delete(self, request: Request, id: int) -> Response:
        """Удаляет вопрос."""
        self.service.delete_question(id)
        return Response(status=HTTPStatus.NO_CONTENT)


class QuestionByTextView(APIView):
    """Поиск вопросов по тексту."""

    service = QuestionService()

    def get(self, request: Request, text: str) -> Response:
        """Возвращает вопросы по части текста."""
        questions = self.service.get_questions_by_text(text)
        return Response(QuestionSerializer(questions, many=True).data)


class QuestionCheckAnswerView(APIView):
    """Проверка ответа."""

    service = QuestionService()

    def post(self, request: Request, id: int) -> Response:
        """Проверяет ответ на вопрос."""
        answer = request.data.get('answer', '')
        if not isinstance(answer, str) or not answer.strip():
            return Response(
                {'detail': CHECK_ANSWER_REQUIRED_ERROR},
                status=HTTPStatus.BAD_REQUEST,
            )
        return Response({'is_correct': self.service.check_answer(id, answer)})
