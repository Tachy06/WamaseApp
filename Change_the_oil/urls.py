from django.urls import path
from .views import *

urlpatterns = [
    path('change_the_oil/', change_The_Oil_View.as_view(), name='Change_The_Oil')
]