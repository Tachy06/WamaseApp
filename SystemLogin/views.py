from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *

# Create your views here. 
def Logout(request):
    logout(request)
    return redirect('/login/')

class RegisterView(View):
    def get(self, request):
        usersCar = usersCars.objects.all()
        return render(request, 'register.html', {'usersCars': usersCar})

    def post(self, request):
        car = request.POST.get('brand')
        year = request.POST.get('year')
        license_plate = request.POST.get('license_plate')
        correo = request.POST.get('email')
        oil = request.POST.get('oil')
        vin = request.POST.get('vin')
        property = request.POST.get('property')
        drivers = request.POST.getlist('drivers')
        
        if car == '':
            messages.error(request, 'No deje el nombre en blanco')
            return redirect('/register/')
        elif car.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register/')
        
        if year == '':
            messages.error(request, 'No deje el apellido en blanco')
            return redirect('/register/')
        elif year.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register/')
        
        if license_plate == '':
            messages.error(request, 'No deje el nombre en blanco')
            return redirect('/register/')
        elif license_plate.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register/')
        
        if oil == '':
            messages.error(request, 'Seleccione un tipo de aceite')
            return redirect('/register/')
        elif oil.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register/')
        
        elif User.objects.filter(username=license_plate):
            messages.error(request, 'Usuario existente')
            return redirect('/register/')
        
        if correo.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register/')
        elif correo == '':
            User.objects.create_user(first_name=car, username=license_plate, email='Nothing', password=license_plate, last_name=oil)
            usuario = User.objects.get(username=license_plate)
            drivers_Cars = usersCars.objects.filter(pk__in=drivers)
            moreInfo = moreInformation.objects.create(user=usuario, year=year, vin=vin, property=property)
            moreInfo.usersCar.set(drivers_Cars)
            messages.success(request, 'Todo correcto')
            return redirect('/login/')
        
        User.objects.create_user(first_name=car, username=license_plate, email=correo, password=license_plate, last_name=oil)
        usuario = User.objects.get(username=license_plate)
        drivers_Cars = usersCars.objects.filter(pk__in=drivers)
        moreInfo = moreInformation.objects.create(user=usuario, year=year, vin=vin, property=property)
        moreInfo.usersCar.set(drivers_Cars)
        messages.success(request, 'Todo correcto')
        return redirect('/login/')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        license_plate = request.POST['license_plate']
        session = authenticate(username=license_plate, password=license_plate)
        if session is None:
            messages.error(request, 'Credenciales incorrectos')
            return redirect('/login/')
        login(request, session)
        return redirect('/')