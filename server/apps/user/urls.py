from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
  path("signup/", views.signup, name="signup"),
  path("logout/", views.logout, name="logout"),
<<<<<<< Updated upstream
  path("login/", views.log_in, name="login"),
=======
  path("profile_update/", views.profile_update, name="profile_update"),
>>>>>>> Stashed changes
]