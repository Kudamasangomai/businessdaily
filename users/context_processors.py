
from company.models import company,product,customer_order
from django.contrib.auth.models import User 

 
def profile(request,**kwargs):  

    logged_as_company = company.objects.all() 
    return {'logged_as_company':logged_as_company}

def total_products(request,**kwargs):  
     total = product.objects.filter(postedbyuser = request.user.id).count()
     company_orders = customer_order.objects.filter(companyname = company.id ).count()
     pending_payments = customer_order.objects.filter(companyname = request.user.id).count()
     total_company = company.objects.filter(company_name__isnull= False).count()

     return {
         
         'totalproducts':total,
        'company':company_orders ,
         'pending_payments':pending_payments,
         'total_company':  total_company
         }

def getcompanyname(request,**kwargs):

    mycompanyname = company.objects.get(companyid = request.user.id) 
    return {'mycompanyname':mycompanyname}