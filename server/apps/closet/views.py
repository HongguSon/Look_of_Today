from django.shortcuts import render, redirect
from server.apps.main.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from itertools import chain

# Create your views here.
# REVIEW : mysql 파일 삭제 요망
def closet_main(request):
    # REVIEW : qs1, qs2 보다 의미있는 변수명 필요
    # REVIEW : 변수명 의미가 없다면, 각각 따로 정의할 필요없이 아래 처럼 코딩 가능
    # clothe_set = set()
    # for Model in [Outer, Top, Bottom, Shoes, Acc]:
    #     chothe_set = clothe_set.union(Model.objects.filter(author=request.user))
    qs1 = Outer.objects.filter(author=request.user)
    qs2 = Top.objects.filter(author=request.user)
    qs3 = Bottom.objects.filter(author=request.user)
    qs4 = Shoes.objects.filter(author=request.user)
    qs5 = Acc.objects.filter(author=request.user)
    clothes_list = []
    clothes_all = qs1.union(qs2, qs3, qs4, qs5)
    # clothes_list = clothes_all.objects.filter(author=request.user)
    context ={
        'clothes_list': clothes_all
    }
    return render(request,'closet/closet_main.html', context=context)

def closet_main2(request):
    # REVIEW : this_user를 따로 정의하는 이유는?
    this_user = request.user
    # post_list = Post.objects.all()

    context={
        # 'post_list':post_list,
        }
    return render(request,'closet/closet_main2.html',context=context)


class OuterCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Outer
    fields = ['img','title']

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

    template_name = 'closet/outer_create.html'

    def test_func(self):
        return self.request.user

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(OuterCreate, self).form_valid(form)
        else:
            return redirect('closet:outer_list')

def outer_list(request):
    clothes_list = Outer.objects.filter(author=request.user)

    return render(
        request,
        'closet/closet_main.html',
        {
            'clothes_list': clothes_list,
        })

def top_list(request):
    clothes_list = Top.objects.filter(author=request.user)

    return render(
        request,
        'closet/closet_main.html',
        {
            'clothes_list': clothes_list,
        })

def bottom_list(request):
    clothes_list = Bottom.objects.filter(author=request.user)

    return render(
        request,
        'closet/closet_main.html',
        {
            'clothes_list': clothes_list,
        })

def shoes_list(request):
    clothes_list = Shoes.objects.filter(author=request.user)

    return render(
        request,
        'closet/closet_main.html',
        {
            'clothes_list': clothes_list,
        })

def acc_list(request):
    clothes_list = Acc.objects.filter(author=request.user)

    return render(
        request,
        'closet/closet_main.html',
        {
            'clothes_list': clothes_list,
        })
