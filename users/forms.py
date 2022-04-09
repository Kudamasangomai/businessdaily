from django import forms
from company.models import company ,product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#User._meta.get_field('email')._unique = True


class LoginForm(forms.Form):
    username = forms.CharField(max_length=5,label='Your name')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)



    

    


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(min_length=3)

    #the model in which this form is going to interact with
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']


class companyregistration(forms.ModelForm):
    company_name = forms.CharField(max_length=50,required=True,
    widget=forms.TextInput(attrs={'Placeholder': 'Unique and Human readable e.g CBZ'}),)
    companyid = forms.CharField(
         widget=forms.TextInput(attrs={'Placeholder': 'Company ID'}),
    )
    company_reg_number = forms.CharField(
         widget=forms.TextInput(attrs={'Placeholder': 'CBZ10456'}),
    )   
   


    class Meta:
        model = company
        fields = "__all__"    

class CompanyUpdateForm(forms.ModelForm):   
	

	class Meta:
		model = User
		fields = ['is_superuser']


class productform(forms.ModelForm): 

    class Meta:
        model = product
        exclude = ['postedbyuser','companyid']
   #     fields ='__all__'
        
        
  








