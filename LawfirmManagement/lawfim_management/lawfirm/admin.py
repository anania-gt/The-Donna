from django.contrib import admin

# Register your models here.
from .models import Lawyer,Client,Appointment,ClientDischargeDetails
# Register your models here.
class LawyerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Lawyer, LawyerAdmin)

class ClientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Client, ClientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class ClientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(ClientDischargeDetails, ClientDischargeDetailsAdmin)
