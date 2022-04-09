from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from datetime import datetime ,timedelta
from django.urls import reverse
User._meta.get_field('email').verbose_name = "new name"

# Create your models here.

class company(models.Model):
    
    location_choices= (

    ("cbd", "CBD"),
    ("graniteside", "granitiside"),
    ("willovale", "willovale"),
    ("workington", "workington"),
    ("borrowdale", "borrowdale"),
   
    )

    type_choices=(
        ("pbc","Public Business Corperation "),
        ("pvt","Private limited"),
    )
  
    companyid = models.OneToOneField(User,on_delete = models.CASCADE)
    company_name =  models.CharField(max_length=100,unique=True)
    company_reg_number = models.CharField(max_length=100,unique=True)
    company_address = models.CharField(max_length=100)
    location = models.CharField( max_length = 20, choices = location_choices,default = 'cbd')
    company_type = models.CharField(max_length=50,choices =type_choices,default='pbc')
    firstname_director = models.CharField(max_length=50)
    firstsurname_director = models.CharField(max_length=50)
    secondname_director = models.CharField(max_length=50)
    secondsurname_director = models.CharField(max_length=50)
    regdate = models.DateTimeField(default=timezone.now)
    approved=models.CharField(max_length=20,default="Not Approved")
        
        
    def __str__(self):
        return self.company_name


class product(models.Model):
    category_choices= (

    ("kitchenware", "kitchenware"),
    ("clothes", "clothes"),
    ("accesories", "accesories"),
    ("service", "service"),
    ("bevarages", "bevarages"),
    ("gadgets", "gadgets"),
    ("food", "food"),
    ("vehicles", "vehicles"),
   
    )
   
    product_image = models.ImageField(default='default.jpg' ,upload_to ='product_pics')
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_info = models.CharField(max_length=200)    
    product_quantity = models.IntegerField()
    product_category = models.CharField( max_length = 20, choices =  category_choices,default = 'food')
    dateposted = models.DateTimeField(default=timezone.now)
    postedbyuser = models.ForeignKey(User,on_delete=models.CASCADE)
    companyid = models.ForeignKey(company,on_delete=models.CASCADE)
   


    def __str__(self):
        return self.product_name
    


class customer_order(models.Model):
    customer_id = models.ForeignKey(User,on_delete=models.CASCADE)
    productid = models.CharField(max_length=10)
    productname = models.CharField(max_length=100)
    productprice = models.CharField(max_length=100)
    companyname =models.CharField(max_length=100)
    totalprice = models.CharField(default='',max_length=100)
    productqty = models.CharField(default='',max_length=100)


    def __str__(self):
        return self.customer_id.last_name


class comments(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    comments = models.CharField(max_length=100)
    commentdate = models.DateTimeField(default=timezone.now)
    postedbyuser = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.product.product_name






