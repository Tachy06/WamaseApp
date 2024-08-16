from django.urls import path
from .views import *

urlpatterns = [
    path('maintenance/', PageMante.as_view(), name="Mantenimiento"),
    path('maintenance_report/', MantenimientosPendientes.as_view(), name='Reportes_Pendientes'),
    path('maintenance_completed/<int:mantenance_id>/', CompletedMante.as_view(), name='Mantenimiento_Completado'),
    path('messages/', Mensajes.as_view(), name='Mensajes')
]