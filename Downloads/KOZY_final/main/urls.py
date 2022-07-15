from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name="main"),
    path('conversation/', views.conversation, name="conversation"),
    path('chat/', views.chat, name="chat"),
    path('register/', views.register, name="register")
]