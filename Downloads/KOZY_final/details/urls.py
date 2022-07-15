from django.urls import path
from . import views

app_name = 'details'

urlpatterns = [
    path('', views.details, name="details"),
    path('bookmark/', views.bookmark, name="bookmark"),
    path('todo/', views.index),
    path('new/', views.create),
    path('complete/', views.mark_complete),
    path('uncomplete/', views.mark_uncomplete),
    path('delete/',views.delete ),
    path('search/',views.search ),
]