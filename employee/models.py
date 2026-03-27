from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    adhar_number = models.CharField(max_length=20, unique=True)
    worked_hours = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=(('Male','Male'),('Female','Female'),('Other','Other')))
    
    def __str__(self):
        return self.name
from django.db import models

class Signup(models.Model):
    user = models.CharField(max_length=50, unique=True)
    pasw = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user