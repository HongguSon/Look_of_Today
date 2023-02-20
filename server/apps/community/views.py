import json
from django.shortcuts import render, redirect, get_object_or_404
from server.apps.main.models import *
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger , EmptyPage
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.views.generic import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from server.apps.user.models import Profile

def post_create(request, *args, **kwargs):
    outer_list = Outer.objects.filter(author=request.user)
    top_list = Top.objects.filter(author=request.user)
    bottom_list = Bottom.objects.filter(author=request.user)
    shoes_list = Shoes.objects.filter(author=request.user)
    acc_list = Acc.objects.filter(author=request.user)
    
    if request.method == "POST":
        int_outer = list(map(int, request.POST.getlist('outer')))
        int_top = list(map(int, request.POST.getlist('top')))
        int_bottom = list(map(int, request.POST.getlist('bottom')))
        int_shoes = list(map(int, request.POST.getlist('shoes')))
        int_acc = list(map(int, request.POST.getlist('acc')))
        if not request.POST["title"] or not request.FILES.get("look"):
            error = '에러'
            context = {
                'outer_list' : outer_list,
                'top_list' : top_list,
                'bottom_list' : bottom_list,
                'shoes_list' : shoes_list,
                'acc_list' : acc_list,
                'error' : error,
            }
            
            return render(request, "community/post_create.html", context=context)
        new_post = Post.objects.create(
            title=request.POST["title"],
            main_img=request.FILES.get("look"),
            author=request.user,
            open=request.POST["open"],
        )
        for i in int_outer:
            new_post.outer.add(i)
        for i in int_top:
            new_post.top.add(i)   
        for i in int_bottom:
            new_post.bottom.add(i)
        for i in int_shoes:
            new_post.shoes.add(i)
        for i in int_acc:
            new_post.acc.add(i)
        new_post.save()
        return redirect('closet:our_closet')
    
    context = {
        'outer_list' : outer_list,
        'top_list' : top_list,
        'bottom_list' : bottom_list,
        'shoes_list' : shoes_list,
        'acc_list' : acc_list,
    }
    
    return render(request, "community/post_create.html", context=context)

@csrf_exempt
def post_create_img(request, pk):
  req = json.loads(request.body)
  id = req['id']
  return JsonResponse({'id' : id})

