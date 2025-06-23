from django.db import models
from django.contrib.auth.models import User

from django.db import models

class CustomerModels(models.Model):
     LIVE=1
     DELETE=0
     DELETE_CHOICE=((LIVE,'live'),(DELETE,'Delete'))
     name=models.CharField(max_length=100)
     address=models.CharField(max_length=200)
     image=models.ImageField(upload_to='media/userimage')
     user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='coustomer_profile')
     phone=models.CharField(default="none")
     delete_status=models.IntegerField(choices=DELETE_CHOICE,default=LIVE)
     created_at=models.DateTimeField(auto_created=True)
     updated_at=models.DateTimeField(auto_now=True)

     def __str__(self)->str:
          return self.name

