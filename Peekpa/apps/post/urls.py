from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.post_list_view, name="post_list"),
    path("detail/<int:time_id>/", views.detail, name="detail"),
]
