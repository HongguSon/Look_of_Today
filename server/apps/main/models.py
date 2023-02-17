from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from rembg import remove
from PIL import Image,ImageOps,ImageFilter
from io import BytesIO
import sys
import os.path
from django.utils.html import format_html


# Create your models here.

# REVIEW : 각 모델의 속성이 많이 중복되므로, BaseClass 추상화시 코드 중복 제거 가능
class Clothes(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  img = models.ImageField(upload_to='main/images/clothes/%Y/%m/%d')
  title = models.CharField(max_length=100)
  likes = models.ManyToManyField(User, related_name = "%(class)sLike", blank=True)
  buying = models.TextField(null=True, blank=True)
  rem_img = models.ImageField(upload_to='main/images/remclothes/%Y/%m/%d', null=True, blank=True)
  
  def thumbnail(self):
    return format_html('<img src="{}" width="100">'.format(self.rem_img.url))
  
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return f'/closet/'
  
  def save(self, *args, **kwargs):
    self.remove_img()
    super(Clothes, self).save(*args, **kwargs)
    
  def remove_img(self, *args, **kwargs):
    image_converted = convert_test(self.img)
    self.rem_img = InMemoryUploadedFile(file=image_converted, field_name="ImageField", name=self.img.name,
                                                content_type='image/jpeg', size=sys.getsizeof(image_converted), charset=None)
        
def convert_test(img):
  img = Image.open(img)
  output = remove(img)
  img = output.convert('RGBA')
  img = img.resize((300, 300), Image.ANTIALIAS)
  return image_to_bytes(img)

def image_to_bytes(img):
  output = BytesIO()
  img.save(output, format='PNG')
  output.seek(0)
  return output

class Top(Clothes):
  pass

class Bottom(Clothes):
  pass

class Outer(Clothes):
  pass

class Shoes(Clothes):
  pass

class Acc(Clothes):
  pass


class Post(models.Model):
  main_img = models.ImageField(upload_to='main/images/post/%Y/%m/%d')
  title = models.CharField(max_length=100)
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  top = models.ManyToManyField(Top, related_name='Top', blank=True)
  bottom = models.ManyToManyField(Bottom,  related_name='Bottom', blank=True)
  acc = models.ManyToManyField(Acc, related_name='Acc', blank=True)
  outer = models.ManyToManyField(Outer, related_name='Outer', blank=True)
  shoes = models.ManyToManyField(Shoes, related_name='Shoes', blank=True)

  likes = models.ManyToManyField(User, related_name='Likes', blank=True)
  open = models.BooleanField(default=False)

  def __str__(self):
    return f'{self.pk}: {self.title}'

  def get_absolute_url(self):
    return f'/community/detail/{self.pk}/'
  #이거 나중에 detail page로 바꿔주세요

class Talk(models.Model):
  Talk_CHOICES = (
    ('공동 구매', '공동 구매'), #공동구매
    ('오픈런', '오픈런'), #오픈런
    ('잡담방', '잡담방'), #고민방
  )
  category = models.CharField(max_length=10 ,choices=Talk_CHOICES)
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
    return f'/community/talk-detail/{self.pk}/'

class Comment(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  
class PostComment(Comment):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'({self.author}) {self.post.title} :  {self.content}'

class TalkComment(Comment):
  talk = models.ForeignKey(Talk, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'({self.author}) {self.talk.title} :  {self.content}'