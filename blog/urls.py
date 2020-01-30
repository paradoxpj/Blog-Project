from django.urls import path
from . import views


app_name = "blog"

urlpatterns = [
    path('accounts/register/', views.signup, name="signup" ),
    path('home/', views.home, name="home"),
]
