from django.db import models
from Customers.models import CustomerModels
from Products.models import ProductModels

class Order(models.Model):
    # Soft Delete Choices
    LIVE = 1
    DELETE = 0
    DELETE_CHOICE = (
        (LIVE, 'Live'),
        (DELETE, 'Delete'),
    )

    # Order Status Choices
    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4
    STATUS_CHOICE = (
        (CART_STAGE, 'Cart Stage'),
        (ORDER_CONFIRMED, 'Order Confirmed'),
        (ORDER_PROCESSED, 'Order Processed'),
        (ORDER_DELIVERED, 'Order Delivered'),
        (ORDER_REJECTED, 'Order Rejected'),
    )

    order_status = models.IntegerField(choices=STATUS_CHOICE, default=CART_STAGE)
    owner = models.ForeignKey(CustomerModels, on_delete=models.SET_NULL, null=True, related_name='orders')
    delete_status = models.IntegerField(choices=DELETE_CHOICE, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)  # Corrected this line
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - Status: {self.get_order_status_display()}"


class OrderItem(models.Model):
    product = models.ForeignKey(ProductModels, related_name='added_carts', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    owner = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_items')

    def __str__(self):
        return f"{self.quantity} x {self.product.title if self.product else 'Unknown Product'}"
