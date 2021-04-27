from . import views
from django.urls import path

urlpatterns = [
    path('home/', views.home),
    path('aboutme/', views.about),
    path('page2/', views.disp),
    path('page3/', views.disp),
    path('mumbai/', views.mum),
    path('delhi/', views.delhi),
    path('goa/', views.goa),
    path('manali/', views.man),
    path('rajasthan/', views.raj),
    path('news/', views.news),
]