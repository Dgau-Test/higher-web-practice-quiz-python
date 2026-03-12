"""Корневой роутинг версионированного API."""

from django.urls import include, path

urlpatterns = [
    path('v1/', include('quiz.api.v1.urls')),
]
