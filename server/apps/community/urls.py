from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
  path("", views.community_main, name="community_main"),
  path("create",views.post_create,name="post_create"),
  path("<int:pk>", views.detail, name='detail'),
  path("<int:pk>/update", views.update, name='update'),
  path("<int:pk>/delete", views.delete,name='delete'),
]
