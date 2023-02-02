from django.urls import path
from . import views

app_name = "closet"

urlpatterns = [
  path("", views.closet_main, name="closet_main"),
]
