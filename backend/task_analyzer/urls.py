"""Root URL configuration for Task Analyzer."""
from django.urls import include, path


urlpatterns = [
    path("api/tasks/", include("tasks.urls")),
]

