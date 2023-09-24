from django.contrib import admin

# Register your models here.

from .models import ip_results, port_status, cidr_table

admin.site.register(ip_results)
admin.site.register(port_status)
admin.site.register(cidr_table)
