from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("create-new-page/", views.create_new_page, name="create-new-page"),
    path("<str:title>/", views.entry, name="entry"),
]
