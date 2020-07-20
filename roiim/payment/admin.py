from django.contrib import admin

from .models import Payment
# Register your models here.
class PAymentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Payment, PaymentAdmin)