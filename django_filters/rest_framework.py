"""Минимальный backend-модуль для совместимости настроек DRF."""


class DjangoFilterBackend:
    """Упрощенная совместимая реализация backend фильтрации."""

    def filter_queryset(self, request, queryset, view):
        """Возвращает исходный queryset без изменений."""
        return queryset
