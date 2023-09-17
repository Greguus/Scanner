from django.db import models

# Create your models here.

class IP_results(models.Model):
    hostname = models.CharField(max_length=200)
    IP_address = models.GenericIPAddressField()
    ip_state = models.CharField(max_length=20)
    def __str__(self):
        return self.IP_address
    