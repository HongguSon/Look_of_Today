from django.shortcuts import render, redirect
from server.apps.main.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView

# Create your views here.
def closet_main(request):
    # clothes_list = Clothes.objects.all() 
    # clothes_count = Clothes.objects.all().count()
    context={
        # 'clothes_list' : clothes_list,
        # 'clothes_count' : clothes_count,
        }   
    return render(request,'closet/closet_main.html',context=context)

def closet_main2(request):
    this_user = request.user
    # post_list = Post.objects.all() 

    context={
        # 'post_list':post_list,
        }   
    return render(request,'closet/closet_main2.html',context=context)

# class ClothesCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#   model = Clothes
#   fields = ['img','title', 'category', 'buying']
  
#   template_name = 'closet/clothes_create.html'

#   def test_func(self):
#     return self.request.user

#   def form_valid(self, form):
#     current_user = self.request.user
#     if current_user.is_authenticated:
#       form.instance.author = current_user
#       return super(ClothesCreate, self).form_valid(form)
#     else:
#       return redirect('closet:closet_main')

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
