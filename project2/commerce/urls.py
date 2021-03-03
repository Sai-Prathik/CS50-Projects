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
    path("listing/<str:name>",views.listing,name="listing")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
