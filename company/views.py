from django.shortcuts import render,redirect,get_list_or_404, get_object_or_404,HttpResponse
from users.forms import companyregistration
from django import forms
from users.forms import CompanyUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import company ,customer_order ,product
from main.models import salestable
from django.contrib.auth.models import User 
from django.views.generic import ListView,DetailView,FormView,UpdateView ,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from paynow import Paynow
import time
from django.db.models import Sum
from django.urls import reverse
from django.urls import reverse_lazy
from django.db.models import Q ,Count
from datetime import datetime ,timedelta
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.urls import reverse
import io
import csv
from django.conf import settings
from django.core.mail import send_mail
from businessdaily.settings import EMAIL_HOST_USER
import time


# Create your views here.
@login_required
def register_company(request):
    

    if request.method == 'POST':
        
        #cid = request.POST.get('companyid')
        form = companyregistration(request.POST)
        cid = User.objects.get(id = request.POST.get('companyid'))
        usermodel = User()
       

        if form.is_valid(): 
            if cid.id == request.user.id:                
                #subject = "New Company registration"
                #message ="Please Activate the follwing New Company"
                #recipient_list = ['masboyk@gmail.com']
                #send_mail(subject, message, EMAIL_HOST_USER,recipient_list,fail_silently=False)
                form.save()
                messages.success(request,f'Company Successfully Registered')
                return redirect('home')    
           
                       

    else:
        form = companyregistration()
    return render(request,'company/register-company.html',{'form':form})

class companies(LoginRequiredMixin,ListView):
    model = company
    template_name = 'company/companies.html'
    context_object_name = 'companies'



@login_required
def company_edit(request,companyid):
    print(companyid)
    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST)
        comp = company.objects.get(companyid = companyid)
        comp.approved = 'Approved'
        

        if form.is_valid():
            form.cleaned_data['email']
            form.save()
            comp.save()
            messages.success(request,f'Your profile has been updated')
            return redirect('companies')
    else:
        a = User.objects.get(id= companyid)  
        b = company.objects.get( companyid = companyid )    
        
        context ={
            'form':CompanyUpdateForm(instance = a),
            'companyname':b

        }
        return render(request,'company/company-edit.html',context)
@login_required
def submit_pay(request,**kwargs):
    #print(request.user.id)
    usercartinfo = customer_order.objects.filter(customer_id = request.user.id)
    #total = customer_order.objects.filter(customer_id = request.user.id).aggregate(total_price=Sum('productprice'))
    total = customer_order.objects.filter(customer_id = request.user.id).aggregate(total_price=Sum('totalprice'))
    totalprice = customer_order.objects.filter(customer_id = request.user.id)
    return render(request,'company/submitpay.html',{
        'usercartinfo':usercartinfo,
        'total':total,
        'fulltotalprice':totalprice,
        'today' : timezone.now() })   
'''
def payment(request):
    

    timeout = 10
    retries = 0
    sleep_time = 10
    returnUrl ='http://google.com'
    returnUrl ='http://google.com'

    paynow = Paynow(
    '13396',
    'af269a2d-c734-4a6a-aa2a-c96aa73fb4d3',
    returnUrl,
    returnUrl
    )
    payment = paynow.create_payment('Order', 'test@example.com')
    payment.add('Payment for stuff', 1)
    response = paynow.send_mobile(payment, '0778548832', 'ecocash')


    if(response.success):
        poll_url = response.poll_url
        print("Poll Url: ", poll_url)

        while retries < timeout:
            time.sleep(sleep_time)
            status = paynow.check_transaction_status(poll_url)

            if status.paid :
                print('Yay! Transaction was paid for. Update transaction')
                redirect_to = request.POST.get('next', request.user.id)
                messages.success(request, f'Transaction Was Succesfull')
                return redirect('submit-pay', redirect_to)
            else:
                redirect_to = request.POST.get('next', request.user.id)
                messages.warning(request, f'Transaction Fail please try again')
                return redirect('submit-pay', redirect_to)
                  
        retries = retries + 1
    
    # Timeout reached here'''


