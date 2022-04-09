from django.urls import path 
from . import views

from .views import (

UpdateproductView
) 

urlpatterns = [


    path('home/', views.home,name='home'),
    path('addtocart/',views.add_to_cart,name='add-to-cart'),
    path('openproduct/<productid>',views.open_product,name='open-product'),
    path('update_product/<int:pk>',UpdateproductView.as_view(),name='Update-product'),
    path('add_product_comment/',views.add_product_comment,name='add-product-comment')
    
   
  #  path('login/' ,views.logout, name= 'logout')


]
