from base.models import *

print(FuelPurchase.objects.all())  # Yonilg'i sotib olishlar
print(Moyka.objects.all())  # Moyka xizmatlari
fuel_stats = FuelPurchase.objects.values('petrol_type').annotate(
    total=Count('petrol_type'),
    total_price=Sum('price')
).order_by('petrol_type')

moyka_stats = Moyka.objects.values('service_type').annotate(
    total=Count('service_type')
).order_by('service_type')

print(fuel_stats)  # Yonilg'i statistikasi
print(moyka_stats)  # Moyka statistikasi
