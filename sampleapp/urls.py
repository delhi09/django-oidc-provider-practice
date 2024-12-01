from django.urls import path

from . import views

app_name = "sampleapp"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("authorize/", views.AuthorizeView.as_view(), name="authorize"),
    path(
        "consent/<str:authorization_token>/",
        views.ConsentView.as_view(),
        name="consent",
    ),
]
