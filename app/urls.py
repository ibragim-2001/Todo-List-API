from django.urls import path
from .views import *


urlpatterns = [
    path('todos/', TodosView.as_view()),
    path('todos/<int:pk>/', TodoItemVIew.as_view()),
]