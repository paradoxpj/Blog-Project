from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('accounts/register/', views.signup_view, name="signup" ),
    path('home/', views.home, name="home"),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout', views.logout_view, name="logout"),
    path('upload/', views.PostCreate.as_view(), name="post_create"),
    path('search/', views.searchusers, name='search_results'),
]
