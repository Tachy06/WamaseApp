from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from PagePrincipal.models import *

# Create your views here.
class change_The_Oil_View(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'changeOil.html')
    def post(self, request):
        date_oil = request.POST['date']
        if date_oil is None:
            messages.error(request, 'Seleccione una fecha')
            return redirect('/change_the_oil/')
        car = User.objects.get(username=request.user)
        change = Change_Oil.objects.filter(car=car).first()
        date_object = datetime.strptime(date_oil, '%Y-%m-%d')
        if change is not None:
            change.date_of_change = date_object
            KMCar.objects.create(license_plate=car, km_today=0, total_journey=0, date=date_object)
            change.save()
            messages.success(request, 'Fecha cambiada')
            return redirect('/change_the_oil/')
        else:
            Change_Oil.objects.create(car=car, date_of_change=date_object)
            KMCar.objects.create(license_plate=car, km_today=0, total_journey=0, date=date_object)
            messages.success(request, 'Fecha cambiada')
            return redirect('/change_the_oil/')