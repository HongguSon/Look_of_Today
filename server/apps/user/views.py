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
      auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return redirect('user:profile_update')
    #이거 나중에 프로필 생성화면으로 가야함
    
    return render(request, 'user/signup.html')
  return render(request, 'user/signup.html')

def logout(request, *args, **kwargs):
  auth.logout(request)
  return redirect('main:main')

def log_in(request, *args, **kwargs):
  if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return redirect('main:main')
    else:
      context={'msg':'로그인 정보가 맞지 않습니다! 아이디 또는 비밀번호를 확인해주세요',}
      return render(request, 'user/login.html',context=context)
  return render(request, 'user/login.html')

def mypage(request, *args, **kwargs):
  user = request.user
  profile_image = user.profile.profile_image
  phone_num = user.profile.phone_num
  height = user.profile.height
  weight = user.profile.weight
  age = user.profile.age
  birth_date = user.profile.birth_date
  following = user.profile.following
  context = {'user':user,
             'profile_image':profile_image,
             'phone_num':phone_num,
             'height':height,
             'weight':weight,
             'age':age,
             'birth_date':birth_date,
             'following': following,
             'str_following': str(following)}
  return render(request, 'user/mypage.html', context=context)

def mypage_update(request, *args, **kwargs):
  user = request.user
  profile_image = user.profile.profile_image
  phone_num = user.profile.phone_num
  height = user.profile.height
  weight = user.profile.weight
  age = user.profile.age
  birth_date = user.profile.birth_date
  following = user.profile.following
  context = {'user':user,
             'profile_image':profile_image,
             'phone_num':phone_num,
             'height':height,
             'weight':weight,
             'age':age,
             'birth_date':birth_date,
             'following': following,
             'str_following': str(following)}
  
  if request.method == "POST":
    if request.FILES.get("image"):
      user.profile.profile_image=request.FILES["image"]
    if request.POST.get("check1"):
      user.profile_user.profile_image = None
    user.profile.phone_num = request.POST["phone_num"]
    user.profile.height = request.POST["height"]
    user.profile.weight = request.POST["weight"]
    user.profile.age = request.POST["age"]
    
    '1999년 8월 30일'
    x = request.POST["birth_date"]
    year = x.split('년')[0]
    month = x.split('년')[1].split('월')[0].strip()
    date = x.split('년')[1].split('월')[1].split('일')[0].strip()
    user.profile.birth_date = year+'-'+month+'-'+date
    #following도 처리해줘야함
    user.profile.save()
    return redirect("user:mypage")
  
  return render(request, "user/mypage_update.html",context=context)

# class PostUpdate(LoginRequiredMixin, UpdateView):
#   model = Profile
#   fields = ['profile_image', 'phone_num', 'height', 'weight', 'age', 'birth_date']

#   template_name = 'user/profile_update.html'

#   def dispatch(self, request, *args, **kwargs):
#     if request.user.is_authenticated:
#       return super(PostUpdate, self).dispatch(request, *args, **kwargs)
#     else:
#       raise PermissionDenied

def profile_update(request, *args, **kwargs):
  if request.method == 'POST':
    form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
    if  form.is_valid():
      form.save()
      messages.success(request, f'Your account has been updated!!!!!')
      return redirect('main:main') # Redirect back to profile page
  else:
    form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'form': form,
  }
  return render(request, 'user/profile_update.html', context=context)