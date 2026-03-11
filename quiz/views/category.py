"""Модуль с контроллерами для категорий."""

from http import HTTPStatus
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService


class CategoryListCreateView(APIView):
    """Создание и список категорий."""

    service = CategoryService()

    def get(self, request: Request) -> Response:
        """Возвращает список категорий."""
        categories = self.service.list_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Создаёт категорию."""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = self.service.create_category(
            serializer.validated_data['title']
        )
        return Response(
            CategorySerializer(category).data, status=HTTPStatus.CREATED
        )


class CategoryDetailView(APIView):
    """Операции с конкретной категорией."""

    service = CategoryService()

    def get(self, request: Request, id: int) -> Response:
        """Возвращает категорию."""
        category = self.service.get_category(id)
        return Response(CategorySerializer(category).data)

    def put(self, request: Request, id: int) -> Response:
        """Обновляет категорию."""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = self.service.update_category(id, serializer.validated_data)
        return Response(CategorySerializer(category).data)

    def delete(self, request: Request, id: int) -> Response:
        """Удаляет категорию."""
        self.service.delete_category(id)
        return Response(status=HTTPStatus.NO_CONTENT)
