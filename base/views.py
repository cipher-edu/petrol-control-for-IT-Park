from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Count
from django.utils.timezone import now

# bazovoy kodlar
def custom_logout(request):
    logout(request)
    return redirect('login')
  
def handler404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def add_fuel(request):
    if request.method == "POST":
        fuel_form = FuelPurchaseForm(request.POST)
        if fuel_form.is_valid():
            fuel_form.save()
            messages.success(request, "Yonilg‘i muvaffaqiyatli saqlandi!")
            return redirect('customer_list')  # Ma'lumot saqlangandan keyin qayta yuklash
        else:
            messages.error(request, "Xatolik yuz berdi! Ma’lumotlarni to‘ldiring.")

    return redirect('customer_list')

#asosiy kodlar
class CustomerListView(LoginRequiredMixin, View):
    def get(self, request):
        customers_list = Customer.objects.all()

        # Bugungi qo‘shilgan foydalanuvchilar soni
        today = now().date()
        daily_customers = Customer.objects.filter(created_at__date=today).count()

        # Bugungi eng ko‘p sotilgan yoqilg‘i turini topish
        daily_top_petrol = (
            FuelPurchase.objects.filter(date__date=today)
            .values('petrol_type')
            .annotate(count=Count('petrol_type'))
            .order_by('-count')
            .first()
        )
        daily_most_used_petrol = daily_top_petrol['petrol_type'] if daily_top_petrol else None  

        paginator = Paginator(customers_list, 25)
        page_number = request.GET.get('page')
        customers = paginator.get_page(page_number)
        fuel_form = FuelPurchaseForm()
        customer_form = CustomerForm()
        return render(request, 'customer_list.html', {
            'customers': customers,
            'customer_form': customer_form,
            'daily_customers': daily_customers,
            'daily_most_used_petrol': daily_most_used_petrol,
            'fuel_form': fuel_form,
        })

    def post(self, request):
        if 'add_customer' in request.POST:
            return self.add_customer(request)
        elif 'add_fuel' in request.POST:
            return self.add_fuel(request)
        return redirect('customer_list')

    def add_customer(self, request):
        customer_form = CustomerForm(request.POST)
        
        phone_number = request.POST.get('phone_number')
        full_name = request.POST.get('full_name')

        if Customer.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Bu telefon raqami bilan foydalanuvchi allaqachon mavjud!")
        elif Customer.objects.filter(full_name=full_name).exists():
            messages.error(request, "Bu ism bilan foydalanuvchi allaqachon mavjud!")
        elif customer_form.is_valid():
            customer_form.save()
            messages.success(request, "Foydalanuvchi muvaffaqiyatli qo‘shildi!")
            return redirect('customer_list')

        return self.get(request)

    def add_fuel(self, request):
        fuel_form = FuelPurchaseForm(request.POST)
        if fuel_form.is_valid():
            fuel_form.save()
            messages.success(request, "Yonilg‘i muvaffaqiyatli saqlandi!")
        else:
            messages.error(request, "Yonilg‘i saqlanmadi, ma'lumotlarni tekshiring!")
        return redirect('customer_list')
    
class CustomerProfileView(LoginRequiredMixin, View):
    def get(self, request, unique_id):
        customer = get_object_or_404(Customer, unique_id=unique_id)
        purchases_list = FuelPurchase.objects.filter(customer=customer).order_by('-id')  # So‘nggi xaridlar yuqorida

        # Xaridlar ro‘yxatiga ballarni qo‘shish
        for purchase in purchases_list:
            if purchase.petrol_type == 80:
                purchase.points = purchase.litres * 0.1
            elif purchase.petrol_type in [91, 92]:
                purchase.points = purchase.litres * 0.2
            elif purchase.petrol_type == 95:
                purchase.points = purchase.litres * 0.3
            else:
                purchase.points = 0

        # Paginatsiya (har sahifada 10 ta xarid)
        paginator = Paginator(purchases_list, 10)
        page_number = request.GET.get('page')
        purchases = paginator.get_page(page_number)

        return render(request, 'customer_profile.html', {
            'customer': customer,
            'purchases': purchases
        })
    
    
# @login_required
# def index(request):
#     customers = Customer.objects.all()
#     form = FuelPurchaseForm()

#     if request.method == 'POST':
#         form = FuelPurchaseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # 'index' emas, 'home' bo‘lishi kerak

#     return render(request, 'index.html', {'customers': customers, 'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username'] 
#         password = request.POST['password'] 
#         user = authenticate(request, username=username, password=password)  
#         if user is not None:
#             login(request, user) 
#             return redirect('admin') 
#         else:
#             return render(request, 'login.html', {'error': 'Noto‘g‘ri foydalanuvchi nomi yoki parol'})  # Xato xabari
#     return render(request, 'login.html')  
