from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class salestable(models.Model):
    customer_id = models.ForeignKey(User,on_delete=models.CASCADE)
    productid = models.CharField(max_length=10)
    productname = models.CharField(max_length=100)
    productprice = models.CharField(max_length=100)
    companyname =models.CharField(max_length=100)
    totalprice = models.CharField(default='',max_length=100)
    productqty = models.CharField(default='',max_length=100)


    def __str__(self):
        return self.customer_id.last_name