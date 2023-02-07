from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
  path("", views.community_main, name="community_main"),
  path("talk_create/",views.TalkCreate.as_view(),name="talk_create"),
  path("talk_delete/<int:pk>/", views.talk_delete,name='talk_delete'),
  path("talk_detail/<int:pk>/",views.talk_detail,name="talk_detail"),
  path('comment_talk/', views.comment_talk_ajax, name='talk_comment'),
  path("talk_likes/<int:pk>/", views.talk_likes, name='talk_likes'), 
  path("talk_update/<int:pk>/", views.TalkUpdate.as_view(), name='talk_update'),
  
  path("openrun/", views.openrun, name='openrun'),
  path("other/", views.other, name='other'),
  path("buying/", views.buying, name='buying'),

]
