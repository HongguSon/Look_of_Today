from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib import messages


# Create your views here.
def signup(request, *args, **kwargs):
  if request.method == 'POST':
    if request.POST['password1'] == request.POST['password2']:
      user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password1'],
        email=request.POST['email'],
      )
      auth.login(request, user)
      return redirect('user:profile_update')
    #이거 나중에 프로필 생성화면으로 가야함
    
    return render(request, 'user/signup.html')
  return render(request, 'user/signup.html')

def logout(request, *args, **kwargs):
  auth.logout(request)
  return redirect('closet:closet_main')

def log_in(request):
  if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      login(request, user)
      return redirect('main:main')
    else:
      context={'msg':'로그인 정보가 맞지 않습니다! 아이디 또는 비밀번호를 확인해주세요',}
      return render(request, 'user/login.html',context=context)
  return render(request, 'user/login.html')
      

# class PostUpdate(LoginRequiredMixin, UpdateView):
#   model = Profile
#   fields = ['profile_image', 'phone_num', 'height', 'weight', 'age', 'birth_date']

#   template_name = 'user/profile_update.html'

#   def dispatch(self, request, *args, **kwargs):
#     if request.user.is_authenticated:
#       return super(PostUpdate, self).dispatch(request, *args, **kwargs)
#     else:
#       raise PermissionDenied
def profile_update(request):
  if request.method == 'POST':
    form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
    if  form.is_valid():
      form.save()
      messages.success(request, f'Your account has been updated!')
      return redirect('closet:closet_main') # Redirect back to profile page
  else:
    form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'form': form,
  }

  return render(request, 'user/profile_update.html', context=context)