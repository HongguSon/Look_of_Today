from django.shortcuts import render,redirect
from server.apps.main.models import Post,Clothes
from django.http.request import HttpRequest
# Create your views here.
def community_main(request):
    post_list = Post.objects.all() 
    context={
        'post_list':post_list
        }   
    return render(request,'community\community.html',context=context)

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