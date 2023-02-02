from django.shortcuts import render, redirect
from server.apps.main.models import Post,Clothes
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.
def community_main(request):
    post_list = Post.objects.all() 
    context={
        'post_list':post_list
        }   
    return render(request,'community\community.html',context=context)

# def post_create(request:HttpRequest,*args, **kwargs):
#     clothes_list=Clothes.objects.all()
    
#     if request.method == "POST":
#         clothes_id = request.POST["clothes"] 
#         Post.objects.create(
#             title=request.POST["title"],
#             author=request.user,
#             clothes=Clothes.objects.get(id=clothes_id),
#             main_img=request.FILES["main_img"],
#     )
#     context={
#         "clothes_list": clothes_list,
#     }
#     return render(request, 'community\post_create.html',context=context)
  
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