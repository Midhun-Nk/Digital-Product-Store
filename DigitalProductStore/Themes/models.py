from django.db import models

class SiteSettings(models.Model):
     image=models.ImageField(upload_to='media/banner/')
     caption=models.TextField()
