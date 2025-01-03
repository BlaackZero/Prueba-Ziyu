from django.contrib import admin
from .models import Client, Gardener, VisitRequest

# Registrar los modelos en el admin
admin.site.register(Client)
admin.site.register(Gardener)
admin.site.register(VisitRequest)
# Register your models here.
