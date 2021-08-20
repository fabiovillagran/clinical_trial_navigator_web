from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index.jinja"),
    path('results/', views.results, name="results.jinja"),
]