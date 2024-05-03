from django.urls import path
from .views import *

urlpatterns = [
    path('expenses/', expenseView.as_view(), name='Expenses'),
]