import json
from django.shortcuts import render, redirect, get_object_or_404
from server.apps.main.models import *
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.views.generic import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
        new_post = Post.objects.create(
            title=request.POST["title"],
            main_img=request.FILES.get("image"),
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
        return redirect('closet:closet_main')
    
    context = {
        'outer_list' : outer_list,
        'top_list' : top_list,
        'bottom_list' : bottom_list,
        'shoes_list' : shoes_list,
        'acc_list' : acc_list,
    }
    
    return render(request, "community/post_create.html", context=context)

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
    
    comment = PostComment.objects.create(
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

def delete_pcomment(request, pk, *args, **kwargs):
    comment = get_object_or_404(PostComment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect('community:post_detail', post.pk)
    else:
        PermissionDenied

class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['main_img', 'title', 'open', 'top', 'bottom', 'acc', 'outer', 'shoes']
    
    template_name = 'community/post_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
def post_update(request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    outer_list = Outer.objects.filter(author=request.user)
    top_list = Top.objects.filter(author=request.user)
    bottom_list = Bottom.objects.filter(author=request.user)
    shoes_list = Shoes.objects.filter(author=request.user)
    acc_list = Acc.objects.filter(author=request.user)
    
    context = {
        'post': post,
        'outer_list' : outer_list,
        'top_list' : top_list,
        'bottom_list' : bottom_list,
        'shoes_list' : shoes_list,
        'acc_list' : acc_list,
    }
    
    if request.method == "POST":
        post.title=request.POST["title"]
        if request.FILES.get("image"):
            post.main_img=request.FILES.get("image")
        post.author=request.user 
        post.open=request.POST["open"]
        int_outer = list(map(int, request.POST.getlist('outer')))
        int_top = list(map(int, request.POST.getlist('top')))
        int_bottom = list(map(int, request.POST.getlist('bottom')))
        int_shoes = list(map(int, request.POST.getlist('shoes')))
        int_acc = list(map(int, request.POST.getlist('acc')))
        post.outer.clear()
        post.top.clear()
        post.bottom.clear()
        post.shoes.clear()
        post.acc.clear()
        for i in int_outer:
            post.outer.add(i)
        for i in int_top:
            post.top.add(i)   
        for i in int_bottom:
            post.bottom.add(i)
        for i in int_shoes:
            post.shoes.add(i)
        for i in int_acc:
            post.acc.add(i)
        post.save()
        return redirect("community:post_detail", pk)
    
    return render(request, "community/post_update.html", context=context)
    
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
        # return redirect('accouts:login')위에거 대신 이거 떠야함! 나중에 로그인 합치고!!
    return render(request, 'community/post_detail.html')


# 여기까지가 옷장이고
# 여기서부터가 커뮤니티

class TalkCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Talk
    fields = ['category', 'img', 'title', 'content']
    template_name = 'community/talk_create.html'

    def test_func(self):
        return self.request.user

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(TalkCreate, self).form_valid(form)
        else:
            return redirect('community:community_main')

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
    
    comment = TalkComment.objects.create(
        talk = talk,
        author = request.user,
        content = data.get('content'),)
    comment.save()

    context = {
        'author' : str(comment.author),
        'talk_id' : talk.id,
        'content' : comment.content,
        'comment_id' : comment.id,
    }
    
    return JsonResponse(context)

def delete_tcomment(request, pk, *args, **kwargs):
    tcomment = get_object_or_404(TalkComment, pk=pk)
    talk = tcomment.post
    if request.user.is_authenticated and request.user == tcomment.author:
        tcomment.delete()
        return redirect('community:talk_detail', talk.pk)
    else:
        PermissionDenied

class TalkUpdate(LoginRequiredMixin,UpdateView):
    model = Talk
    fields = ['category', 'img', 'title', 'content']
    template_name = 'community/post_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(TalkUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
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

def community_main(request, *args, **kwargs):
    talk_list = Talk.objects.all()
    t_comments = TalkComment.objects.all()
    title = "모든 게시물" 
    if talk_list:
        for i in talk_list:
            talk_pk = i.pk
    else:
        talk_pk = 0
    comments_count=[0 for i in range(talk_pk)]
    comments_count.append(0)
    for t_comment in t_comments:
        for talk in talk_list:
            if talk.pk == t_comment.talk.pk:
                comments_count[talk.pk]+=1
            print(talk.pk)
    context={
        'talk_list' : talk_list,
        'title' : title,
        'comments_count' : comments_count,
        }   
    print(comments_count)
    return render(request,'community/community.html',context=context)

# def community_kind(request, category, *args, **kwargs):
#     talk_list = Talk.objects.filter(category=category)
#     context={
#         'talk_list' : talk_list,
#         'category' : category,
#     }   
#     return render(request,'community/community.html',context=context)

def openrun(request,*args, **kwargs):
    talk_list = Talk.objects.filter(category='오픈런')
    title = "오픈런"
    context={
        'talk_list' : talk_list,
        'title' : title,
        }   
    return render(request,'community/community.html',context=context)

def other(request,*args, **kwargs):
    talk_list = Talk.objects.filter(category='잡담방')
    title = "잡담방"
    context={
        'talk_list' : talk_list,
        'title' : title,
        }   
    return render(request,'community/community.html',context=context)

def buying(request,*args, **kwargs):
    talk_list = Talk.objects.filter(category='공동 구매')
    title = "공구방"
    context={
        'talk_list' : talk_list,
        'title' : title,
        }   
    return render(request,'community/community.html',context=context)