from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('process_youtube/', views.youtube_summary, name='process_youtube'),
]