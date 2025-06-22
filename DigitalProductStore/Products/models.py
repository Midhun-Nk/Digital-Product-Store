from django.db import models

class ProductModels(models.Model):
     LIVE=1
     DELETE=0
     DELETE_CHOICE=((LIVE,'live'),(DELETE,'Delete'))
     title=models.CharField(max_length=100)
     price=models.FloatField()
     description=models.CharField(max_length=200)
     image=models.ImageField(upload_to='media/productimage')
     category=models.CharField(max_length=100)
     priority=models.IntegerField(default=0)
     delete_status=models.IntegerField(choices=DELETE_CHOICE,default=LIVE)
     created_at=models.DateTimeField(auto_created=True)
     updated_at=models.DateTimeField(auto_now=True)

     def __str__(self)->str:
          return self.title

