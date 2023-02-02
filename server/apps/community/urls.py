from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
  path("", views.community_main, name="community_main"),
  path("create",views.PostCreate.as_view(),name="post_create")
]
