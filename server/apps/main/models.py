from django.db import models
from django.contrib.auth.models import User


# Create your models here.
  

class Top(models.Model):
  img = models.ImageField(upload_to='main/images/clothes/%Y/%m/%d')
  title = models.CharField(max_length=100,unique=True)
  like = models.ManyToManyField(User, related_name='TopLike', blank=True)
  buying = models.TextField(null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.title}'
  
  def get_absolute_url(self):
    return f'/closet/'
  
class Bottom(models.Model):
  img = models.ImageField(upload_to='main/images/clothes/%Y/%m/%d')
  title = models.CharField(max_length=100,unique=True)
  like = models.ManyToManyField(User, related_name='BottomLike', blank=True)
  buying = models.TextField(null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.title}'
  
  def get_absolute_url(self):
    return f'/closet/'

class Outer(models.Model):
  img = models.ImageField(upload_to='main/images/clothes/%Y/%m/%d')
  title = models.CharField(max_length=100,unique=True)
  like = models.ManyToManyField(User, related_name='OutterLike', blank=True)
  buying = models.TextField(null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.title}'
  
  def get_absolute_url(self):
    return f'/closet/'

class Shoes(models.Model):
  img = models.ImageField(upload_to='main/images/clothes/%Y/%m/%d')
  title = models.CharField(max_length=100,unique=True)
  like = models.ManyToManyField(User, related_name='ShoesLike', blank=True)
  buying = models.TextField(null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.title}'
  
  def get_absolute_url(self):
    return f'/closet/'

class Acc(models.Model):
  img = models.ImageField(upload_to='main/images/clothes/%Y/%m/%d')
  title = models.CharField(max_length=100,unique=True)
  like = models.ManyToManyField(User, related_name='AccLike', blank=True)
  buying = models.TextField(null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.title}'
  
  def get_absolute_url(self):
    return f'/closet/'
  

class Post(models.Model):
  main_img = models.ImageField(upload_to='main/images/post/%Y/%m/%d')
  title = models.CharField(max_length=100)
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  top = models.ManyToManyField(Top, related_name='Top', blank=True)
  bottom = models.ManyToManyField(Bottom,  related_name='Bottom', blank=True)
  acc = models.ManyToManyField(Acc, related_name='Acc', blank=True)
  outer= models.ManyToManyField(Outer, related_name='Outter', blank=True)
  shoes= models.ManyToManyField(Shoes, related_name='Shose', blank=True)

  likes = models.ManyToManyField(User, related_name='Likes', blank=True)
  open = models.BooleanField(default=False)
  
  def __str__(self):
    return f'{self.pk}: {self.title}'
  
  def get_absolute_url(self):
    return f'/community/'
  #이거 나중에 detail page로 바꿔주세요
  

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f'({self.author}) {self.post.title} :  {self.content}'

class Talk(models.Model):
  Talk_CHOICES = (
    ('공동 구매', '공동 구매'), #공동구매
    ('오픈런', '오픈런'), #오픈런
    ('고민방', '고민방'), #고민방
  )
  category = models.CharField( max_length=5,choices=Talk_CHOICES)
  img = models.ImageField(upload_to='main/images/commu/%Y/%m/%d', null=True, blank=True)
  title = models.CharField(max_length=100)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  create_date = models.DateTimeField(auto_now_add=True)
  # update_date = models.DateTimeField(auto_now=True)
  likes = models.ManyToManyField(User, related_name='Talk_Likes', blank=True)


  def __str__(self):
    return f'{self.pk}: {self.title}'

  def total_likes(self):
        return self.likes.count()

  def get_absolute_url(self):
    return f'/community/'


class Comment_Talk(models.Model):
  talk = models.ForeignKey(Talk, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f'({self.author}) {self.talk.title} :  {self.content}'