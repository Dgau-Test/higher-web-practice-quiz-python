"""Минимальная локальная реализация API django_filters для учебного проекта."""

from dataclasses import dataclass


@dataclass
class BaseFilter:
    """Базовый фильтр поля."""

    field_name: str
    lookup_expr: str = 'exact'

    def apply(self, queryset, value):
        """Применяет фильтр к queryset."""
        lookup = self.field_name
        if self.lookup_expr != 'exact':
            lookup = f'{lookup}__{self.lookup_expr}'
        return queryset.filter(**{lookup: value})


class CharFilter(BaseFilter):
    """Фильтр для строковых значений."""


class NumberFilter(BaseFilter):
    """Фильтр для числовых значений."""

    def apply(self, queryset, value):
        """Применяет числовой фильтр; невалидные значения игнорирует."""
        if isinstance(value, int):
            return super().apply(queryset, value)
        if isinstance(value, str) and value.isdigit():
            return super().apply(queryset, int(value))
        return queryset


class FilterSet:
    """Упрощенный аналог django_filters.FilterSet."""

    def __init__(self, data, queryset):
        """Инициализирует filterset и применяет фильтры к queryset."""
        self.data = data
        self.queryset = queryset
        self.qs = queryset
        self._apply_filters()

    @classmethod
    def declared_filters(cls):
        """Возвращает объявленные фильтры класса."""
        filters = {}
        for name, value in cls.__dict__.items():
            if isinstance(value, BaseFilter):
                filters[name] = value
        return filters

    def _apply_filters(self):
        """Применяет все фильтры из query params."""
        for name, filter_obj in self.declared_filters().items():
            value = self.data.get(name)
            if value in (None, ''):
                continue
            self.qs = filter_obj.apply(self.qs, value)

    def is_valid(self):
        """Сохраняет интерфейс django-filter (всегда True в упрощенной версии)."""
        return True
