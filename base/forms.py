from django import forms
from .models import FuelPurchase, Customer, Moyka, MoykaCustomer

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class FuelPurchaseForm(forms.ModelForm):
    class Meta:
        model = FuelPurchase
        fields = ['customer', 'petrol_type', 'litres']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'petrol_type': forms.Select(attrs={'class': 'form-control'}),
            'litres': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FuelPurchaseForm1(forms.ModelForm):
    class Meta:
        model = FuelPurchase
        fields = ['petrol_type', 'litres']
        widgets = {
            'petrol_type': forms.Select(attrs={'class': 'form-control'}),
            'litres': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'full_name', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqam'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi ismi'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Manzil', 'rows': 3}),
        }

class MoykaForm(forms.ModelForm):
    class Meta:
        model = Moyka
        fields = ['service_type']
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-control'}),
        }

class MoykaCustomerForm(forms.ModelForm):
    class Meta:
        model = MoykaCustomer
        fields = ['phone_number', 'full_name', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqam'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi ismi'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Manzil', 'rows': 3}),
        }