from django.shortcuts import render, redirect, get_object_or_404
from server.apps.main.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.views.decorators.http import require_POST
from itertools import chain
from rembg import remove
from PIL import Image
import os


# Create your views here.
# REVIEW : mysql 파일 삭제 요망
def closet_main(request, *args, **kwargs):
  clothes_list = Clothes.objects.filter(author=request.user)
  context = {
    'clothes_list': clothes_list,
  }
  return render(request,'closet/closet_main.html', context=context)

def closet_all(request, *args, **kwargs):
  post_list = Post.objects.all() 
  context={
      'post_list':post_list,
  }   
  return render(request,'closet/closet_all.html',context=context)

def clothes_list(request, Clothes, *args, **kwargs):
  clothes_mapping = {
    'top': Top,
    'bottom': Bottom,
    'outer': Outer,
    'shoes': Shoes,
    'acc': Acc,
  }
  clothes_list = clothes_mapping.get(Clothes).objects.filter(author=request.user)
  context={
    'clothes_list': clothes_list,
    }   
  return render(request,'closet/closet_main.html',context=context)
  
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
    post_list = Post.objects.filter(open=True)

    context={
        'post_list' : post_list,
        }
    return render(request,'closet/our_closet.html',context=context)

class TopCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Top
  fields = ['img', 'title', 'buying']

  template_name = 'closet/clothes_create.html'

  def test_func(self):
    return self.request.user

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      form.instance.author = current_user
      return super(TopCreate, self).form_valid(form)
    else:
      return redirect('closet:closet_main')

class BottomCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Bottom
  fields = ['img', 'title', 'buying']

  template_name = 'closet/clothes_create.html'

  def test_func(self):
    return self.request.user

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      form.instance.author = current_user
      return super(BottomCreate, self).form_valid(form)
    else:
      return redirect('closet:closet_main')

class OuterCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Outer
  fields = ['img', 'title', 'buying']

  template_name = 'closet/clothes_create.html'

  def test_func(self):
    return self.request.user

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      form.instance.author = current_user
      return super(OuterCreate, self).form_valid(form)
    else:
      return redirect('closet:closet_main')

class AccCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Acc
  fields = ['img', 'title', 'buying']

  template_name = 'closet/clothes_create.html'

  def test_func(self):
    return self.request.user

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      form.instance.author = current_user
      return super(AccCreate, self).form_valid(form)
    else:
      return redirect('closet:closet_main')

class ShoesCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Shoes
  fields = ['img', 'title', 'buying']

  template_name = 'closet/clothes_create.html'

  def test_func(self):
    return self.request.user

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      form.instance.author = current_user
      return super(ShoesCreate, self).form_valid(form)
    else:
      return redirect('closet:closet_main')

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

# class ClothesCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#   context_object_name = 'clothes'
#   template_name = 'closet/clothes_create.html'

#   def dispatch(self, request, *args, **kwargs):
#     clothes_kind = kwargs.get('clothes', None)
#     if clothes_kind == 'dog':
#       self.model = Dog
#     elif clothes_kind == 'cat':
#       self.model = Cat

#     return super(AnimalDetailView, self).dispatch(request, *args, **kwargs)

#   def get_queryset(self):
#       return self.model.objects.filter()

# def clothes_remimg(request, pk, *args, **kwargs):
#   if request.user.is_authenticated:
#   #   clothes = get_object_or_404(Clothes, pk=pk)
#     # users = article.likes.all()
#   # if request.method == 'POST':
#     # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     BASE_DIR = r'C:\Users\yj418\OneDrive\바탕 화면\피로그래밍\final\Look_of_Today\server'
#     clothes = Clothes.objects.get(pk=pk)
#     input_url = BASE_DIR + clothes.img.url
#     input = Image.open(input_url)
#     output = remove(input)
#     .save(output)
#     # input_path = clothes.img.url # input image path
#     # output_path = clothes.rem_img # output image path

#     # input = Image.open(input_path) # load image
#     # output = remove(input) # remove background
#     # output.save(output_path) # save image
    
#     # input_path = clothes.img.url
#     # output_pathe = input_url.replace("images", "results")
    
#     return redirect('closet:closet_main')

#     # context= {
#     #   "clothes":clothes ,
#     # }
#     # return render(request, "closet/closet_main.html",context=context)


# 누끼 개발중
def clothes_remimg(request, pk, *args, **kwargs):
  if request.user.is_authenticated:
    clothes_list = Clothes.objects.filter(author=request.user)
    clothes = Clothes.objects.get(pk=pk)
    clothes_url=clothes.img.url
    new_url_print=clothes_url #출력을 위한 경로
    # basic_url = r'C:\Users\yj418\OneDrive\바탕 화면\피로그래밍\final\Look_of_Today\server'
    basic_url = '/Users/hongguson/Desktop/Look_of_Today/Look_of_Today/server'
    clothes_url= basic_url + clothes_url
    input=Image.open(clothes_url)
    output=remove(input)
    dir,file = os.path.split(clothes_url)
    new_url=dir+'/redu_'+file
    output=output.convert("RGB")
    output.save(new_url) #파일에는 이렇게 해야 같은 폴더에 들어감..!
    n_dir,n_file=os.path.split(new_url_print)
    new_url_print=n_dir+'/redu_'+n_file
    context = {
      'clothes_list': clothes_list,
      'clothes_url':clothes_url,
      'new_url' : new_url_print,
    }
    return render(request,'closet/closet_main.html', context=context)