from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from socket import *
import time
from .models import port_status, ip_results, cidr_table
from .forms import IpResultsForm, SubnetScan
import ipaddress


# Create your views here.

#subnet_scan view with form to scan desired subnet
def subnet_scan(request):
    form = SubnetScan()
    if request.method == "POST":
        form = SubnetScan(request.POST)
        form.is_valid()
        vlan_id = form.cleaned_data["VLAN"]
        ip_network = form.cleaned_data["IP"]
        cidr = form.cleaned_data["CIDR"]    
        hosts = check_cidr(cidr)
        successful_connections =[]
        state = scan_ips(ip_network, cidr)
        return render(request, 'scan/subnet_scan.html', 
                {'vlan_id':vlan_id,
                'ip_network':ip_network,
                'cidr': cidr,
                'hosts':hosts,
                'form':form,
                'state': state,
                'successful_connections': successful_connections,
                })
    return render(request, 'scan/subnet_scan.html', 
            {'form': form,
            })

#Iterate through all IP addresses in given subnet (cidr)
def scan_ips(ip_network, cidr):
    ip_network = ip_network + cidr
    network = ipaddress.IPv4Network(ip_network, strict=False)
    successful_connections =[]
    state = []
    for ip in network.hosts():
        ip_address = str(ip)
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout (0.02)
        #socket to check if port is open      
        conn = s.connect_ex((ip_address, 80))
        if(conn == 0):
            successful_connections.append(ip_address)
            state.append('active')
        else:
            successful_connections.append(ip_address)
            state.append('inactive')
        # error handling here?
        s.close()
        
    return (successful_connections, state)

#cidr check and compare value from the form with database, extracting amount of hosts 
def check_cidr(cidr):
    cidr_database = cidr_table.objects.all()
    for cidr_fromdatabase in cidr_database:
            cidr_value = cidr_fromdatabase.cidr
            if cidr == cidr_value:
               return cidr_fromdatabase.noOFhosts
    return 'Incorrect subnet'    
            

 
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

#index page "hello world"
def index(request):
    return render(request, "scan/index.html",)