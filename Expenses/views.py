from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Expenses
from django.contrib import messages
# Create your views here.
class AddExpenses(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        cars = User.objects.all()
        return render(request, 'add_expenses.html', {'cars': cars})
    def post(self, request):
        if request.user.is_superuser:
            car = request.POST['car']
            if car == '0':
                messages.error(request, 'Seleccione un vehiculo')
                return redirect('/add_expenses/')
            car_id = User.objects.get(id=car)
            expense = request.POST['expense']
            amount = request.POST['amount']
            description = request.POST['description']
            Expenses.objects.create(user=car_id, title=expense, description=description, amount=float(amount))
            messages.success(request, 'Creado exitosamente')
            return redirect('/add_expenses/')
        else:
            car_id = User.objects.get(username=request.user)
            expense = request.POST['expense']
            amount = request.POST['amount']
            description = request.POST['description']
            Expenses.objects.create(user=car_id, title=expense, description=description, amount=float(amount))
            messages.success(request, 'Creado exitosamente')
            return redirect('/add_expenses/')
    
class expenseViewUser(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        expenses = Expenses.objects.filter(user=request.user)
        amount = 0
        for expense in expenses:
            amount = amount + expense.amount
        total = amount
        return render(request, 'view_expensesUser.html', {'expenses': expenses, 'total': total})
    
class deleteExpense(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, expense_id):
        expense = get_object_or_404(Expenses, pk=expense_id)
        expense.delete()
        messages.success(request, 'Eliminado exitosamente')
        return redirect(f'/expenses-Admin/{expense.user.id}/')