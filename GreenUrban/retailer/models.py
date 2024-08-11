from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

User = get_user_model()
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Retailer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    rating = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    approval = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    def update_rating(self):
        reviews = self.productreview_set.all()
        if reviews.exists():
            self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.save()
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='webstore/static/images/products/%Y/%m/%d/')

    def __str__(self):
        return f"Image for {self.product.name}"
    
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} likes {self.product.name}"
    

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (1, 'Order Placed'),
        (2, 'Order Confirmed'),
        (3, 'Dispatched'),
        (4, 'Out for Delivery'),
        (5, 'Delivered'),
        (0, 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    order_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    delivery_boy_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"