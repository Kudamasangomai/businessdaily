from django.urls import path
from . import views

from .views import (
  companies,
  deleteproductview,
  productsview,
  company_approve,
  totalsales,
  companysales
) 



urlpatterns = [
  path('register_company/',views.register_company,name='register-company'),
  path('companies/',companies.as_view(),name='companies'),
  path('company_edit/<companyid>',views.company_edit,name="company-edit"),
  path('payment/',views.payment,name='payment'),
  path('payment-succes/',views.payment,name='payment-success'),
  path('submitpay/<int:pk>',views.submit_pay,name='submit-pay'),
  path('deleteproduct/<int:pk>',deleteproductview.as_view(),name="delete-cart-product"),
  path('searched_product',views.searched_product,name="searched-product"),
  path('product/<int:pk>',productsview.as_view(),name='products'),
  path('edit-product/<int:pk>',views.edit_product,name='edit-product'),
  path('company_approve/<int:pk>',company_approve.as_view(),name='company-approve'),
  path('totalsales',totalsales.as_view(),name='total-sales'),
  path('companysales/<userid>',companysales.as_view(),name='company-sales'),
  #path('companysales/<userid>',view.companysales,name='company-sales'),  

  path('export_csv/',views.export_csv,name="export-csv"),
  path('export_pdf/',views.export_pdf,name="export-pdf"),
  


  
 
]

