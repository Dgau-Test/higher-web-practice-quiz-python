"""Модуль с реализацией сервиса категорий."""

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from quiz.dao import AbstractCategoryService
from quiz.models import Category


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий."""

    @staticmethod
    def _base_queryset() -> QuerySet[Category]:
        """Базовый queryset категорий."""
        return Category.objects.all()

    def list_categories(self) -> list[Category]:
        """Возвращает список категорий."""
        return list(self._base_queryset())

    def get_category(self, category_id: int) -> Category:
        """Возвращает категорию по идентификатору."""
        return get_object_or_404(self._base_queryset(), id=category_id)

    def create_category(self, title: str) -> Category:
        """Создаёт категорию."""
        return Category.objects.create(title=title)

    def update_category(self, category_id: int, data: dict) -> Category:
        """Обновляет категорию."""
        category = self.get_category(category_id)
        if 'title' in data:
            category.title = data['title']
            category.save(update_fields=['title'])
        return category

    def delete_category(self, category_id: int) -> None:
        """Удаляет категорию."""
        category = self.get_category(category_id)
        category.delete()
