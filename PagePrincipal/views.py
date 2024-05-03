from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import *
from Change_the_oil.models import *
from SystemLogin.models import *

# Create your views here.
class Home(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        car = User.objects.get(username=request.user)
        date = Change_Oil.objects.filter(car=car).last()
        formatted_date = date.date_of_change.strftime('%d/%m/%Y') if date else None
        km_journey = KMCar.objects.filter(license_plate=car).last()
        if car.last_name == '':
            return render(request, 'index.html', {'car': car.last_name})
        try:
            if int(car.last_name) == 1 and km_journey:
                if km_journey.total_journey >= 10000.0:
                    messages.warning(request, '10000 Km recorridos, es hora de cambiar el aceite')
            elif int(car.last_name) == 2:
                if km_journey.total_journey >= 5000.0 and km_journey:
                    messages.warning(request, '5000 Km recorridos, es hora de cambiar el aceite')
            return render(request, 'index.html', {'km_journey': km_journey.total_journey, 'date': formatted_date})
        except:
            return render(request, 'index.html', {'km_journey': km_journey.total_journey if km_journey else None, 'date': formatted_date, 'car': car.last_name})

class KMCarView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        user = User.objects.get(username=request.user)
        moreInfo = moreInformation.objects.filter(user=user)
        return render(request, 'kmcar.html', {'moreInfo': moreInfo})
    
    def post(self, request):
        km = request.POST['km']
        date = request.POST['date']
        drivers = request.POST['drivers']

        if km == '' or km.isspace():
            messages.error(request, 'No dejes en blanco el kilometraje')
            return redirect('/km/')

        car = User.objects.get(username=request.user)
        km_record = KMCar.objects.filter(license_plate=car).last()
        driver = usersCars.objects.get(id=drivers)
        if km_record is not None:
            today = KMCar.objects.filter(license_plate=car, date=date)
            if not km_record.km_today == 0.00:
                if today.exists():
                    messages.error(request, 'Ya ingresaste los kilometros de ese día')
                    return redirect('/km/')
                else:
                    total = km_record.total_journey + float(km)
                    KMCar.objects.create(license_plate=car, user_use=driver.user, km_today=float(km), total_journey=total, date=date)
                    messages.success(request, 'Kilometraje agregado')
                    return redirect('/km/')
            else:
                total = km_record.total_journey + float(km)
                KMCar.objects.create(license_plate=car, user_use=driver.user, km_today=float(km), total_journey=total, date=date)
                messages.success(request, 'Kilometraje agregado')
                return redirect('/km/')
        else:
            date_exist = Change_Oil.objects.filter(car=car)
            if date_exist.exists():
                KMCar.objects.create(license_plate=car, user_user=driver.user, km_today=float(km), total_journey=float(km), date=date)
                messages.success(request, 'Kilometraje agregado')
                return redirect('/km/')
            else:
                messages.error(request, 'Primero debes agregar una fecha del cambio de aceite')
                return redirect('/km/')
        
class profile(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        car = User.objects.get(username=request.user)
        moreinfo = moreInformation.objects.filter(user=car).last()
        return render(request, 'profile.html', {'car': car, 'moreinfo': moreinfo})