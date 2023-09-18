from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    image = models.ImageField(upload_to='assets/img', blank=True, null=True, default='assets/img/dp.png') 
    