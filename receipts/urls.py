from django.urls import path
from . import views

urlpatterns = [
    path('process', views.ReceiptCreate.as_view(), name='process'),
    path('<str:pk>/points', views.ReceiptRetrieve.as_view(), name='points'),
]