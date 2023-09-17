from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Create your views here.

def index(request):
    ip_list = ["10.10.30.101", "10.10.30.102", "10.10.30.103"]
    context = {"ip_list": ip_list}
    return render(request, "scan/index.html", context)