from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from SystemLogin.models import *
from Change_the_oil.models import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from Expenses.models import *
from PagePrincipal.models import *
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

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
        url = '/'
    return render(request, 'panelAdmin.html', {'users_with_info': users_with_info, 'count_cars': count_cars, 'url': url})

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
        url = '/admin/'
        return render(request, 'register_admin.html', {'usersCars': usersCar, 'url': url})
    def post(self, request):
        car = request.POST.get('brand')
        year = request.POST.get('year')
        license_plate = request.POST.get('license_plate')
        correo = request.POST.get('email')
        oil = request.POST.get('oil')
        vin = request.POST.get('vin')
        property = request.POST.get('property')
        code = request.POST.get('code')
        code_filter_oil = request.POST.get('code_filter_oil')
        code_filter_air = request.POST.get('code_filter_air')
        
        if car == '':
            messages.error(request, 'No deje el nombre en blanco')
            return redirect('/register_admin/')
        elif car.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        if year == '':
            messages.error(request, 'No deje el apellido en blanco')
            return redirect('/register_admin/')
        elif year.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        if license_plate == '':
            messages.error(request, 'No deje el nombre en blanco')
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
        
        if code_filter_oil == '':
            messages.error(request, 'No deje el código en blanco')
            return redirect('/register_admin/')
        elif code_filter_oil.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        if code_filter_air == '':
            messages.error(request, 'No deje el código en blanco')
            return redirect('/register_admin/')
        elif code_filter_air.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        if code == '':
            messages.error(request, 'No deje el código en blanco')
            return redirect('/register_admin/')
        elif code.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register_admin/')
        
        elif correo == '':
            if code == '1982':
                User.objects.create_user(first_name=car, username=license_plate, email='Nothing', password=license_plate, last_name=oil)
                usuario = User.objects.get(username=license_plate)
                moreInfo = moreInformation.objects.create(user=usuario, year=year, vin=vin, property=property, code_filter_oil=code_filter_oil, code_filter_air=code_filter_air)
                messages.success(request, 'Todo correcto')
                return redirect('/admin/')
            else:
                messages.error(request, 'Código de seguridad incorrecto')
                return redirect('/register_admin/')
        if code == '1982':
            User.objects.create_user(first_name=car, username=license_plate, email=correo, password=license_plate, last_name=oil)
            usuario = User.objects.get(username=license_plate)
            moreInfo = moreInformation.objects.create(user=usuario, year=year, vin=vin, property=property, code_filter_oil=code_filter_oil, code_filter_air=code_filter_air)
            messages.success(request, 'Todo correcto')
            return redirect('/admin/')
        else:
            messages.error(request, 'Código de seguridad incorrecto')
            return redirect('/register_admin/')
    
