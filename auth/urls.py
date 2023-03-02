from django.urls import path
from .views import LoginGetTokenView, GetLoggedInUserDetailView

urlpatterns = [
    path('user/current/', GetLoggedInUserDetailView.as_view()),
    path('login/token/', LoginGetTokenView.as_view()),
]
