import json
from django.shortcuts import render, redirect
from server.apps.main.models import *
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.views.generic import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
def community_main(request, *args, **kwargs):
    post_list = Talk.objects.all() 
    if request.user.is_authenticated:
      post_count = Talk.objects.filter(author=request.user).count()
      comment_count = Comment_Talk.objects.filter(author=request.user).count()
    else:
      post_count = 0
      comment_count = 0
    context={
        'post_list' : post_list,
        'post_count': post_count,
        'comment_count': comment_count,
        }   
    return render(request,'community/community.html',context=context)

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Post
  fields = ['main_img', 'title', 'open', 'top', 'bottom', 'acc', 'outer', 'shoes']
  template_name = 'community/post_create.html'

  def test_func(self):
    return self.request.user

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      form.instance.author = current_user
      return super(TalkCreate, self).form_valid(form)
    else:
      return redirect('closet:our_closet')

def talk_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        post = Post.objects.get(pk=pk)
        post.delete()
    return redirect("community:community_main")

def post_detail(request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=pk)
    context = {
        'post' : post,
        'comments' : comments,
    }
    return render(request, 'community/talk_detail.html', context=context)

@csrf_exempt
def comment_talk_ajax(request, *args, **kwargs):
    data = json.loads(request.body)
    post = Talk.objects.get(id=data["post_id"])
    
    comment = Comment_Talk.objects.create(
        talk = post,
        author = request.user,
        content = data.get('content'),)
    comment.save()

    context = {
        'author' : str(comment.author),
        'post_id' : post.id,
        'content' : comment.content,
        'comment_id' : comment.id,
    }
    
    return JsonResponse(context)

@require_POST
def talk_likes(request, pk, *args, **kwargs):
    if request.user.is_authenticated:
        article = get_object_or_404(Talk, pk=pk)
        users=article.likes.all()
        if users.filter(pk=request.user.pk).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return redirect('community:talk_detail',pk)
        # return redirect('accouts:login')위에거 대신 이거 떠야함! 나중에 로그인 합치고!!
    return render(request, 'community:talk_detail.html')

