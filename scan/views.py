from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from socket import *
import time

# Create your views here.

# ip_check takes IP address from search field in navbar and carries out ping and port scan on given IP.
def ip_check(request):
    if request.method == "POST":
        ip_check_field = request.POST['ip_check_field']
        port_range = range(78, 81)
        status = {}
        n=0
        for i in port_range:
            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout (0.02)
            # socket to check if port is open      
            conn = s.connect_ex((ip_check_field, i))
            if(conn == 0):
                status[port_range[n]]='open'
                n+=1
               # return render(request, 'scan/ip_check.html',
                #{'ip_check_field':ip_check_field,
                #'status':status,
                #'port_range':port_range,
                #'i':i})  
            else:
                status[port_range[n]]='closed'
                n+=1
               # return render(request, 'scan/ip_check.html',
                #    {'ip_check_field':ip_check_field,
                 #   'status':status,
                  #  'port_range':port_range,
                   # 'i':i})
        s.close()
        return render(request, 'scan/ip_check.html',
                {'ip_check_field':ip_check_field,
                'status':status,
                'port_range':port_range,
                'i':i})  
            
    else:
        return render(request, "scan/ip_check.html",
                  {})


def index(request):
    ip_list = ["10.10.30.101", "10.10.30.102", "10.10.30.103"]
    context = {"ip_list": ip_list}
    return render(request, "scan/index.html", context)