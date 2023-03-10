from django.urls import path
from . import views
from server.apps.closet.views import *

app_name = "community"

urlpatterns = [
  # REVIEW : REST한 CRUD 추천
  path("", views.community_main, name="community_main"),
  path("openrun/", views.openrun, name='openrun'),
  path("other/", views.other, name='other'),
  path("buying/", views.buying, name='buying'),
  
  path("create/",views.post_create,name="post_create"),
  path("create/<int:pk>",views.post_create_img,name="post_create_img"),
  path("detail/<int:pk>/",views.post_detail,name="post_detail"),
  path('comment/', views.comment_ajax, name='comment'),
  path('delete-comment/<int:pk>/', views.delete_pcomment, name='delete_comment'),
  path("delete/<int:pk>/", views.post_delete,name='delete'),
  path("likes/<int:pk>/", views.post_likes, name='likes'),
  
  path("talk-create/",views.talk_create,name="talk_create"),
  path("talk-create/<int:pk>",views.talk_create_img,name="talk_create_img"),
  path("talk-detail/<int:pk>/",views.talk_detail,name="talk_detail"),
  path('talk-comment/', views.comment_talk_ajax, name='talk_comment'),
  path('delete-tcomment/<int:pk>/', views.delete_tcomment, name='delete_tcomment'),
  path("talk-update/<int:pk>/", views.talk_update, name='talk_update'),
  path("talk-delete/<int:pk>/", views.talk_delete,name='talk_delete'),
  path("talk-likes/<int:pk>/", views.talk_likes, name='talk_likes'),

]