from django.urls import path

from . import views

urlpatterns = [
   path('register/',views.Registration,name='register'),
    path('',views.loginPage,name='login'),
   path('logout/',views.logOut,name='logout')
     
    
]

