from django.urls import path
from . import views

app_name = "closet"

urlpatterns = [
  path("", views.closet_main, name="closet_main"),
  path("2/", views.closet_main2, name="closet_main2"),
  path("outer/", views.outer_list, name="outer_list"),
  path("top/", views.top_list, name="top_list"),
  path("bottom/", views.bottom_list, name="bottom_list"),
  path("shoes/", views.shoes_list, name="shoes_list"),
  path("acc/", views.acc_list, name="acc_list"),
  # path("Post_create/",views.PostCreate.as_view(),name="post_create"),
  # path("create/",views.ClothesCreate.as_view(),name="clothes_create"),
  path("outer_create/",views.OuterCreate.as_view(),name="outer_create"),
]