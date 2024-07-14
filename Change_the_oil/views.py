from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from PagePrincipal.models import *
from Expenses.models import *

# Create your views here.
class change_The_Oil_View(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        cars = User.objects.all()
        if not request.user.is_superuser:
            return redirect('/')
        return render(request, 'changeOil.html', {'cars': cars})
    def post(self, request):
        car = request.POST['car']
        date_oil = request.POST['date']
        air_filter = request.POST['air-filter']
        oil_filter = request.POST['oil-filter']
        fuel_filter = request.POST['fuel-filter']
        water_trap = request.POST['water-trap']
        search = PriceOfChangeOil.objects.all().last()
        if date_oil is None:
            messages.error(request, 'Seleccione una fecha')
            return redirect('/change_the_oil/')
        
        if air_filter == "Si":
            air = search.air_filter
        else:
            air = 0

        if oil_filter == "Si":
            oil = search.oil_filter
        else:
            oil = 0

        if fuel_filter == "Si":
            fuel = search.fuel_filter
        else:
            fuel = 0
        if water_trap == "Si":
            water = search.water_trap
        else:
            water = 0

        car_object = User.objects.get(id=car)
        if car_object.last_name == '1':
            suma = air + oil + fuel + water + search.oil_havoline
            Expenses.objects.create(user=car_object, title='Cambio de aceite', amount=suma)
        else:
            suma = air + oil + fuel + water +search.oil_chevron
            Expenses.objects.create(user=car_object, title='Cambio de aceite', amount=suma)

        change = Change_Oil.objects.filter(car=car_object).first()
        date_object = datetime.strptime(date_oil, '%Y-%m-%d')
        
        if change is not None:
            change.date_of_change = date_object
            KMCar.objects.create(license_plate=car_object, km_today=0, total_journey=0, date=date_object)
            change.save()
            messages.success(request, 'Fecha cambiada')
            return redirect('/change_the_oil/')
        else:
            Change_Oil.objects.create(car=car_object, date_of_change=date_object)
            KMCar.objects.create(license_plate=car_object, km_today=0, total_journey=0, date=date_object)
            messages.success(request, 'Fecha cambiada')
            return redirect('/change_the_oil/')