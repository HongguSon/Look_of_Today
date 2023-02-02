from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  profile_image = models.ImageField(null=True, blank=True, upload_to='user/images/profile/%Y/%m/%d')
  # phone_num = PhoneNumberField(unique=True, null=True, blank=True)
  phone_num = models.IntegerField(unique=True, null=True, blank=True)
  height = models.FloatField(null=True, blank=True)
  weight = models.FloatField(null=True, blank=True)
  age = models.IntegerField(null=True, blank=True)
  birth_date = models.DateField(null=True, blank=True)
  following = models.ManyToManyField(User, related_name='following',null=True, blank=True)
  
  def __str__(self):
    return self.user.username