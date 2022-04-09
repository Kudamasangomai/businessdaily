from django.urls import path 
from . import views
#from .views import (profile )

urlpatterns = [


    path('', views.login,name='login-user'),
    path('signup/',views.sign_up,name='sign-up')  ,  
   # path('profile/<int:pk>/',profile.as_view(),name='profile'),
    path('profile/<int:pk>/',views.profile,name='profile')



]
