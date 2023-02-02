from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def signup(request):
  if request.method == 'POST':
    if request.POST['password1'] == request.POST['password2']:
      user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password1'],
        email=request.POST['email'],
      )
      auth.login(request, user)
      return redirect('closet:closet_main')
    #이거 나중에 프로필 생성화면으로 가야함
    
    return render(request, 'user/signup.html')
  return render(request, 'user/signup.html')

def logout(request):
  auth.logout(request)
  return redirect('closet:closet_main')