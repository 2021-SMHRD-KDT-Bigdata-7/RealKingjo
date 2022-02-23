from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm
from .forms import CustomUserChangeForm

# Create your views here.

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)# 사용자 인증
            login(request, user)  # 로그인
            return redirect('MainBoard:main')
    else:
        form = UserForm()
    return render(request, 'common/join_from.html', {'form': form})

