
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import seller_panel
from Customers.views import add_product  # or Sellers.views

from . import views
urlpatterns = [
        path('account', views.show_account,name='account'),
      
    path('logout/', views.user_logout, name='logout'),  # 👈 add this
    
  path('seller/', seller_panel, name='seller_panel'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/add-product/', add_product, name='add_product'),

]

