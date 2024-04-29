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
]