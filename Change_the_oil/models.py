from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Change_Oil(models.Model):
    car = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_change = models.DateField(null=False)

    class Meta:
        verbose_name = 'Change_Oil'
        verbose_name_plural = 'Changes_Oil'
    
    def __str__(self):
        return f'Car: {self.car} and date: {self.date_of_change}'