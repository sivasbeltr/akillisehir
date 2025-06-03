from django.urls import path

from . import views

app_name = "fileman"

urlpatterns = [
    path("", views.file_list, name="file_list"),
]
