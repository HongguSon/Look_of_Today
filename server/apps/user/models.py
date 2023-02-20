from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Profile(models.Model):
  GENDERS = (
        ('남성', '남성'),
        ('여성', '여성'),
    )
  
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  profile_image = models.ImageField(null=True, blank=True, upload_to='user/images/profile/%Y/%m/%d')
  phone_num = PhoneNumberField(null=True, blank=True)
  height = models.IntegerField(null=True, blank=True)
  weight = models.IntegerField(null=True, blank=True)
  birth_date = models.DateField(null=True, blank=True)
  gender = models.CharField(verbose_name='성별', max_length=10, choices=GENDERS, null=True, blank=True)
  following = models.ManyToManyField(User, related_name='following', blank=True)
  
  def __str__(self):
    return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
      
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()

