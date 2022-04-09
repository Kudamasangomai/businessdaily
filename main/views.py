from django.shortcuts import render ,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from users.forms import productform
from company.models import company ,product ,customer_order
from django.contrib import messages
from django.views.generic import ListView,DetailView,FormView,UpdateView ,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from main.models import salestable
from company.models import comments
from .mixins import Directions
from django.contrib.auth.models import User 

# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        
               
        form = productform(request.POST,request.FILES)
        companygetid = company.objects.get(companyid = request.user.id)  
        user = User.objects.get(id=request.user.id)   
        
        print(form)
        print(form.errors)
        if form.is_valid():
            
            print('valid')
            
            a = form.save(commit=False)
            a.postedbyuser = request.user
            a.companyid = companygetid
            a.save()
            messages.success(request,f'Product Successfully Added')
            #return render(request ,'main/home.html',{'form':form}) 
            return redirect('home')
            
        
        else:
            
            messages.warning(request,f'Error Somewhere')
            return redirect('home')
                 
    else:
      
        context={
                'form' : productform(),   
                #'userinfo' : company.objects.get(companyid = request.user.id),
               # 'userinfolog' : User.objects.get(id = request.user.id),
                'product':product.objects.all(),
                'company':company.objects.all(),
                'title':'Home'
                }         
    
        return render(request ,'main/home.html',context)
     



class UpdateproductView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    
    model = product
    context_object_name = "product"
    fields ="__all__"
    success_message = "Product Successfully Updated"


    def get_success_url(self):
        return reverse_lazy('Update-product', kwargs={'pk': self.object.pk})
    

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        

        userqty = request.POST['qty']
        userqtya = request.POST.get('qty')

        #getcompid = company.objects.get(companyid = request.POST['companyname'])
        productqty = product.objects.get(id =request.POST['pid']) 
        productqty.product_quantity = productqty.product_quantity - int(userqty)
        order = customer_order()
        sales = salestable()

        order.productid = request.POST['pid']
        order.productname = request.POST['pname']
        order.productprice = request.POST['pprice']
        order.customer_id_id = request.user.id  
        order.companyname = request.POST['companyname']
        order.totalprice =  int(order.productprice) * int(userqtya)
        order.productqty = userqty
        #print(order.totalprice)
        sales.productid = request.POST['pid']
        sales.productname = request.POST['pname']
        sales.productprice = request.POST['pprice']
        sales.customer_id_id = request.user.id  
        #sales.companyname = getcompid.id
        sales.companyname = request.POST['companyname']
        sales.totalprice =  int(order.productprice) * int(userqtya)
        sales.productqty = userqty

        
        order.save()
        productqty.save()
        sales.save()
        #print(getcompid.id)
        messages.success(request,f'Product Successfully Added to Cart')
        return redirect('home')
    


@login_required
def open_product(request,productid):
    
    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "product_details" : product.objects.get(id = productid),
        'comments' : comments.objects.filter(product_id = productid),
        
        }

    
    product_details = product.objects.get(id = productid)
    return render(request,'main/open-product.html',context)
    
'''
def route(request):
    
	context = {"google_api_key": settings.GOOGLE_API_KEY}
	return render(request, 'main/open-product.html', context)
'''

'''
Basic view for displaying a map 
'''



def add_product_comment(request):
    
    
    if request.method == "POST":
       
        
        usercomment = comments()
        usercomment.product = product.objects.get(id =request.POST['prodid']) 
        usercomment.comments = request.POST.get('comment')
        usercomment.postedbyuser = request.user

        usercomment.save()
        return redirect('home')
            



        


        

def map(request):

	lat_a = request.GET.get("lat_a")
	long_a = request.GET.get("long_a")
	lat_b = request.GET.get("lat_b")
	long_b = request.GET.get("long_b")
	directions = Directions(
		lat_a= lat_a,
		long_a=long_a,
		lat_b = lat_b,
		long_b=long_b
		)

	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"lat_a": lat_a,
	"long_a": long_a,
	"lat_b": lat_b,
	"long_b": long_b,
	"origin": f'{lat_a}, {long_a}',
	"destination": f'{lat_b}, {long_b}',
	"directions": directions,

	}
	return render(request, 'main/map.html', context)

    
    
 
   






