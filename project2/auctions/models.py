from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime 
# Create your models here.
DEFAULT_USER_ID=0
CATEGORIES=[("F","Fashion"),("T","Toys"),("E","Electronics"),("H","Home"),("A","Antique"),("O","Wine")]
class Localuser(AbstractUser):
     pass

class Listings(models.Model):
     item_name=models.CharField(max_length=20,default="Item")
     item_description=models.TextField(max_length=10000,default="No Description")
     bid_price=models.FloatField(default=0.0)
      
     category=models.CharField(choices=CATEGORIES,max_length=10,default="NAN")
     end_date=models.DateTimeField(blank=True)
     created_time=models.DateTimeField(auto_now_add=True)
     created_by=models.ForeignKey(Localuser,on_delete=models.CASCADE,null=True,related_name="creator")
     img_url=models.CharField(default="No Image",max_length=10000)
     current_price=models.FloatField(default=0.0)
     item_active=models.BooleanField(default=True)

     def end_list(self):
          obj=Listings.objects.filter(id=self.id)
          print(self)
          obj.update(item_active=False)
          return "/created_listings"
     def get_date(self):
          return self.created_time.date()
     def get_end_date(self):
          return self.end_date.date()
     def get_now(self):
          return datetime.now()
     def get_category(self):
          for i in CATEGORIES:
               if i[0]==self.category:
                    return i[1]
     #updated_on=models.DateField(auto_now=True,default=now)
class Watchlist(models.Model):
      
     user=models.ForeignKey(Localuser,on_delete=models.CASCADE,related_name="user")
     item=models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="item")   
     count=models.IntegerField(default=1)
     
class Bid(models.Model):
     user=models.ForeignKey(Localuser,on_delete=models.CASCADE)
     bid_price=models.FloatField(default=0.0)
     list_item=models.ForeignKey(Listings,on_delete=models.CASCADE)

class Comments(models.Model):
     user=models.ForeignKey(Localuser,on_delete=models.CASCADE)
     item=models.ForeignKey(Listings,on_delete=models.CASCADE)
     comments=models.TextField(max_length=100000,default="No Comments")
     like=models.BooleanField(default=False)