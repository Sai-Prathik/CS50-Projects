from django.contrib import admin
from . models import Localuser,Listings,Watchlist
# Register your models here.

admin.site.register(Localuser)
admin.site.register(Listings)
admin.site.register(Watchlist)