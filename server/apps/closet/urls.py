from django.urls import path
from . import views

app_name = "closet"

urlpatterns = [
  path("", views.closet_main, name="closet_main"),
  path("2/", views.closet_main2, name="closet_main2"),
  # path("Post_create/",views.PostCreate.as_view(),name="post_create"),
  path("create/",views.ClothesCreate.as_view(),name="clothes_create"),
]