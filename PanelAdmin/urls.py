from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', viewAdmin, name='Admin'),
    path('eliminar_usuario/<int:user_id>/', eliminarUsuario.as_view(), name='Eliminar_usuario'),
    path('register_admin/', registrarUsuarioAdmin.as_view(), name='Registrar_usuario'),
    path('edit_user/<int:user_id>/', editUser.as_view(), name='Edit_user'),
    path('look_for/<str:user_id>/', look_for.as_view(), name='Look_for'),
    path('create_admin/', createSuperUser.as_view(), name='Create_admin'),
    path('createChofer/', createChofer.as_view(), name='createChofer'),
    path('deleteChofer/', deleteChofer, name='DeleteChofer'),
    path('expenses-Admin/<int:user_id>/', expensesAdmin.as_view(), name='Expenses_Admin'),
    path('expenses-admin/<int:user_id>/pdf/', generate_pdf, name='Expenses_Admin_PDF'),
    path('delete_driver/', deleteDriver.as_view(), name='Delete_driver'),
    path('change_prices/', changePrices.as_view(), name='Change_Prices'),
    path('generate_all_expenses/', GenerateAllExpenses.as_view(), name='Generate_All_Expenses'),
    path('generate_all_expenses/pdf/', generate_all_pdf, name='Generate_All_Expenses_PDF'),
]