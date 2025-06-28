
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import seller_panel
from Seller.views import add_product  # or Sellers.views
from .views import view_seller_products
from . import views

from . import views
urlpatterns = [
   

  path('', seller_panel, name='seller_panel'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/add-product/', add_product, name='add_product'),
        path('view-products/', view_seller_products, name='view_seller_products'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('track-orders/', views.track_orders, name='track_orders'),  # 👈 New
    path('settings/', views.seller_settings, name='seller_settings'),  # 👈 New
     path('pending-orders/', views.view_pending_orders, name='view_pending_orders'),
    path('confirm-order/<int:order_id>/', views.approve_order, name='approve_order'),
    path('seller/orders/reject/<int:order_id>/', views.reject_order, name='reject_order'),

]
