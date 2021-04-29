from django.contrib.auth.models import AbstractUser
from django.db import models
import json
from django.http import request
class User(AbstractUser):
    pass
    
    def serialize(self,user=None):
        obj=Follows()
         

        
        return{
            "id":self.id,
            "username":self.username,
            "date_joined":self.date_joined,
            "followers":Follows.get_followers_count(obj,self.id)[0],
            "following":Follows.get_followers_count(obj,self.id)[1],
            "relation":Follows.get_relation(obj,self.id,user)
        }

class Posts(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     post=models.TextField(default="No Post")
     time_stamp=models.DateTimeField(auto_now=True)
     likes=models.ManyToManyField(User,related_name="likes")

     def serialize(self,id,name=None):   

         if len(self.likes.filter(username=id))==0:
             relation=False
         else:
             relation=True
          
         return{
             "id":self.id,
             "author":self.user.username,
             "post":self.post,
             "time_stamp":self.time_stamp.strftime("%b %d %Y, %I:%M %p"),
             "relation":relation,
             "likes":len(self.likes.all())
              }
      

class Follows(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User")
     follower=models.ManyToManyField(User,related_name="follower")

     def get_followers_count(self,user):
       obj=Follows.objects.filter(user=user)
       obj1=Follows.objects.filter(follower=user)
       return (len(obj),len(obj1))
    
     def get_relation(self,user,follower):
         if len(Follows.objects.filter(user=user,follower=follower))==0:
             return False
         else:
             return True
    
     def seriliaze(self):
         pass
      
