from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Movie(models.Model):
    name=models.CharField(max_length=200,unique=type)
    
    year=models.CharField(max_length=200)
    language=models.CharField(max_length=200)
    rating=models.FloatField(null=True)
   
    image=models.ImageField(upload_to="images",null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name
