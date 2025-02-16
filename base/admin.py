from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Customer, FuelPurchase

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'phone_number', 'full_name', 'address', 'total_points')
    search_fields = ('unique_id', 'phone_number', 'full_name')
    list_filter = ('total_points', 'unique_id', 'phone_number', 'full_name')

    def save_model(self, request, obj, form, change):
        if self.name(request, obj) or self.telefon(request, obj):
            return
        super().save_model(request, obj, form, change)

    def name(self, request, obj):
        if Customer.objects.filter(full_name=obj.full_name).exists():
            messages.error(request, 'Ushbu ism familiya bilan avval foydalanuvchi ro\'yxatdan  o\'tkazilgan.')
            return True
        return False

    def telefon(self, request, obj):
        if Customer.objects.filter(phone_number=obj.phone_number).exists():
            messages.error(request, 'Ushbu telefon raqam avval ro\'yxatdan o\'tkazilgan.')
            return True
        return False

@admin.register(FuelPurchase)
class FuelPurchaseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'petrol_type', 'litres', 'get_customer_points')
    list_filter = ('petrol_type', 'customer__full_name', 'customer__phone_number')

    def get_customer_points(self, obj):
        return obj.customer.total_points
    get_customer_points.short_description = 'Total Points'