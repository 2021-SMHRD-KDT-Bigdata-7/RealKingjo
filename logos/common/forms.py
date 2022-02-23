from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(UserCreationForm):
    username = forms.CharField(label="아이디")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", 'age', 'location','gender','phone','last_name')
