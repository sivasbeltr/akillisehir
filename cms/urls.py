from django.urls import path

from . import views

app_name = "cms"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("iletisim/", views.ContactView.as_view(), name="contact"),
    path(
        "iletisim/basarili/",
        views.ContactSuccessView.as_view(),
        name="contact_success",
    ),
    path(
        "proje-onerisi/",
        views.ProjectSuggestionView.as_view(),
        name="project_suggestion",
    ),
    path(
        "proje-onerisi/basarili/",
        views.ProjectSuggestionSuccessView.as_view(),
        name="project_suggestion_success",
    ),
    path("ekibimiz/", views.StaffView.as_view(), name="staff"),
    path("ekibimiz/<int:staff_id>/", views.staff_detail_ajax, name="staff_detail_ajax"),
]
