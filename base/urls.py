from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('register/', views.registerPage, name = "register"),
    path('', views.home, name = "home"),
    path('logout/', views.logout_view, name = 'logout'),
    path('about/', views.aboutUs, name = "aboutUs"),
    path('petitions/', views.petitions, name = "petitions"),
    path('create-petition', views.create_petition, name = "create-petition"),
]