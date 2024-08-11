from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class OTP(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
     
class RegisteredUser(AbstractUser):
    img = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    pincode = models.PositiveIntegerField(blank=True, null=True)
    number = models.CharField(max_length=10, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.username
    

class scrap():
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField()
    description = models.CharField(max_length=225)
    img1 =models.ImageField(null=False)
    img2 =models.ImageField(null=False)
    img3 =models.ImageField(null=False)
    location = models.CharField(null=False)

    def __str__(self):
        return self.user