from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import UserChangeForm






class UserForm(UserCreationForm):
    username = forms.CharField(label="아이디")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", 'age', 'location','gender','phone','last_name')
        
        
        
class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ('last_name', 'age', 'phone','gender','location')