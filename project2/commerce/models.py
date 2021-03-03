from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime 
# Create your models here.
CATEGORIES=[("F","Fashion"),("T","Toys"),("E","Electronics"),("H","Home"),("A","Antique")]
class Localuser(AbstractUser):
     pass

class listings(models.Model):
     item_name=models.CharField(max_length=20,default="Item")
     item_description=models.TextField(max_length=100,default="No Description")
     bid_price=models.FloatField(default=0.0)
     img=models.ImageField(upload_to="images/")
     category=models.CharField(choices=CATEGORIES,max_length=10,default="NAN")
     end_date=models.DateTimeField(blank=True)
     created_time=models.DateTimeField(auto_now_add=True)
     
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
     