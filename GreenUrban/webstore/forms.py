from django import forms
from .models import RegisteredUser,Scrap

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = RegisteredUser
        fields = ['img']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = RegisteredUser
        fields = ['name', 'email', 'pincode', 'number', 'address', 'img']

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    username = forms.CharField(max_length=255)
    pincode = forms.IntegerField()
    number = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        return cleaned_data

class ScrapForm(forms.ModelForm):
    class Meta:
        model = Scrap
        fields = ['category', 'description', 'img1', 'img2', 'img3']
