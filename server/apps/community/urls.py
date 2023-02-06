from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
  path("", views.community_main, name="community_main"),
  path("create/",views.PostCreate.as_view(),name="post_create"),
  # path("detail/<int:pk>/",views.post_detail,name="post_detail"),
  path('comment/', views.comment_ajax, name='comment'),
  path("update/<int:pk>/", views.PostUpdate.as_view(), name='update'),
  path("delete/<int:pk>/", views.post_delete,name='delete'),
  path("likes/<int:pk>/", views.post_likes, name='likes'),
  # path("create",views.PostCreate.as_view(),name="post_create"),
  # path("<int:pk>", views.detail, name='detail'),
]
