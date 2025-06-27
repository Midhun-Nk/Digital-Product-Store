
from django.db import models
from django.contrib.auth.models import User

class SellerModels(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICE = (
        (LIVE, 'Live'),
        (DELETE, 'Delete'),
    )

    shop_name = models.CharField(max_length=100)
    shop_address = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    phone = models.CharField(max_length=20, default="none")
    image = models.ImageField(upload_to='media/sellerimage', blank=True, null=True)
    delete_status = models.IntegerField(choices=DELETE_CHOICE, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.shop_name
