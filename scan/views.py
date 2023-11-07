from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import socket
from socket import AF_INET, SOCK_STREAM
import time
from .models import port_status, ip_results, cidr_table
from .forms import IpResultsForm, SubnetScan
import ipaddress
import asyncio
from asgiref.sync import sync_to_async
from django.template.loader import render_to_string

#Variables

PORT_RANGE = range(1, 1024)
hosts = ''
cidr = ''
# Create your views here.

def start_time():
    st_time = time.time()
    return (st_time)

def end_time():
    en_time = time.time()
    return (en_time)


def clean_database(dt_table):
    non_persistent_table = dt_table.objects.all() #prep database ip_results to store data
    non_persistent_table.delete() 

#subnet_scan view with form to scan desired subnet
"""def subnet_scan(request):
    st_time = start_time()
    form = SubnetScan()
    if request.method == "POST":
        form = SubnetScan(request.POST)
        form.is_valid()
        vlan_id = form.cleaned_data["VLAN"]
        ip_network = form.cleaned_data["IP"]
        cidr = form.cleaned_data["CIDR"]  
        hosts = check_cidr(cidr)
        state = scan_ips(ip_network, cidr, clean_database(ip_results)) #run scan_ips to discover active/inactive hosts
        en_time = round((end_time() - st_time), 3) #measure time to process scan
        return render(request, 'scan/subnet_scan.html', 
                {#'vlan_id':vlan_id,
                'ip_network':ip_network,
                'cidr': cidr,
                'hosts':hosts,
                'form':form,
                'state': state,
                'en_time': en_time,
                })
    return render(request, 'scan/subnet_scan.html', 
            {'form': form,
            })"""


async def subnet_scan(request):
    st_time = start_time()
    form = SubnetScan()

    if request.method == "POST":
        form = SubnetScan(request.POST)
        form.is_valid()
        vlan_id = form.cleaned_data["VLAN"]
        global ip_network
        ip_network = form.cleaned_data["IP"]
        global cidr
        cidr = form.cleaned_data["CIDR"]
        #hosts = check_cidr(cidr)  # Run check_cidr in a thread
        #state = await asyncio.to_thread(scan_ips, ip_network, cidr, await asyncio.to_thread(clean_database, ip_results))  # Run scan_ips and clean_database in threads
        state = await scan_ips(ip_network, cidr, await asyncio.to_thread(clean_database, ip_results))
        global en_time
        en_time = round((end_time() - st_time), 3)

        # context = {
        #     'ip_network': ip_network,
        #     'cidr': cidr,
        #     'hosts': hosts,
        #     'form': form,
        #     'state': state,
        #     'en_time': en_time,
        # }
        return redirect('subnet_results')
        #return render(request, 'scan/subnet_scan.html', context)

    context = {'form': form}
    return render(request, 'scan/subnet_scan.html', context)

def subnet_results(request):
    state = ip_results.objects.all().order_by('IP_address')
    hosts = check_cidr(cidr)
    form = SubnetScan()
    
    context = {
        'ip_network': ip_network,
        'cidr': cidr,
        'hosts': hosts,
        'state': state,
        'en_time': en_time,
        'form': form,
    }
    return render(request, 'scan/subnet_results.html', context)

async def check_ip(ip, non_persistent_table):
    for port in PORT_RANGE:
        s = socket.socket(AF_INET, SOCK_STREAM)
        s.settimeout(0.002)
        conn = await asyncio.to_thread(s.connect_ex, (str(ip), port))
        if conn == 0:
            ip_state = 'active'
            break
    else:
        ip_state = 'inactive'

    non_persistent_table = ip_results(IP_address=ip, ip_state=ip_state)
    await asyncio.to_thread(non_persistent_table.save)
    s.close()

async def scan_ips(ip_network, cidr, non_persistent_table):
    ip_network = ip_network + cidr
    network = ipaddress.IPv4Network(ip_network, strict=False)

    tasks = []
    for ip in network.hosts():
        task = asyncio.create_task(check_ip(ip, non_persistent_table))
        tasks.append(task)

    await asyncio.gather(*tasks)
    
    non_persistent_table = await asyncio.to_thread(ip_results.objects.all)
    return non_persistent_table

#cidr check and compare value from the form with database, extracting amount of hosts 
"""def check_cidr(cidr):
    cidr_database = cidr_table.objects.all()
    for cidr_fromdatabase in cidr_database:
            cidr_value = cidr_fromdatabase.cidr
            if cidr == cidr_value:
               return cidr_fromdatabase.noOFhosts
    return 'Incorrect subnet'   """ 

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
        st_time = start_time()
        ip_check_field = request.POST['ip_check_field']
        #clear table
        clean_database(port_status)   
        no_open = ''
        port_scan(PORT_RANGE, ip_check_field) #port_scan to run scan on given ip
        port_scan_results = port_status.objects.all() #create queryset
        # if no records in queryset exists set "No open ports found" context - meaning no open ports found in port_scan
        en_time = round((end_time() - st_time), 3) 
        if not port_status.objects.exists():
            no_open = 'No open ports found!'    
        return render(request, 'scan/ip_check.html',
            {'ip_check_field':ip_check_field,
            'port_scan_results':port_scan_results,
            'no_open':no_open,
            'en_time': en_time,
            })    
    else:
        return render(request, "scan/ip_check.html",
            {})

# port scanning method
# takes PORT_RANGE and ip from ip_check function and carries port scan
def port_scan(PORT_RANGE, ip_check_field): 
    for i in PORT_RANGE:
        s = socket.socket(AF_INET, SOCK_STREAM)
        s.settimeout (0.03)
        #socket to check if port is open      
        conn = s.connect_ex((ip_check_field, i))
        if(conn == 0):
            port_scan_results = port_status(port_number=(i), port_status='open')
            port_scan_results.save()
            port_scan_results = port_status.objects.all()
        else:
            no_open = "No open ports found!"
            port_scan_results = port_status.objects.all()
        # error handling here?
        s.close()    
    return (port_scan_results, no_open)

#index page "hello world"
def index(request):
    return render(request, "scan/index.html",)