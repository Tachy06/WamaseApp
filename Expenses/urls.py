from django.urls import path
from .views import *

urlpatterns = [
    path('add_expenses/', expenseView.as_view(), name='Expenses'),
    path('view_expenses_user/', expenseViewUser.as_view(), name='Expenses-User'),
    path('delete_expenses/<int:expense_id>/', deleteExpense.as_view(), name='Delete_expense'),
]