@login_required
def payment(request): 
    timeout = 10
    retries = 0
    sleep_time = 10

    if request.method == 'POST':
        usern = request.POST.get('ecocashnumber')
        amount =float( request.POST.get('amount'))
        returnUrl ='http://google.com'
        returnUrl ='http://google.com'
        #print(usern)
        paynow = Paynow(
           
            'id',
            'key',
            returnUrl,
            returnUrl
            )
        
        payment = paynow.create_payment('Order', 'masboyk@gmail.com')
        payment.add('Payment for stuff', amount )
        response = paynow.send_mobile(payment, usern, 'ecocash')
        
        
       
        if(response.success):            
            poll_url = response.poll_url
            print("Poll Url: ", poll_url)

        while retries < timeout:
            time.sleep(sleep_time)
            status = paynow.check_transaction_status(poll_url)

            if status.paid :
                #print('Yay! Transaction was paid for. Update transaction')
                #redirect_to = request.POST.get('next', request.user.id)
                messages.success(request, f'Transaction Was Succesfull')
                #return redirect('submit-pay', redirect_to)
                context = {
                    'paid' : status.paid
                }
                return render(request,'company/payment-success.html',context)
            else:
                print(status.paid)
                redirect_to = request.POST.get('next', request.user.id)
                messages.warning(request, f'Transaction Fail please try again')
                return redirect('submit-pay', redirect_to)
                  
        retries = retries + 1



class company_approve(LoginRequiredMixin,UpdateView):
    model = company


class deleteproductview(LoginRequiredMixin,DeleteView):
	model =customer_order
	success_url= reverse_lazy('home')
	success_message = "Product Successfully Deleted"

 
        
    

@login_required
def searched_product(request,**kwargs):
    
  
	if request.method == 'POST':
		searchedq = request.POST.get('searchproduct')
		searchedproduct = product.objects.filter(
			Q(product_name__contains = searchedq) |
			Q(product_category__contains = searchedq) |
			Q(product_info__contains = searchedq)
			)
		return render(request,'main/searched_products.html',{'searchedproduct':searchedproduct})
	else:
		return render(request,'main/home.html')

class productsview(LoginRequiredMixin,ListView):
    model = product
    template_name = 'product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self,**kwargs):
        queryset = super(productsview, self).get_queryset()
        queryset = product.objects.filter(postedbyuser_id = self.request.user.id)
        total_products = product.objects.count()
        return queryset

class totalsales(LoginRequiredMixin, ListView):
    model = salestable
    template_name = 'main/sales-table.html'
    context_object_name = 'sales'

'''    def get_queryset(self,**kwargs):
        getcompdata = company()
        queryset = super(totalsales,self).get_queryset()
        queryset = salestable.objects.filter(companyname = getcompdata.id)
        return queryset
'''

class companysales(LoginRequiredMixin,ListView):
    model = salestable
    template_name = 'company/companysales.html'
    context_object_name = 'companysales'

    



    



@login_required
def edit_product(request,**kwargs):
    print('working')



@login_required
def export_csv(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition']=  'attachment; filename=products.csv'
	writer =csv.writer(response)
	writer.writerow(['product Name','price','product_category','product_category',
    'product_info'])
	objbooks = product.objects.all()

	for objb in objbooks:
		writer.writerow([
            objb.product_name,objb.product_price ,    
            objb. product_quantity,
            objb.product_category,
            objb.product_info,
           
                  
            ]),
	return response

@login_required
def export_pdf(request):
	buf = io.BytesIO()
	c = canvas.Canvas(buf,pagesize=letter,bottomup=0)


	textob = c.beginText()
	#textob.setTextOrigin(inch,inch)
	textob.setFont("Helvetica",14)
	objbooks = product.objects.all()
	lines = []
	for objb in objbooks:
		lines.append(objb.product_name)
		lines.append(objb.product_price)	



	for line in lines:
		textob.textLine(line)
	
	c.drawText(textob)
	c.showPage()
	c.save()	
	buf.seek(0)
	return FileResponse(buf, as_attachment=True, filename='products.pdf')
  







