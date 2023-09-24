from django import forms
from .models import ip_results

#form to filter IP results
class IpResultsForm(forms.ModelForm):
    class Meta:
        model = ip_results
        fields = ['hostname', 'IP_address', 'ip_state', 'snmp']

#form to scan IP range (based on CIDR or VLAN)
class SubnetScan(forms.Form):
    VLAN = forms.CharField(label="VLAN", max_length=4)
    IP = forms.GenericIPAddressField(label="IP")
    CIDR_CHOICES = [(f'/{i}') for i in range(0, 33)]  # Generates /0 to /32
    CIDR = forms.ChoiceField(choices=CIDR_CHOICES)
    