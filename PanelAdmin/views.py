from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from SystemLogin.models import *
from Change_the_oil.models import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from Expenses.models import *

# Create your views here.
def viewAdmin(request):
    if request.method == 'POST':
        lookFor = request.POST['lookFor']
        try:
            car = User.objects.get(username=lookFor)
            return redirect(f'/look_for/{car}')
        except User.DoesNotExist:
            messages.error(request, 'No existe esta placa en la base de datos')
            return redirect('/admin/')
    if not request.user.is_superuser:
        return redirect('/')
    elif not request.user.is_authenticated:
        return redirect('/login/')
    users_with_info = []
    users = User.objects.all()
    count_cars = users.count()
    for user in users:
        try:
            user_info = {
                'user': user,
                'more_info': moreInformation.objects.filter(user=user).last(),
                'oil': Change_Oil.objects.filter(car=user).last()
            }
        except moreInformation.DoesNotExist:
            user_info = {
                'user': user,
            }
        users_with_info.append(user_info)
    return render(request, 'panelAdmin.html', {'users_with_info': users_with_info, 'count_cars': count_cars})

class eliminarUsuario(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return redirect('/admin/')
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return redirect('/admin/')
    
class registrarUsuarioAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        usersCar = usersCars.objects.all()
        return render(request, 'register_admin.html', {'usersCars': usersCar})
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
            messages.error(request, 'No deje la marca en blanco')
            return redirect('/register_admin/')
        elif car.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        if year == '':
            messages.error(request, 'No deje el año en blanco')
            return redirect('/register_admin/')
        elif year.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        if license_plate == '':
            messages.error(request, 'No deje la placa en blanco')
            return redirect('/register_admin/')
        elif license_plate.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        if oil == '':
            messages.error(request, 'Seleccione un tipo de aceite')
            return redirect('/register_admin/')
        elif oil.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        elif User.objects.filter(username=license_plate):
            messages.error(request, 'Usuario existente')
            return redirect('/register_admin/')
        
        if correo.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        elif correo == '':
            User.objects.create_user(first_name=car, username=license_plate, email='Nothing', password=license_plate, last_name=oil)
            usuario = User.objects.get(username=license_plate)
            drivers_Cars = usersCars.objects.filter(pk__in=drivers)
            moreInfo = moreInformation.objects.create(user=usuario, year=year, vin=vin, property=property)
            moreInfo.usersCar.set(drivers_Cars)
            return redirect('/admin/')
        
        User.objects.create_user(first_name=car, username=license_plate, email=correo, password=license_plate, last_name=oil)
        usuario = User.objects.get(username=license_plate)
        drivers_Cars = usersCars.objects.filter(pk__in=drivers)
        moreInfo = moreInformation.objects.create(user=usuario, year=year, vin=vin, property=property)
        moreInfo.usersCar.set(drivers_Cars)
        return redirect('/admin/')
    
class editUser(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        # Obtener información adicional del usuario
        user_info = {
            'user': user,
            'more_info': moreInformation.objects.get(user=user),
            'oil': Change_Oil.objects.filter(car=user).last()
        }
        return render(request, 'edit_user_admin.html', {'user_info': user_info})
    def post(self, request, user_id):
        car = request.POST.get('brand')
        license_plate = request.POST.get('license_plate')
        correo = request.POST.get('email')
        oil = request.POST.get('oil')
        year = request.POST.get('year')
        car_id = User.objects.get(id=user_id)
        more = moreInformation.objects.get(user_id=car_id)
        if car == '':
            messages.error(request, 'No deje la marca en blanco')
            return redirect(f'/edit_user/{user_id}')
        elif car.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect(f'/edit_user/{user_id}')
        
        if license_plate == '':
            messages.error(request, 'No deje la placa en blanco')
            return redirect(f'/edit_user/{user_id}')
        elif license_plate.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect(f'/edit_user/{user_id}')
        
        if oil == '':
            messages.error(request, 'Seleccione un tipo de aceite')
            return redirect(f'/edit_user/{user_id}')
        elif oil.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect(f'/edit_user/{user_id}')
        
        if year == '':
            messages.error(request, 'No deje el año en blanco')
            return redirect(f'/edit_user/{user_id}')
        elif year.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect(f'/edit_user/{user_id}')
        
        if correo.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect(f'/edit_user/{user_id}')
        elif correo == '':
            car_id.first_name = car
            car_id.last_name = oil
            car_id.username = license_plate
            car_id.email = 'Nothing'
            car_id.save()
            more.year = year
            more.save()
            messages.success(request, 'Cambio exitoso')
            return redirect('/admin/')
        car_id.first_name = car
        car_id.last_name = oil
        car_id.username = license_plate
        car_id.email = correo
        car_id.save()
        more.year = year
        more.save()
        messages.success(request, 'Cambio exitoso')
        return redirect('/admin/')

class look_for(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        try:
            try:
                car = User.objects.get(username=user_id)
                more = moreInformation.objects.get(user=car)
                oil = Change_Oil.objects.filter(car=car).last()
                return render(request, 'look_for.html', {'car': car, 'more_info': more, 'oil': oil})
            except moreInformation.DoesNotExist:
                car = User.objects.get(username=user_id)
                return render(request, 'look_for.html', {'car': car})
        except User.DoesNotExist:
            messages.error(request, 'No existe este usuario en la base de datos')
            return redirect('/admin/')
        
class createSuperUser(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'createSuperUser.html')
    def post(self, request):
        name = request.POST['name']
        last_name = request.POST['last_name']
        user = request.POST['user']
        email = request.POST['email']

        if name == '':
            messages.error(request, 'No dejes el nombre en blanco')
            return redirect('/create_admin/')
        elif name.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/create_admin/')
        if last_name == '':
            messages.error(request, 'No dejes el apellido en blanco')
            return redirect('/create_admin/')
        elif last_name.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/create_admin/')
        if user == '':
            messages.error(request, 'No dejes el usuario en blanco')
            return redirect('/create_admin/')
        elif user.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/create_admin/')
        if email == '':
            messages.error(request, 'No dejes el email en blanco')
            return redirect('/create_admin/')
        elif email.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/create_admin/')
        try:
            user_search = User.objects.get(username=user)
            if user_search:
                messages.error(request, 'Usuario existente')
                return redirect('/create_admin/')
        except User.DoesNotExist:
            User.objects.create_superuser(first_name=name, last_name=last_name, username=user, password=user, email=email)
            messages.success(request, 'Admin creado')
            return redirect('/admin/')
        
class createChofer(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'drivers.html')
    def post(self, request):
        name = request.POST['chofer']
        if name == '':
            messages.error(request, 'No dejes el nombre en blanco')
            return redirect('/create_driver/')
        elif name.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/create_driver/')
        driver = usersCars.objects.create(user=name)
        messages.success(request, 'Creado exitosamente')
        return redirect('/admin/')
    
class expensesAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        expenses = Expenses.objects.filter(user=user)
        total = 0
        for expense in expenses:
            total += expense.amount
        return render(request, 'view_expenses_admin.html', {'user': user, 'expenses': expenses, 'total': total})