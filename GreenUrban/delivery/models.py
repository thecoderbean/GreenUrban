from django.conf import settings
from django.db import models

class DeliveryBoy(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.user.username
