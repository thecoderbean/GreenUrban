from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'available']

ProductImageFormSet = inlineformset_factory(Product, ProductImage, fields=('image',), extra=1, can_delete=True)    
        
class RetailerLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
