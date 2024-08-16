from django.db import models
from datetime import date
from django.contrib.auth.models import User
from SystemLogin.models import *

# Create your models here.
class Maintenance(models.Model):
    maintenance = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    date = models.DateField(default=date.today())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(usersCars, on_delete=models.SET_NULL, null=True)
    completed = models.BooleanField(default=False)