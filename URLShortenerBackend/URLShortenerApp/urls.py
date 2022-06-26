from django.urls import path
from .views import RegisterView, LoginView, UserView, URLShortenerView


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),

    path('urlshorten', URLShortenerView.as_view())
]