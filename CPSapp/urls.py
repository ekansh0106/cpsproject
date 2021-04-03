from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('aboutme/', views.about),
    path('page2/', views.disp),
]