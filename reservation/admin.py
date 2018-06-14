from django.contrib import admin
from .models import Film, Audi, Screening, Seat, Booking

# Register your models here.
admin.site.register(Film)
admin.site.register(Audi)
admin.site.register(Screening)
admin.site.register(Seat)
admin.site.register(Booking)