def post_detail(request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    comments = PostComment.objects.filter(post=pk)
    context = {
        'post' : post,
        'comments' : comments,
    }
    return render(request, 'community/post_detail.html', context=context)

@csrf_exempt
def comment_ajax(request, *args, **kwargs):
    data = json.loads(request.body)
    post = Post.objects.get(id=data["post_id"])
    profile = Profile.objects.get(user=request.user)
    
    comment = PostComment.objects.create(
        post = post,
        author = request.user,
        content = data.get('content'),)
    comment.save()
    
    if profile.profile_image:
      user_img_url = profile.profile_image.url
    else:
      user_img_url = 0

    context = {
        'user_img_url' : user_img_url,
        'author' : str(comment.author),
        'post_id' : post.id,
        'content' : comment.content,
        'comment_id' : comment.id,
    }
    return JsonResponse(context)

def delete_pcomment(request, pk, *args, **kwargs):
    comment = get_object_or_404(PostComment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect('community:post_detail', post.pk)
    else:
        PermissionDenied

def post_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        post = Post.objects.get(pk=pk)
        post.delete()
    return redirect("/")

@require_POST
def post_likes(request, pk, *args, **kwargs):
    if request.user.is_authenticated:
        article = get_object_or_404(Post, pk=pk)
        users = article.likes.all()
        if users.filter(pk=request.user.pk).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return redirect('community:post_detail',pk)
    return render(request, 'community/post_detail.html')


# 여기까지가 옷장이고
# 여기서부터가 커뮤니티

def talk_create(request, *args, **kwargs):
  user = request.user
  context = {
    'user': user,
  }
  if request.method == "POST":
    if not request.POST['category'] or not request.POST['content'] or not request.POST['title']:
      error = '에러'
      context = {
        'user': user,
        'error': error,
      }
      return render(request, "community/talk_create.html", context=context)
    Talk.objects.create(
      author = User.objects.get(username=user),
      category = request.POST['category'],
      content = request.POST['content'],
      img = request.FILES.get("image"),
      title = request.POST['title'],
    )
    return redirect("community:community_main")
  return render(request, "community/talk_create.html", context=context)

@csrf_exempt
def talk_create_img(request, pk, *args, **kwargs):
    req = json.loads(request.body)
    id = req['id']
    return JsonResponse({'id' : id})

def talk_detail(request, pk, *args, **kwargs):
    talk = Talk.objects.get(pk=pk)
    t_comments = TalkComment.objects.filter(talk=pk)
    context = {
        'talk' : talk,
        't_comments' : t_comments,
    }
    return render(request, 'community/talk_detail.html', context=context)

@csrf_exempt
def comment_talk_ajax(request, *args, **kwargs):
  data = json.loads(request.body)
  talk = Talk.objects.get(id=data["talk_id"])
  profile = Profile.objects.get(user=request.user)
  
  comment = TalkComment.objects.create(
    talk = talk,
    author = request.user,
    content = data.get('content'),)
  comment.save()

  if profile.profile_image:
    user_img_url = profile.profile_image.url
  else:
    user_img_url = 0
    
  context = {
    'user_img_url' : user_img_url,
    'author' : str(comment.author),
    'talk_id' : talk.id,
    'content' : comment.content,
    'comment_id' : comment.id,
  }
    
  return JsonResponse(context)

def delete_tcomment(request, pk, *args, **kwargs):
    tcomment = get_object_or_404(TalkComment, pk=pk)
    talk = tcomment.talk
    if request.user.is_authenticated and request.user == tcomment.author:
        tcomment.delete()
        return redirect('community:talk_detail', talk.pk)
    else:
        PermissionDenied

def talk_update(request, pk, *args, **kwargs):
  talk = Talk.objects.get(id=pk)
  context = {
    'talk' : talk,
  }
  if request.method == "POST":
    if not request.POST['category'] or not request.POST['content'] or not request.POST['title']:
      error = '에러'
      context = {
        'talk' : talk,
        'error': error,
      }
      return render(request, "community/talk_update.html", context=context)
    talk.title=request.POST["title"]
    talk.category=request.POST["category"]
    talk.content=request.POST["content"]
    talk.img = request.FILES.get("image")
    talk.save()
    return redirect(f"/community/talk-detail/{talk.id}")
  return render(request, "community/talk_update.html", context=context)
        
def talk_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        talk = Talk.objects.get(pk=pk)
        talk.delete()
    return redirect("community:community_main")

@require_POST
def talk_likes(request, pk, *args, **kwargs):
    if request.user.is_authenticated:
        article = get_object_or_404(Talk, pk=pk)
        users = article.likes.all()
        if users.filter(pk=request.user.pk).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return redirect('community:talk_detail', pk)
        # return redirect('accouts:login')위에거 대신 이거 떠야함! 나중에 로그인 합치고!!
    return render(request, 'community:talk_detail.html')


# -----------------------------------------------------------
#페이지네이션 코드
def paginations(request,talk_list):
    page=request.GET.get('page')
    paginator=Paginator(talk_list,5) #5개씩 보기
    try:
        page_obj=paginator.page(page)
    except PageNotAnInteger:
        page=1
        page_obj=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        page_obj=paginator.page(page)
    return page_obj ,paginator

#댓글 수 세기 코드
def count_comments(talk_list,t_comments):
    if talk_list:
        talk_pk=0
        for i in talk_list:
            if talk_pk<i.pk:
                talk_pk = i.pk
    else:
        talk_pk = 0
    comments_count=[0 for i in range(talk_pk)]
    comments_count.append(0)
    for t_comment in t_comments:
        for talk in talk_list:
            if talk.pk == t_comment.talk.pk:
                comments_count[talk.pk]+=1
    return talk_list,comments_count

#정렬 코드
def sorting(request:HttpRequest,title):
    sort = request.GET.get('sort','')
    if title:
        if sort == 'new':
            talk_list = Talk.objects.filter(category=title).order_by("-pk")
        elif sort == 'old':
            talk_list = Talk.objects.filter(category=title).order_by("pk")
        elif sort == 'like':
            talk_list= Talk.objects.filter(category=title).annotate(likes_count=Count('likes')).order_by('-likes_count')
        else:
            talk_list = Talk.objects.filter(category=title).order_by("-pk")
    else:
        if sort == 'new':
            talk_list = Talk.objects.all().order_by("-pk")
        elif sort == 'old':
            talk_list = Talk.objects.all().order_by("pk")
        elif sort == 'like':
            talk_list= Talk.objects.all().annotate(likes_count=Count('likes')).order_by('-likes_count')
        else:
            talk_list = Talk.objects.all().order_by("-pk")        
    return talk_list,sort

def community_main(request:HttpRequest, *args, **kwargs):
    title = "모든 게시물"
    t_comments=TalkComment.objects.all()
    # talk_list=sorting(request)
    talk_list,sort=sorting(request,None)
    talk_list,comments_count = count_comments(talk_list,t_comments)
    page_obj ,paginator = paginations(request,talk_list)
    context={
        'talk_list' : talk_list,'title' : title,'comments_count' : comments_count,'page_obj':page_obj,'paginator':paginator,'sort':sort,
        }   
    return render(request,'community/community.html',context=context)

def openrun(request:HttpRequest,*args, **kwargs):
    talk_list = Talk.objects.filter(category="오픈런")
    title = "오픈런"
    t_comments=TalkComment.objects.all()
    talk_list,sort=sorting(request,title)
    page_obj ,paginator = paginations(request,talk_list)
    comments_count = count_comments(talk_list,t_comments)
    context={
        'talk_list' : talk_list,'title' : title,'comments_count' : comments_count,'page_obj':page_obj,'paginator':paginator,'sort':sort,
        }   
    return render(request,'community/community.html',context=context)

def other(request:HttpRequest,*args, **kwargs):
    talk_list = Talk.objects.filter(category='잡담방')
    title = "잡담방"
    t_comments=TalkComment.objects.all()
    talk_list,sort=sorting(request,title)
    page_obj ,paginator = paginations(request,talk_list)
    comments_count = count_comments(talk_list,t_comments)
    context={
        'talk_list' : talk_list,'title' : title,'comments_count' : comments_count,'page_obj':page_obj,'paginator':paginator,'sort':sort,
        }   
    return render(request,'community/community.html',context=context)

def buying(request:HttpRequest,*args, **kwargs):
    talk_list = Talk.objects.filter(category='공동 구매')
    title = "공동 구매"
    t_comments=TalkComment.objects.all()
    talk_list,sort=sorting(request,title)
    page_obj ,paginator = paginations(request,talk_list)
    comments_count = count_comments(talk_list,t_comments)
    context={
        'talk_list' : talk_list,'title' : title,'comments_count' : comments_count,'page_obj':page_obj,'paginator':paginator,'sort':sort,
        }   
    return render(request,'community/community.html',context=context)