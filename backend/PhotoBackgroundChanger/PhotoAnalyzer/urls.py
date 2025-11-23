from django.urls import path
from . import views


urlpatterns = [
    path("add-photo/", views.add_photo.as_view(), name="add_photo"),
    path("remove-photo/", views.remove_photo.as_view(), name="remove_photo"),
    path("generate-background/", views.generate_background.as_view(),
         name="generate_background"),
]
