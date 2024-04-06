from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('slgame', views.sololingo_game, name='slgame'),

    path('/login/', views.user_login, name='login'),
    path('/signup/', views.user_signup, name='signup'),
    path('/logout/', views.user_logout, name='logout'),
]