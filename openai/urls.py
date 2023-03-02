from django.urls import path
from . import views
from .views import OpenAIChatCompletion
from django.views.generic.base import TemplateView

urlpatterns = [
    path('chat/completions/', OpenAIChatCompletion.as_view()),
]
