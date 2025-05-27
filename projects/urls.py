from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("<slug:slug>/yazdir/", views.project_print_view, name="project_print"),
]
