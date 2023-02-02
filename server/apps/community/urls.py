from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
  path("", views.community_main, name="community_main"),
  path("<int:pk>/update", views.update, name='update'),
  path("<int:pk>/delete", views.delete,name='delete'),
  path("<int:pk>/likes/", views.likes, name='likes'),
  path("create",views.PostCreate.as_view(),name="post_create")
  path("<int:pk>", views.detail, name='detail'),
]
