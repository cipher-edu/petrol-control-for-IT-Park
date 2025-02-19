from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('', CustomerListView.as_view(), name='home'),  # Asosiy sahifa
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/<str:unique_id>/profile/', CustomerProfileView.as_view(), name='customer_profile'),
    path('add_fuel/', add_fuel, name='add_fuel'),
    path('index2/', index2, name='index2'),
]
