from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.post_list, name="post_list"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("category/<slug:slug>/", views.category_view, name="category"),
    path("tag/<slug:slug>/", views.tag_view, name="tag"),
    path("search/", views.search_view, name="search"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
