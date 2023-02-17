from django.urls import path
from . import views

app_name = "closet"

urlpatterns = [
  path("", views.closet_main, name="closet_main"),
  path("all/", views.closet_all, name="closet_all"),
  path("our-closet/", views.our_closet, name="our_closet"),
  # REVIEW : 아래 리스트 함수 5개는 모델만 다르지, 로직은 모두 동일
  # REVIEW : 따로 model 변수를 입력받아 함수 통일해 코드 중복 제거 가능
  # path("<slug:Clothes>/", views.clothes_list, name="clothes_list"),
  path("outer/", views.outer_list, name="outer_list"),
  path("top/", views.top_list, name="top_list"),
  path("bottom/", views.bottom_list, name="bottom_list"),
  path("shoes/", views.shoes_list, name="shoes_list"),
  path("acc/", views.acc_list, name="acc_list"),
  path("create/clothes/",views.create_clothes,name="clothes_create"),
  # path("delete/clothes/<int:pk>/",views.create_clothes,name="clothes_create"),
  # path("detail/clothes/<int:pk>/",views.create_clothes,name="clothes_create"),
  path("clothes-likes/<int:pk>/", views.clothes_likes, name='clothes_likes'),
  path("clothes-like-list/", views.clothes_like_list, name='clothes_like_list'),
  path("post-like-list/", views.post_like_list, name='post_like_list'),
]
