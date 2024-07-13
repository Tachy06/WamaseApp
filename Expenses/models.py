from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=1000, null=True)
    amount = models.FloatField(null=False)
    date = models.DateField(default=date.today())