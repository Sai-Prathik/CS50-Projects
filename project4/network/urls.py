
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/",views.set_posts,name="set_posts"),
    path("get_posts/<str:type>",views.get_posts,name="get_posts"),
    path("get_profile/<str:username>",views.get_user_posts,name="get_user_posts"),
    path("get_user_profile/<str:username>",views.get_user,name="get_user"),
    path("follow/<int:user_id>/<str:type>",views.follow,name="follow"),
    path("like_posts/<int:post_id>/<str:type>",views.like_post,name="like_post"),
    path("edit_post/",views.edit_post,name="edit_post")
]
    