from django.shortcuts import render, redirect
from server.apps.main.models import Post,Clothes,Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView

# Create your views here.
def closet_main(request):
    clothes_list = Clothes.objects.all() 
    b=0
    for a in clothes_list:
        b+=1
    context={
        'clothes_list':clothes_list,
        'clothes_count':b
        }   
    return render(request,'closet/closet_main.html',context=context)

def closet_main2(request):
    this_user = request.user
    post_list = Post.objects.all() 

    context={
        'post_list':post_list,
        }   
    return render(request,'closet/closet_main2.html',context=context)

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Post
  fields = ['main_img', 'title', 'clothes']
  
  template_name = 'closet/post_create.html'

  def test_func(self):
    return self.request.user.is_superuser or self.request.user.is_staff

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
      form.instance.author = current_user
      return super(PostCreate, self).form_valid(form)
    else:
      return redirect('closet:closet_main')

class ClothesCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Clothes
  fields = ['img', 'category']
  
  template_name = 'closet/clothes_create.html'

  def test_func(self):
    return self.request.user

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      #form.instance.author = current_user
      return super(ClothesCreate, self).form_valid(form)
    else:
      return redirect('closet:closet_main')