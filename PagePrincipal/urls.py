from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('km/', KMCarView.as_view(), name='KMCarView'),
    path('profile/', profile.as_view(), name='Profile'),
]