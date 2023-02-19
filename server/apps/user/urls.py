from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
  path("signup/", views.signup, name="signup"),
  path("logout/", views.logout, name="logout"),
  path("login/", views.log_in, name="login"),
  path("profile_update/", views.profile_update, name="profile_update"),
  path("mypage/", views.mypage, name="mypage"),
  path("mypage/update", views.mypage_update, name="mypage_update"),
  path("mypage/update/profile_img/<int:pk>", views.profile_img_mod, name="profile_img_mod"),
]
