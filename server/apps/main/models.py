from django.db import models
from django.contrib.auth.models import User

# Create your models here.
  
class Category(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name
  
class Clothes(models.Model):
  img = models.ImageField(upload_to='main/images/clothes/%Y/%m/%d')
  like = models.ManyToManyField(User, related_name='Like', blank=True)
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
  buying = models.TextField(null=True, blank=True)
  
  def __str__(self):
    return f'{self.pk}: {self.category}'

# class Closet(models.Model):
  

class Post(models.Model):
  main_img = models.ImageField(upload_to='main/images/post/%Y/%m/%d')
  title = models.CharField(max_length=100)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  clothes = models.ManyToManyField(Clothes)
  likes = models.ManyToManyField(User, related_name='Likes', blank=True)
  
  def __str__(self):
    return f'{self.pk}: {self.title}'
  
  def get_absolute_url(self):
    return f'/community/'
  #이거 나중에 detail page로 바꿔주세요
  
class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  # create_date = models.DateTimeField(auto_now_add=True)
  # update_date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f'({self.author}) {self.post.title} :  {self.content}'
