from django.shortcuts import render ,redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from . forms import UserRegistrationForm
from django.views.generic import ListView,DetailView,FormView,UpdateView ,DeleteView
from django.contrib.auth.models import User
from company.models import company

# Create your views here.


def login(request):
    form = forms.LoginForm()
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )         
        
    else:
        form = forms.LoginForm()
       # return render_to_response('users/sign-in.html')
        return render_to_response("users/sign-in.htm",{"form":form})





def sign_up(request):
    if request.method == 'POST':
      form =  UserRegistrationForm(request.POST)
      if form.is_valid():
             form.save()
             username = form.cleaned_data.get('username')
             messages.success(request, f'Account Created for {username} you can now log in')
             return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request ,'users/sign-up.html',{'form':form})


def profile(request,**kwargs):
    
    logged_as_company = company.objects.get(companyid = request.user.id)
    if logged_as_company:
        print(logged_as_company.company_name)
        return render(request,'users/profile.html',{'logged_as_company':logged_as_company})

   



