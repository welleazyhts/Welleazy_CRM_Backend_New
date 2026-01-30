from django.urls import path
from .views import SecondOpinionCaseAPI

urlpatterns = [
    path("cases/", SecondOpinionCaseAPI.as_view()),
]
