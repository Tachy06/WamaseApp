from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from SystemLogin.models import *
from .models import *
from django.utils.datastructures import MultiValueDictKeyError
from datetime import date, timedelta

# Create your views here.
class PageMante(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        users = User.objects.all()
        allDrivers = usersCars.objects.all()
        return render(request, 'mante.html', {'users': users, 'allDrivers': allDrivers})
    def post(self, request):
        date_maintenance = request.POST['date']
        maintenance = request.POST['maintenance']
        description = request.POST['description']
        driver = 0
        try:
            carID = request.POST['carID']
            driver = request.POST['driver']
            user = User.objects.get(id=carID)
            try:
                driver_selected = usersCars.objects.get(id=driver)
                Maintenance.objects.create(user=user, date=date_maintenance, maintenance=maintenance, description=description, driver=driver_selected)
                messages.success(request, 'Creado exitosamente')
                return redirect('/')
            except usersCars.DoesNotExist:
                Maintenance.objects.create(user=user, date=date_maintenance, maintenance=maintenance, description=description, driver=None)
                messages.success(request, 'Creado exitosamente')
                return redirect('/')
        except MultiValueDictKeyError:
            user = User.objects.get(username=request.user)
            Maintenance.objects.create(user=user, date=date_maintenance, maintenance=maintenance, description=description, driver=None)
            messages.success(request, 'Creado exitosamente')
            return redirect('/')

class MantenimientosPendientes(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        users = User.objects.all()
        mantenimientos_por_usuario = {}
        for user in users:
            mantenimientos = Maintenance.objects.filter(user=user)
            mantenimientos_por_usuario[user] = mantenimientos

        return render(request, 'reportes_mante.html', {'mantenimientos_por_usuario': mantenimientos_por_usuario})

class CompletedMante(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, mantenance_id):
        mante = get_object_or_404(Maintenance, id=mantenance_id)
        mante.completed = True
        mante.save()
        return redirect('/maintenance_report/')

class Mensajes(View):
    def get(self, request):
        tipo = request.GET.get('type')
        users = User.objects.all()
        mensajes = {}

        # Fecha actual
        hoy = date.today()

        # Calcular el primer día del mes siguiente
        if hoy.month == 12:  # Si es diciembre, el próximo mes es enero del siguiente año
            primer_dia_mes_siguiente = date(hoy.year + 1, 1, 1)
        else:  # Cualquier otro mes
            primer_dia_mes_siguiente = date(hoy.year, hoy.month + 1, 1)

        # Filtrar por technique_revision y expiration_date menores a la fecha actual
        for user in users:
            if user.is_superuser:
                continue

            try:
                moreInfo = moreInformation.objects.get(user=user)
                if moreInfo.technique_revision or moreInfo.expiration_date:
                    mensajes[user] = moreInfo
            except moreInformation.DoesNotExist:
                continue


        return render(request, 'messages.html', {
            'mensajes': mensajes,
            'tipo': tipo,
            'hoy': hoy,
            'primer_dia_mes_siguiente': primer_dia_mes_siguiente
        })