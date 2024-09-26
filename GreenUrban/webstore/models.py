from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


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
    address = models.TextField()# New field for storing coins, default set to 500

    def __str__(self):
        return self.username


class Scrap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    category = models.CharField(max_length=100)  
    description = models.CharField(max_length=225)
    img1 = models.ImageField(upload_to='scrap_images/', null=False)
    img2 = models.ImageField(upload_to='scrap_images/', null=False)
    img3 = models.ImageField(upload_to='scrap_images/', null=False)

    def __str__(self):
        return f"Scrap by {self.user.username}"
