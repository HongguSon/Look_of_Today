from django.urls import path
from . import views

app_name = "closet"

urlpatterns = [
  path("", views.closet_main, name="closet_main"),
  path("our_closet/", views.our_closet, name="our_closet"),
  path("2/", views.closet_main2, name="closet_main2"),
  path("create/top/",views.TopCreate.as_view(),name="top_create"),
  path("create/bottom/",views.BottomCreate.as_view(),name="bottom_create"),
  path("create/outer/",views.OuterCreate.as_view(),name="outer_create"),
  path("create/acc/",views.AccCreate.as_view(),name="acc_create"),
  path("create/shoes/",views.ShoesCreate.as_view(),name="shoes_create"),
]