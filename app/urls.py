from django.urls import path
from .views import *


urlpatterns = [
    path('todos/', TodosView.as_view()),
]