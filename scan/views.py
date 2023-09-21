from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from socket import *
import time
from .models import port_status

# Create your views here.

# takes IP address from search field in navbar.
def ip_check(request):
    if request.method == "POST":
        ip_check_field = request.POST['ip_check_field']
        port_range = port_status.objects.all()
        #clear table
        port_range.delete()    
        no_open = ''
        port_range = range (1, 85)
        port_scan(port_range, ip_check_field)
        port_range = port_status.objects.all()
        # if no records in queryset exists set "No open ports found" context
        if not port_status.objects.exists():
            no_open = 'No open ports found!'   
       
        return render(request, 'scan/ip_check.html',
            {'ip_check_field':ip_check_field,
            'port_range':port_range,
            'no_open':no_open,
            })    
    else:
        return render(request, "scan/ip_check.html",
                  {})

# port scanning method
# takes port_range and ip from ip_check function and carries port scan
def port_scan(port_range, ip_check_field): 
    for i in port_range:
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout (0.02)
        #socket to check if port is open      
        conn = s.connect_ex((ip_check_field, i))
        if(conn == 0):
            port_range = port_status(port_number=(i), port_status='open')
            port_range.save()
            port_range = port_status.objects.all()
        else:
            no_open = "No open ports found!"
        # error handling here?
        s.close()
        
    return (port_range, no_open)

def index(request):
    return render(request, "scan/index.html",)