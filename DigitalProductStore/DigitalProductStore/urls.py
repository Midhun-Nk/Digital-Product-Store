
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Products.urls'),),
     path('Customer/',include('Customers.urls')),
      path('Orders/',include('Orders.urls')),
            path('Seller/',include('Seller.urls')),

   
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)