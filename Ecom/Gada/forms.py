from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User,Shipping
from django import forms

 
class UserForm(ModelForm):

    password = forms.PasswordInput()
    avatar = forms.ImageField(required=False)
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['name', 'email', 'avatar', 'username','password']
        

class LoginForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']


class ShippingForm(ModelForm):

    class Meta:
        model = Shipping
        fields ='__all__'
        exclude = ['user','order']