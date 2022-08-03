from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("movie/<int:key_id>/", views.movie),
    path("tv/<int:key_id>/", views.tv),
    path("artist/<int:key_id>/", views.artist),
    path("search", views.search),
    path("wishlist", views.wishlist),
]