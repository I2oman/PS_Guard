from django.urls import path
from . import views

urlpatterns = [
    path('', views.psgSearch),
    path('<str:nick>', views.psgUser),
    path('<str:nick>/<str:game>', views.psgTitle),
]
