from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Count
from django.utils.timezone import now
from django.db.models import Q

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
        query = request.GET.get('q', '')  # Qidiruv so‘rovi
        selected_date = request.GET.get('date', '')  # Kalendar orqali tanlangan sana

        customers_list = Customer.objects.all()

        # Qidiruv
        if query:
            customers_list = customers_list.filter(
                Q(unique_id__icontains=query) |
                Q(full_name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(address__icontains=query)
            )

        if selected_date:
            customers_list = customers_list.filter(created_at__date=selected_date)
            
        today = now().date()
        daily_customers = Customer.objects.filter(created_at__date=today).count()

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
        moyka_form = MoykaForm()

        return render(request, 'customer_list.html', {
            'customers': customers,
            'customer_form': customer_form,
            'fuel_form': fuel_form,
            'moyka_form': moyka_form,
            'daily_customers': daily_customers,
            'daily_most_used_petrol': daily_most_used_petrol,
            'query': query,
            'selected_date': selected_date
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
        else:
            messages.error(request, "Ma'lumotlarni to'ldiring. Xatolik yuz berdi!")

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
        purchases_list = FuelPurchase.objects.filter(customer=customer).order_by('-id')

        fuel_points = {
            80: 0,
            91: 0,
            92: 0,
            95: 0
        }

        for purchase in purchases_list:
            if purchase.petrol_type == 80:
                purchase.points = purchase.litres * 0.1
                fuel_points[80] += purchase.points
            elif purchase.petrol_type in [91, 92]:
                purchase.points = purchase.litres * 0.2
                fuel_points[91] += purchase.points
                fuel_points[92] += purchase.points
            elif purchase.petrol_type == 95:
                purchase.points = purchase.litres * 0.3
                fuel_points[95] += purchase.points
            else:
                purchase.points = 0

        paginator = Paginator(purchases_list, 10)
        page_number = request.GET.get('page')
        purchases = paginator.get_page(page_number)

        form = FuelPurchaseForm1()

        return render(request, 'customer_profile.html', {
            'customer': customer,
            'purchases': purchases,
            'form': form,
            'fuel_points': fuel_points
        })

    def post(self, request, unique_id):
        customer = get_object_or_404(Customer, unique_id=unique_id)
        form = FuelPurchaseForm1(request.POST)

        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.customer = customer
            purchase.save()
            messages.success(request, "Yonilg‘i muvaffaqiyatli saqlandi!")
            return redirect('customer_profile', unique_id=unique_id)
        else:
            messages.error(request, "Ma'lumotlarni to'ldiring. Xatolik yuz berdi!")

        purchases_list = FuelPurchase.objects.filter(customer=customer).order_by('-id')
        paginator = Paginator(purchases_list, 10)
        page_number = request.GET.get('page')
        purchases = paginator.get_page(page_number)

        return render(request, 'customer_profile.html', {
            'customer': customer,
            'purchases': purchases,
            'form': form
        })

class CustomerProfileView1(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '')  # Qidiruv so‘rovi
        selected_date = request.GET.get('date', '')  # Kalendar orqali tanlangan sana

        customers_list = Customer.objects.all()

        # Qidiruv
        if query:
            customers_list = customers_list.filter(
                Q(unique_id__icontains=query) |
                Q(full_name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(address__icontains=query)
            )

        if selected_date:
            customers_list = customers_list.filter(created_at__date=selected_date)
            
        today = now().date()
        daily_customers = Customer.objects.filter(created_at__date=today).count()

        daily_top_petrol = (
            FuelPurchase.objects.filter(date__date=today)
            .values('petrol_type')
            .annotate(count=Count('petrol_type'))
            .order_by('-count')
            .first()
        )
        daily_most_used_petrol = daily_top_petrol['petrol_type'] if daily_top_petrol else None  
        paginator = Paginator(customers_list, 15)
        page_number = request.GET.get('page')
        customers = paginator.get_page(page_number)

        fuel_form = FuelPurchaseForm()
        customer_form = CustomerForm()

        return render(request, 'tables-datatables.html', {
            'customers': customers,
            'customer_form': customer_form,
            'fuel_form': fuel_form,
            'daily_customers': daily_customers,
            'daily_most_used_petrol': daily_most_used_petrol,
            'query': query,
            'selected_date': selected_date
        })

    def post(self, request):
        if 'add_customer' in request.POST:
            return self.add_customer(request)
        elif 'add_fuel' in request.POST:
            return self.add_fuel(request)
        return redirect('index2')

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
            return redirect('index2')

        return self.get(request)

    def add_fuel(self, request):
        fuel_form = FuelPurchaseForm(request.POST)
        if fuel_form.is_valid():
            fuel_form.save()
            messages.success(request, "Yonilg‘i muvaffaqiyatli saqlandi!")
        else:
            messages.error(request, "Yonilg‘i saqlanmadi, ma'lumotlarni tekshiring!")
        return redirect('index2')

class MoykaCustomerListView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '')  # Qidiruv so‘rovi
        selected_date = request.GET.get('date', '')  # Kalendar orqali tanlangan sana

        customers_list = MoykaCustomer.objects.all()

        # Qidiruv
        if query:
            customers_list = customers_list.filter(
               Q(unique_id__icontains=query) |
                Q(full_name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(address__icontains=query)
            )

        if selected_date:
            customers_list = customers_list.filter(created_at__date=selected_date)
            
        today = now().date()
        daily_customers = MoykaCustomer.objects.filter(created_at__date=today).count()

        daily_top_service = (
            Moyka.objects.filter(date__date=today)
            .values('service_type')
            .annotate(count=Count('service_type'))
            .order_by('-count')
            .first()
        )
        daily_most_used_service = daily_top_service['service_type'] if daily_top_service else None  
        paginator = Paginator(customers_list, 25)
        page_number = request.GET.get('page')
        customers = paginator.get_page(page_number)

        moyka_form = MoykaForm()
        customer_form = MoykaCustomerForm()

        return render(request, 'moyka_datatables.html', {
            'customers': customers,
            'customer_form': customer_form,
            'moyka_form': moyka_form,
            'daily_customers': daily_customers,
            'daily_most_used_service': daily_most_used_service,
            'query': query,
            'selected_date': selected_date
        })

    def post(self, request):
        if 'add_customer' in request.POST:
            return self.add_customer(request)
        elif 'add_moyka' in request.POST:
            return self.add_moyka(request)
        return redirect('moyka_list')

    def add_customer(self, request):
        customer_form = MoykaCustomerForm(request.POST)
        
        phone_number = request.POST.get('phone_number')
        full_name = request.POST.get('full_name')

        if MoykaCustomer.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Bu telefon raqami bilan foydalanuvchi allaqachon mavjud!")
        elif MoykaCustomer.objects.filter(full_name=full_name).exists():
            messages.error(request, "Bu ism bilan foydalanuvchi allaqachon mavjud!")
        elif customer_form.is_valid():
            customer_form.save()
            messages.success(request, "Foydalanuvchi muvaffaqiyatli qo‘shildi!")
            return redirect('moyka_list')
        else:
            messages.error(request, "Ma'lumotlarni to'ldiring. Xatolik yuz berdi!")

        return self.get(request)

    def add_moyka(self, request):
        moyka_form = MoykaForm(request.POST)
        if moyka_form.is_valid():
            moyka_form.save()
            messages.success(request, "Moyka muvaffaqiyatli saqlandi!")
        else:
            messages.error(request, "Moyka saqlanmadi, ma'lumotlarni tekshiring!")
        return redirect('moyka_list')

class MoykaCustomerProfileView(LoginRequiredMixin, View):
    def get(self, request, unique_id):
        customer = get_object_or_404(MoykaCustomer, unique_id=unique_id)
        moyka_list = Moyka.objects.filter(customer=customer).order_by('-id')

        service_points = {
            'Ekonom': 0,
            'Bussines': 0,
            'Premium': 0
        }

        for moyka in moyka_list:
            if moyka.service_type == 'Ekonom':
                moyka.points = moyka.summa * 0.1
                service_points['Ekonom'] += moyka.points
            elif moyka.service_type == 'Bussines':
                moyka.points = moyka.summa * 0.2
                service_points['Bussines'] += moyka.points
            elif moyka.service_type == 'Premium':
                moyka.points = moyka.summa * 0.3
                service_points['Premium'] += moyka.points
            else:
                moyka.points = 0

        paginator = Paginator(moyka_list, 10)
        page_number = request.GET.get('page')
        moykas = paginator.get_page(page_number)

        form = MoykaForm()

        return render(request, 'customer_profile.html', {
            'customer': customer,
            'moykas': moykas,
            'form': form,
            'service_points': service_points
        })

    def post(self, request, unique_id):
        customer = get_object_or_404(MoykaCustomer, unique_id=unique_id)
        form = MoykaForm(request.POST)

        if form.is_valid():
            moyka = form.save(commit=False)
            moyka.customer = customer
            moyka.save()
            messages.success(request, "Moyka muvaffaqiyatli saqlandi!")
            return redirect('customer_profile', unique_id=unique_id)
        else:
            messages.error(request, "Ma'lumotlarni to'ldiring. Xatolik yuz berdi!")

        moyka_list = Moyka.objects.filter(customer=customer).order_by('-id')
        paginator = Paginator(moyka_list, 10)
        page_number = request.GET.get('page')
        moykas = paginator.get_page(page_number)

        return render(request, 'customer_profile.html', {
            'customer': customer,
            'moykas': moykas,
            'form': form
        })
