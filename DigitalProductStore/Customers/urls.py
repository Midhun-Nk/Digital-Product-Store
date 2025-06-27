
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


from . import views
urlpatterns = [
        path('account', views.show_account,name='account'),
      
    path('logout/', views.user_logout, name='logout'),  # 👈 add this
    path('about/', views.about_page, name='about'),
path('contact/', views.contact_page, name='contact'),

    

]

