from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)

admin.site.register(MedicalHistory)
admin.site.register(Prescription)
