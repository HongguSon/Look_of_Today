from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Talk)
admin.site.register(TalkComment)

class ClothesAdmin(admin.ModelAdmin):
  def thumbnail(self, object):
    return format_html('<img src="{}" width="30">'.format(object.rem_img.url))
  thumbnail.short_description = "rem_img"
  list_display = ('title', 'author', 'thumbnail', 'buying', 'img')

admin.site.register(Clothes,  ClothesAdmin)
admin.site.register(Top)
admin.site.register(Bottom)
admin.site.register(Shoes)
admin.site.register(Acc)
admin.site.register(Outer)


