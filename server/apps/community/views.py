import json
from django.shortcuts import render, redirect
from server.apps.main.models import Post,Clothes,Comment
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin







# Create your views here.
def community_main(request):
    post_list = Post.objects.all() 
    context={
        'post_list':post_list
        }   
    return render(request,'community/community.html',context=context)
<<<<<<< HEAD
=======

def detail(request,pk):
    post = Post.objects.get(id=pk)
    print(post)
    context={
        "post": post,
    }
    return render(request,'community/post_detail.html',context=context)
>>>>>>> gokun

def delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        post.delete()
    return redirect("/")

@require_POST
def likes(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Post, pk=pk)
        users=article.likes.all()
        if users.filter(pk=request.user.pk).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return redirect('community:community_main')
        
        # return redirect('accouts:login')위에거 대신 이거 떠야함! 나중에 로그인 합치고!!
    return render(request, 'community:detail.html')

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['main_img', 'title', 'clothes']

    template_name = 'community/post_create.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('community:community_main')

def post_create(request):
    return render(request, 'community/post_create.html')

def post_detail(request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    context = {
        'post' : post,
    }
    return render(request, 'community/post_detail.html', context=context)


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


class update(LoginRequiredMixin,UpdateView):
  model = Post
  fields = ['main_img', 'title', 'clothes']
  
  template_name = 'community/update.html'

  def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(update, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

