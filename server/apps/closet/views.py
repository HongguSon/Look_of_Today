from django.shortcuts import render, redirect, get_object_or_404
from server.apps.main.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.views.decorators.http import require_POST
from itertools import chain
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
# REVIEW : mysql 파일 삭제 요망
def closet_main(request, *args, **kwargs):
  clothes_list = Clothes.objects.filter(author=request.user)
  context = {
    'clothes_list': clothes_list,
  }
  return render(request,'closet/closet_main.html', context=context)

def closet_all(request, *args, **kwargs):
  post_list = Post.objects.filter(author=request.user) 
  context={
      'post_list':post_list,
  }   
  return render(request,'closet/closet_main.html',context=context)

# def clothes_list(request, Clothes, *args, **kwargs):
#   clothes_mapping = {
#     'top': Top,
#     'bottom': Bottom,
#     'outer': Outer,
#     'shoes': Shoes,
#     'acc': Acc,
#   }
#   clothes_list = clothes_mapping.get(Clothes).objects.filter(author=request.user)
#   context={
#     'clothes_list': clothes_list,
#     }   
#   return render(request,'closet/closet_main.html',context=context)
  
def outer_list(request, *args, **kwargs):
  clothes_list = Outer.objects.filter(author=request.user)
  context={
    'clothes_list': clothes_list,
  }   
  return render(request,'closet/closet_main.html',context=context)

def top_list(request, *args, **kwargs):
  clothes_list = Top.objects.filter(author=request.user)
  context={
    'clothes_list': clothes_list,
  }   
  return render(request,'closet/closet_main.html',context=context)

def bottom_list(request, *args, **kwargs):
  clothes_list = Bottom.objects.filter(author=request.user)
  context={
    'clothes_list': clothes_list,
  }   
  return render(request,'closet/closet_main.html',context=context)

def shoes_list(request, *args, **kwargs):
  clothes_list = Shoes.objects.filter(author=request.user)
  context={
    'clothes_list': clothes_list,
  }   
  return render(request,'closet/closet_main.html',context=context)

def acc_list(request, *args, **kwargs):
  clothes_list = Acc.objects.filter(author=request.user)
  context={
    'clothes_list': clothes_list,
  }   
  return render(request,'closet/closet_main.html',context=context)

def our_closet(request, *args, **kwargs):  
  # sort = request.GET.get('sort','')
  
  # if sort == 'new':
  #   post_list = Post.objects.filter(open=True).order_by("-pk")
  # elif sort == 'old':
  #   post_list = Post.objects.filter(open=True).order_by("pk")
  # elif sort == 'like':
  #   post_list = Post.objects.filter(open=True).order_by("")
  # else:
  #   post_list = Post.objects.filter(open=True).order_by("-pk")
    
  # page = request.GET.get('page', 1)
  # paginator = Paginator(post_li, 4)
  
  # try:
  #   posts = paginator.page(page)
  # except PageNotAnInteger:
  #   posts = paginator.page(1)
  # except EmptyPage:
  #   posts = paginator.page(paginator.num_pages)
  post_list = Post.objects.filter(open=True).order_by("-pk")

  context={
      'post_list' : post_list,
      }
  return render(request,'closet/our_closet.html',context=context)

def create_clothes(request, *args, **kwargs):
  error = '아직 입력하지 않은 값이 있습니다.'
  context={
    'error' : error,
    }
  if request.method == "POST":
    try:
      clothes = request.POST["clothes"]
    except MultiValueDictKeyError:
      return render(request, "closet/clothes_create.html", context=context) 
    if clothes == 'top':
      kind = Top
    elif clothes == 'bottom':
      kind = Bottom
    elif clothes == 'outer':
      kind = Outer
    elif clothes == 'shoes':
      kind = Shoes
    elif clothes == 'acc':
      kind = Acc
    author = request.user
    kind.objects.create(
      title=request.POST["title"],
      img=request.FILES["image"],
      buying=request.POST["buying"],
      author=author,
    )
    return redirect('closet:closet_main')
  return render(request, "closet/clothes_create.html") 

@require_POST
def clothes_likes(request, pk, *args, **kwargs):
  if request.user.is_authenticated:
    clothes = get_object_or_404(Clothes, pk=pk)
    users = clothes.likes.all()
    if users.filter(pk=request.user.pk).exists():
      clothes.likes.remove(request.user)
    else:
      clothes.likes.add(request.user)
    return redirect('closet:closet_main')
    # return redirect('accouts:login')위에거 대신 이거 떠야함! 나중에 로그인 합치고!!
  return render(request, 'closet/our_closet.html')

def clothes_like_list(request, *args, **kwargs):
  user = User.objects.get(username=request.user)
  clothes_list = Clothes.objects.filter(likes=user)
  context={
    'clothes_list': clothes_list,
  }   
  return render(request,'closet/closet_main.html',context=context)
  
def post_like_list(request, *args, **kwargs):
  user = User.objects.get(username=request.user)
  post_list = Post.objects.filter(likes=user)
  context={
    'post_list': post_list,
  }   
  return render(request,'closet/closet_main.html',context=context)
  