from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
  path("", views.community_main, name="community_main"),
  path("create",views.post_create,name="post_create")
]
