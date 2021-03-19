from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing",views.create_listing,name="new_listing"),
    path("listing/<str:name>",views.listing,name="listing"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("created_listings",views.personal_listing,name="personal_listings"),
    path("edit_details",views.edit,name="edit_details"),
    path("remove_from_watchlist",views.remove_from_watchlist,name="remove"),
    path("commit_bid",views.commit_bid,name="commit_bid"),
    path("post_comments",views.comments,name="comments"),
    path("categories",views.categories,name="categories"),
    path("category/<str:category>",views.cat,name="cat_products")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
