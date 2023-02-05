from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_user")
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
      
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()

