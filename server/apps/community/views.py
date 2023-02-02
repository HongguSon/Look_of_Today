from django.shortcuts import render,redirect
from server.apps.main.models import Post,Clothes
from django.views.decorators.http import require_POST
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
# Create your views here.
def community_main(request):
    post_list = Post.objects.all() 
    context={
        'post_list':post_list
        }   
    return render(request,'community\community.html',context=context)

def detail(request,pk):
    post = Post.objects.get(id=pk)
    print(post)
    context={
        "post": post,
    }
    return render(request,'community\detail.html',context=context)

def delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        post.delete()
    return redirect("/")

def post_create(request:HttpRequest,*args, **kwargs):
    clothes_list=Clothes.objects.all()
    
    if request.method == "POST":
        clothes_id = request.POST["clothes"] 
        Post.objects.create(
            title=request.POST["title"],
            author=request.user,
            clothes=Clothes.objects.get(id=clothes_id),
            main_img=request.FILES["main_img"],
    )
    context={
        "clothes_list": clothes_list,
    }
    return render(request, 'community\post_create.html',context=context)

def update(request:HttpRequest,*args, **kwargs):
    return render(request, 'community\post_create.html')

@require_POST
def likes(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Post, pk=pk)

        if article.likes.filter(pk=request.user.pk).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return redirect('community:community_main')
    # return redirect('accouts:login')
    return render(request, 'community\community.html')