class editUser(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        # Obtener información adicional del usuario
        info = moreInformation.objects.get(user=user)
        user_info = {
            'user': user,
            'more_info': info,
            'oil': Change_Oil.objects.filter(car=user).last(),
        }
        url = '/admin/'
        return render(request, 'edit_user_admin.html', {'user_info': user_info, 'url': url})
    def post(self, request, user_id):
        car = request.POST.get('brand')
        year = request.POST.get('year')
        license_plate = request.POST.get('license_plate')
        correo = request.POST.get('email')
        oil = request.POST.get('oil')
        vin = request.POST.get('vin')
        property = request.POST.get('property')
        code = request.POST.get('code')
        code_filter_oil = request.POST.get('code_filter_oil')
        code_filter_air = request.POST.get('code_filter_air')

        car_id = User.objects.get(id=user_id)
        more = moreInformation.objects.get(user_id=car_id)

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
        
        if correo.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register/')
        
        if code_filter_oil == '':
            messages.error(request, 'No deje el código en blanco')
            return redirect('/register/')
        elif code_filter_oil.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register/')
        
        if code_filter_air == '':
            messages.error(request, 'No deje el código en blanco')
            return redirect('/register/')
        elif code_filter_air.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/register/')
        
        elif correo == '':
            car_id.first_name = car
            car_id.last_name = oil
            car_id.username = license_plate
            car_id.email = 'Nothing'
            car_id.save()
            more.year = year
            more.vin = vin
            more.property = property
            more.code_filter_oil = code_filter_oil
            more.code_filter_air = code_filter_air
            more.save()
            messages.success(request, 'Cambio exitoso')
            return redirect('/admin/')
        car_id.first_name = car
        car_id.last_name = oil
        car_id.username = license_plate
        car_id.email = correo
        car_id.save()
        more.year = year
        more.vin = vin
        more.property = property
        more.code_filter_oil = code_filter_oil
        more.code_filter_air = code_filter_air
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
                url = '/admin/'
                return render(request, 'look_for.html', {'car': car, 'url': url})
        except User.DoesNotExist:
            messages.error(request, 'No existe este usuario en la base de datos')
            return redirect('/admin/')
        
class createSuperUser(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        url = '/admin/'
        return render(request, 'createSuperUser.html', {'url': url})
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
        url = '/admin/'
        usersCar = usersCars.objects.all()
        return render(request, 'drivers.html', {'url': url, 'drivers': usersCar})
    def post(self, request):
        name = request.POST['chofer']
        if name == '':
            messages.error(request, 'No dejes el nombre en blanco')
            return redirect('/createChofer/')
        elif name.isspace():
            messages.error(request, 'No digite solo espacios')
            return redirect('/createChofer/')
        try:
            driver = usersCars.objects.get(user=name)
            if driver:
                messages.error(request, 'Conductor existente')
                return redirect('/createChofer/')
        except:
            driver = usersCars.objects.create(user=name)
            messages.success(request, 'Creado exitosamente')
            return redirect('/createChofer/')

@require_POST
def deleteChofer(request):
    chofer_id = request.POST.get('chofer_delete')
    if chofer_id:
        chofer = get_object_or_404(usersCars, pk=chofer_id)
        chofer.delete()
        messages.success(request, 'Eliminado exitosamente')
        return redirect('/createChofer/')
    else:
        messages.error(request, 'No se pudo eliminar')
        return redirect('/createChofer/')      
    
class expensesAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        expenses = Expenses.objects.filter(user=user).order_by('-date')

        selected_month = request.GET.get('month')
        is_filtered = False
        if selected_month:
            expenses = expenses.filter(date__month=selected_month)
            is_filtered = True
        total = 0
        for expense in expenses:
            total += expense.amount
        url = '/admin/'
        return render(request, 'view_expenses_admin.html', {'user': user, 'expenses': expenses, 'total': total, 'url': url, 'is_filtered': is_filtered})

def generate_pdf(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    expenses = Expenses.objects.filter(user=user).order_by('-date')
        
    selected_month = request.GET.get('month')
    if selected_month:
        try:
            month_number = int(selected_month)
            if 1 <= month_number <= 12:
                expenses = expenses.filter(date__month=month_number)
        except ValueError:
            pass
        
    total = sum(expense.amount for expense in expenses)
        
    html_string = render_to_string('generateExpensesPDF.html', {
        'user': user,
        'expenses': expenses,
        'total': total
    })
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Gastos del camión {user.username}.pdf"'
    html.write_pdf(response)
        
    return response
        
class deleteDriver(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        usersCar = usersCars.objects.all()
        url = '/admin/'
        return render(request, 'delete_driver.html', {'drivers': usersCar, 'url': url})
    def post(self, request):
        drivers = request.POST.getlist('drivers')
        for driver_id in drivers:
            driver = get_object_or_404(usersCars, pk=driver_id)
            driver.delete()
        messages.success(request, 'Eliminado exitosamente')
        return redirect('/admin/')
    
class changePrices(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        url = '/admin/'
        prices = PriceOfChangeOil.objects.all()
        return render(request, 'changes_prices.html', {'url': url, 'prices': prices})
    def post(self, request):
        search = PriceOfChangeOil.objects.all().last()
        oil_havoline = request.POST['oil_havoline']
        oil_chevron = request.POST['oil_chevron']
        air_filter = request.POST['air_filter']
        oil_filter = request.POST['oil_filter']
        fuel_filter = request.POST['fuel_filter']
        water_trap = request.POST['water-trap']

        if oil_havoline == '':
            oil_havoline = search.oil_havoline
        if oil_chevron == '':
            oil_chevron = search.oil_chevron
        if air_filter == '':
            air_filter = search.air_filter
        if oil_filter == '':
            oil_filter = search.oil_filter
        if fuel_filter == '':
            fuel_filter = search.fuel_filter
        if water_trap == '':
            water_trap = search.water_trap
        
        try:
            prices = PriceOfChangeOil.objects.all()
            for price in prices:
                price.oil_havoline = oil_havoline
                price.oil_chevron = oil_chevron
                price.air_filter = air_filter
                price.oil_filter = oil_filter
                price.fuel_filter = fuel_filter
                price.water_trap = water_trap
                price.save()
        except PriceOfChangeOil.DoesNotExist:    
            PriceOfChangeOil.objects.create(oil_chevron=oil_chevron, oil_havoline=oil_havoline, air_filter=air_filter, oil_filter=oil_filter, fuel_filter=fuel_filter, water_trap=water_trap)
        messages.success(request, 'Cambiado exitosamente')
        return redirect('/admin/')
    
class GenerateAllExpenses(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        url = '/admin/'
        users = User.objects.all()
        month = request.GET.get('month')
        user_with_info = []
        is_filtered = False
        total_improve_to_zero = False
        total = 0
        for user in users:
            expenses = Expenses.objects.filter(user=user).order_by('-date')
            if month:
                month = int(month)
                if 1 <= month <= 12:
                    expenses = expenses.filter(date__month=month)
                    total = sum(expense.amount for expense in expenses)
                    is_filtered = True
                if total > 0:
                    total_improve_to_zero = True
                user_info = {
                    'user': user,
                    'total': total
                }
            else:
                user_info = {
                }
            user_with_info.append(user_info)
        return render(request, 'generate_all_expenses.html', {'url': url, 'user_with_info': user_with_info, 'is_filtered': is_filtered, 'total_improve_to_zero': total_improve_to_zero})
    
def generate_all_pdf(request):
    users = User.objects.all()
    selected_month = request.GET.get('month')
    
    user_data = []
    total_amount = 0

    for user in users:
        expenses = Expenses.objects.filter(user=user).order_by('-date')
        
        if selected_month:
            try:
                month_number = int(selected_month)
                if 1 <= month_number <= 12:
                    expenses = expenses.filter(date__month=month_number)
            except ValueError:
                pass
        
        user_total = sum(expense.amount for expense in expenses)
        total_amount += user_total
        user_data.append((user, expenses, user_total))  # Añade el total del usuario a los datos
    
    html_string = render_to_string('generate_all_expensesPDF.html', {
        'user_data': user_data,
        'total_amount': total_amount,
        'month': selected_month
    })
    
    html = HTML(string=html_string)
    pdf_bytes = html.write_pdf()
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Gastos_totales_del_mes_{selected_month}.pdf"'
    
    return response