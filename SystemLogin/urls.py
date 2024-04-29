from django.urls import path
from .views import *

urlpatterns = [
    path('logout/', Logout, name='Logout'),
    path('register/', RegisterView.as_view(), name='Register'),
    path('login/', LoginView.as_view(), name='Login'),
]