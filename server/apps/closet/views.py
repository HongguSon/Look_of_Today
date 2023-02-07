from django.shortcuts import render, redirect
from server.apps.main.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from itertools import chain

# Create your views here.
def closet_main(request):
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
    this_user = request.user
    # post_list = Post.objects.all() 

    context={
        # 'post_list':post_list,
        }   
    return render(request,'closet/closet_main2.html',context=context)


class OuterCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Outer
    fields = ['img','title']

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