class TalkUpdate(LoginRequiredMixin,UpdateView):
  model = Talk
  fields = ['category','img','title', 'content']
  template_name = 'community/post_update.html'

  def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(TalkUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def openrun(request,*args, **kwargs):
    openrun_list = Talk.objects.filter(category='오픈런')
    title = "오픈런"
    if request.user.is_authenticated:
      post_count = Talk.objects.filter(author=request.user).count()
      comment_count = Comment_Talk.objects.filter(author=request.user).count()
    else:
      post_count = 0
      comment_count = 0
    context={
        'title' : title,
        'post_list' : openrun_list,
        'post_count': post_count,
        'comment_count': comment_count,
        }   
    return render(request,'community/commu_view.html',context=context)

def other(request,*args, **kwargs):
    other_list = Talk.objects.filter(category='고민방')
    title = "고민방"
    if request.user.is_authenticated:
      post_count = Talk.objects.filter(author=request.user).count()
      comment_count = Comment_Talk.objects.filter(author=request.user).count()
    else:
      post_count = 0
      comment_count = 0
    context={
        'title' : title,
        'post_list' : other_list,
        'post_count': post_count,
        'comment_count': comment_count,
        }   
    return render(request,'community/commu_view.html',context=context)

def buying(request,*args, **kwargs):
    buying_list = Talk.objects.filter(category='공동 구매')
    title = "공구방"
    # if request.user.is_authenticated:
    #     post_count=buying_list.filter(author=request.user).count()
    #     comment_count= Comment_Talk.buying_list.filter(author=request.user).count()
    # context={
    #     'post_list' : buying_list,
    #     'title' : title,
    #     }   
    # post_list = Talk.objects.all() 
    if request.user.is_authenticated:
      post_count = Talk.objects.filter(author=request.user).count()
      comment_count = Comment_Talk.objects.filter(author=request.user).count()
    else:
      post_count = 0
      comment_count = 0
    context={
        'title' : title,
        'post_list' : buying_list,
        'post_count': post_count,
        'comment_count': comment_count,
        }   
    return render(request,'community/commu_view.html',context=context)

class TalkCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Talk
  fields = ['category','img','title', 'content']
  template_name = 'community/post_create.html'

  def test_func(self):
    return self.request.user

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated:
      form.instance.author = current_user
      return super(TalkCreate, self).form_valid(form)
    else:
      return redirect('community:community_main')

def talk_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        post = Talk.objects.get(pk=pk)
        post.delete()
    return redirect("community:community_main")

def talk_detail(request, pk, *args, **kwargs):
    post = Talk.objects.get(pk=pk)
    comments = Comment_Talk.objects.filter(talk=pk)
    context = {
        'post' : post,
        'comments' : comments,
    }
    return render(request, 'community/talk_detail.html', context=context)

@csrf_exempt
def comment_talk_ajax(request, *args, **kwargs):
    data = json.loads(request.body)
    post = Talk.objects.get(id=data["post_id"])
    
    comment = Comment_Talk.objects.create(
        talk = post,
        author = request.user,
        content = data.get('content'),)
    comment.save()

    context = {
        'author' : str(comment.author),
        'post_id' : post.id,
        'content' : comment.content,
        'comment_id' : comment.id,
    }
    
    return JsonResponse(context)

@require_POST
def talk_likes(request, pk, *args, **kwargs):
    if request.user.is_authenticated:
        article = get_object_or_404(Talk, pk=pk)
        users=article.likes.all()
        if users.filter(pk=request.user.pk).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return redirect('community:talk_detail',pk)
        # return redirect('accouts:login')위에거 대신 이거 떠야함! 나중에 로그인 합치고!!
    return render(request, 'community:talk_detail.html')

class TalkUpdate(LoginRequiredMixin,UpdateView):
  model = Talk
  fields = ['category','img','title', 'content']
  template_name = 'community/post_update.html'

  def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(TalkUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def openrun(request,*args, **kwargs):
    openrun_list = Talk.objects.filter(category='오픈런')
    title = "오픈런"
    if request.user.is_authenticated:
      post_count = Talk.objects.filter(author=request.user).count()
      comment_count = Comment_Talk.objects.filter(author=request.user).count()
    else:
      post_count = 0
      comment_count = 0
    context={
        'title' : title,
        'post_list' : openrun_list,
        'post_count': post_count,
        'comment_count': comment_count,
        }   
    return render(request,'community/commu_view.html',context=context)

def other(request,*args, **kwargs):
    other_list = Talk.objects.filter(category='고민방')
    title = "고민방"
    if request.user.is_authenticated:
      post_count = Talk.objects.filter(author=request.user).count()
      comment_count = Comment_Talk.objects.filter(author=request.user).count()
    else:
      post_count = 0
      comment_count = 0
    context={
        'title' : title,
        'post_list' : other_list,
        'post_count': post_count,
        'comment_count': comment_count,
        }   
    return render(request,'community/commu_view.html',context=context)

def buying(request,*args, **kwargs):
    buying_list = Talk.objects.filter(category='공동 구매')
    title = "공구방"
    # if request.user.is_authenticated:
    #     post_count=buying_list.filter(author=request.user).count()
    #     comment_count= Comment_Talk.buying_list.filter(author=request.user).count()
    # context={
    #     'post_list' : buying_list,
    #     'title' : title,
    #     }   
    # post_list = Talk.objects.all() 
    if request.user.is_authenticated:
      post_count = Talk.objects.filter(author=request.user).count()
      comment_count = Comment_Talk.objects.filter(author=request.user).count()
    else:
      post_count = 0
      comment_count = 0
    context={
        'title' : title,
        'post_list' : buying_list,
        'post_count': post_count,
        'comment_count': comment_count,
        }   
    return render(request,'community/commu_view.html',context=context)

@csrf_exempt
def comment_ajax(request, *args, **kwargs):
    data = json.loads(request.body)
    post = Post.objects.get(id=data["post_id"])
    
    comment = Comment.objects.create(
        post = post,
        author = request.user,
        content = data.get('content'),)
    comment.save()

    context = {
        'author' : str(comment.author),
        'post_id' : post.id,
        'content' : comment.content,
        'comment_id' : comment.id,
    }
    
    return JsonResponse(context)

def post_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        post = Post.objects.get(pk=pk)
        post.delete()
    return redirect("/")

class PostUpdate(LoginRequiredMixin,UpdateView):
  model = Post
  fields = ['main_img', 'title','open',  'top','bottom','acc','outter','shose']
  
  template_name = 'community/update.html'

  def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

@require_POST
def post_likes(request, pk, *args, **kwargs):
    if request.user.is_authenticated:
        article = get_object_or_404(Talk, pk=pk)
        users=article.likes.all()
        if users.filter(pk=request.user.pk).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return redirect('community:post_detail',pk)
        # return redirect('accouts:login')위에거 대신 이거 떠야함! 나중에 로그인 합치고!!
    return render(request, 'community:detail.html')