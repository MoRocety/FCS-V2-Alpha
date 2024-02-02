# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('retrieve_courses/', views.retrieve_courses, name='retrieve_courses'),
    path('add_course/', views.add_course, name='add_course'),
    path('filter_sections/', views.filter_sections, name='filter_sections'),  
]
