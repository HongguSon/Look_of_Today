from django.shortcuts import render, redirect
from server.apps.main.models import Post,Clothes
from django.views.decorators.http import require_POST
from django.http import Http404
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