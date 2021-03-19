from django.contrib import admin
from . models import Localuser,Listings,Watchlist,Bid,Comments
# Register your models here.

admin.site.register(Localuser)
admin.site.register(Listings)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comments)