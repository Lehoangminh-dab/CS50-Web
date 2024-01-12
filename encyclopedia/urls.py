from django.urls import path

from . import views
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("random/", views.random_entry, name="random"),
    path("edit-page/<str:title>", views.edit_page, name="edit-page"),
    path("create-new-page/", views.create_new_page, name="create-new-page"),
    path("<str:title>/", views.entry, name="entry"),
]
