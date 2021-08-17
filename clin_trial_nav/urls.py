from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index.html"),
    path('results/', views.results, name="results.html"),
]