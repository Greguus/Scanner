from django.core.management.base import BaseCommand
from scan.models import cidr_table
import ipaddress

cidr_table.objects.all().delete()

    # List of CIDR notations to consider
cidr_notations = ['/' + str(i) for i in range(33)]  # /0 to /32

for cidr_notation in cidr_notations:
    # Calculate the number of possible hosts
    net = ipaddress.IPv4Network(f'0.0.0.0{cidr_notation}', strict=False)
    num_hosts = net.num_addresses - 2

    # Create and save a record in the cidr_table
    cidr_record = cidr_table(cidr=cidr_notation, noOFhosts=num_hosts)
    cidr_record.save()

    print(f'Successfully added record for {cidr_notation} with {num_hosts} possible hosts.')
