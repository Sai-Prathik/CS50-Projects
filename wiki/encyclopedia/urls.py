from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/",views.entry,name="get_entry"),
    path("search/",views.search_item,name="search"),
    path("new_entry/",views.new_entry,name="new_entry")
     
]
