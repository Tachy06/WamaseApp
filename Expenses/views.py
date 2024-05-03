from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Expenses
from django.contrib import messages
# Create your views here.
class expenseView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'add_expenses.html')
    def post(self, request):
        expense = request.POST['expense']
        amount = request.POST['amount']
        user = User.objects.get(username=request.user)
        Expenses.objects.create(user=user, title=expense, amount=amount)
        messages.success(request, 'Creado exitosamente')
        return redirect('/expenses/')