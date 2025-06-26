
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
                
]

