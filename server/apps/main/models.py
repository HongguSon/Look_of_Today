from django.db import models
from django.contrib.auth.models import User

# Create your models here.
  
class Clothes(models.Model):
  img = models.ImageField(upload_to='main/images/clothes/%Y/%m/%d')
  save = models.ManyToManyField(User, related_name='Save', blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  CATEGORYS =[
    ('top', 'top'), #상의
    ('bottom', 'bottom'), #하의
    ('outter', 'outter'), #아우터
    ('shose', 'shose'), #신발
    ('accessory', 'accessory'), #악세사리
  ]
  category = models.CharField(max_length=20, choices=CATEGORYS)
  buying = models.TextField(null=True, blank=True)
  
  def __str__(self):
    return f'{self.pk}: {self.category}'

# class Closet(models.Model):
  

class Post(models.Model):
  main_img = models.ImageField(upload_to='main/images/post/%Y/%m/%d')
  title = models.CharField(max_length=100)
  content = models.TextField()
  private = models.BooleanField(default=False)
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
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f'({self.author}) {self.post.title} :  {self.content}'
  
class Commu(models.Model):
  COMMU_CHOICES = [
    ('buying', 'buying'), #공동구매
    ('openrun', 'openrun'), #오픈런
    ('question', 'question'), #고민방
  ]
  category = models.CharField(max_length=20, choices=COMMU_CHOICES)
  img = models.ImageField(upload_to='main/images/commu/%Y/%m/%d', null=True, blank=True)
  title = models.CharField(max_length=100)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.pk}: {self.title}'
  
  def get_absolute_url(self):
    return f'/community/commu'