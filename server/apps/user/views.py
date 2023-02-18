from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .forms import DateUpdateForm
from django.contrib import messages
from datetime import datetime, date
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError


# Create your views here.
def signup(request, *args, **kwargs):
  if request.method == 'POST':
    if not request.POST['username'] or not request.POST['password1'] or not request.POST['email']:
      error = '에러'
      context = {
        'error1': error,
      }
      return render(request, 'user/signup.html', context=context)
    try:
      username=request.POST['username']
    except IntegrityError:
      error = '에러'
      context = {
        'error3': error,
      }
      return render(request, 'user/signup.html', context=context)
    if request.POST['password1'] == request.POST['password2']:
      user = User.objects.create_user(
        username=username,
        password=request.POST['password1'],
        email=request.POST['email'],
      )
      auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return redirect('user:mypage')
    #이거 나중에 프로필 생성화면으로 가야함
    error = '에러'
    context = {
      'error3': error,
    }
    return render(request, 'user/signup.html', context=context)
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
  birth_date = user.profile.birth_date
  gender = user.profile.gender
  if not gender:
    gender = '성별을 등록해주세요!'
  
  if birth_date:
    age= str(datetime.today().year - int(str(birth_date).split('-')[0]) + 1) + '세'
  else:
    age='생년월일을 등록해주세요!'
  following = user.profile.following
  context = {'user':user,
             'profile_image':profile_image,
             'phone_num':phone_num,
             'height':height,
             'weight':weight,
             'age':age,
             'birth_date':birth_date,
             'following': following,
             'str_following': str(following),
             'gender':gender}
  return render(request, 'user/mypage.html', context=context)

def mypage_update(request, *args, **kwargs):
  user = request.user
  profile_image = user.profile.profile_image
  phone_num = user.profile.phone_num
  height = user.profile.height
  weight = user.profile.weight
  birth_date = user.profile.birth_date
  if birth_date:
    year = birth_date.year
    month = format(birth_date.month, '02')
    day = format(birth_date.day, '02')
    x = [year, month, day]
    x = map(str, x)
    initial_date = '-'.join(x)
  else:
    initial_date = None
  gender = user.profile.gender
  date_form = DateUpdateForm()
  context = {'user':user,
             'profile_image':profile_image,
             'phone_num':phone_num,
             'height':height,
             'weight':weight,
             'birth_date':birth_date,
             'date_form':date_form,
             'initial_date':initial_date,
             'gender': gender,}
  
  if request.method == "POST":
    if request.FILES.get("image"):
      user.profile.profile_image=request.FILES["image"]
    if request.POST.get("check1"):
      user.profile.profile_image = None
      
      
    user.profile.phone_num = request.POST["phone_num"]
    user.profile.height = request.POST["height"]
    if user.profile.height == '':
      user.profile.height = None
      
    user.profile.weight = request.POST["weight"]
    if user.profile.weight == '':
      user.profile.weight = None
      
    if request.POST["gender"] == 'nochoice':
      user.profile.gender = None
    elif request.POST["gender"] == 'male':
      user.profile.gender = '남자'
    elif request.POST["gender"] == 'female':
      user.profile.gender = '여자'
      
    if request.POST["birth_date"] == "":
      user.profile.birth_date = None
    else:
      user.profile.birth_date = request.POST["birth_date"]
      
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

@csrf_exempt
def profile_img_mod(request, pk):
  req = json.loads(request.body)
  id = req['id']
  return JsonResponse({'id' : id})