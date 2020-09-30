"""mediapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pharmaapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('cart/',views.cart,name='cart'),
    path('contact1/',views.contact1,name='contact1'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('pharmorders/',views.pharmorders,name='pharmorders'),
    path('queorder/',views.queorder,name='queorder'),
    path('invoice/',views.invoice,name='invoice'),
    path('delivery/',views.delivery,name='delivery'),
  # path('stafflogin/',views.stafflogin,name='stafflogin'),
    path('pharmaregister/',views.pharmaregister,name='pharmaregister'),
    path('dvboyregister/',views.dvboyregister,name='dvboyregister'),
    path('adminsignup/',views.adminsignup,name='adminsignup'),
    path('customerlogin/',views.customerlogin,name='customerlogin'),
    path('customersignup/',views.customersignup,name='customersignup'),
    path('login/',views.login,name='login'),
    path('medicine/',views.medicine,name='medicine'),
    path('mcompany/',views.mcompany,name='mcompany'),
    path('mcategory/',views.mcategory,name='mcategory'),
    path('category/',views.category,name='category'),
    path('details/<int:cid>/',views.details,name='details'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('ordermedicine/',views.ordermedicine,name='ordermedicine'),
    path('shop/',views.shop,name='shop'),
    path('checkout/<int:iid>/',views.checkout,name='checkout'),
    path('notification/',views.notification,name='notification'),
    path('feedback/',views.feedback,name='feedback'),
    path('thankyou/',views.thankyou,name='thankyou')
    
]
