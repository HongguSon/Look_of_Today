from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

class PostAdmin(admin.ModelAdmin):
  def get_form(self, request, obj=None, **kwargs):
    form = super(PostAdmin, self).get_form(request, obj, **kwargs)
    form.base_fields['outer'].queryset = Outer.objects.filter(author=request.user)
    form.base_fields['top'].queryset = Top.objects.filter(author=request.user)
    form.base_fields['bottom'].queryset = Bottom.objects.filter(author=request.user)
    form.base_fields['shoes'].queryset = Shoes.objects.filter(author=request.user)
    form.base_fields['acc'].queryset = Acc.objects.filter(author=request.user)
    return form

admin.site.register(Post, PostAdmin)
admin.site.register(PostComment)
admin.site.register(Talk)
admin.site.register(TalkComment)

class ClothesAdmin(admin.ModelAdmin):
  def thumbnail(self, object):
    return format_html('<img src="{}" width="30">'.format(object.rem_img.url))
  thumbnail.short_description = "rem_img"
  list_display = ('author', 'thumbnail', 'img')

admin.site.register(Clothes, ClothesAdmin)
admin.site.register(Top)
admin.site.register(Bottom)
admin.site.register(Shoes)
admin.site.register(Acc)
admin.site.register(Outer)


