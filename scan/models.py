from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class ip_results(models.Model):
    hostname = models.CharField(max_length=200)
    IP_address = models.GenericIPAddressField()
    ip_state = models.CharField(max_length=20)
    
    def __str__(self):
        return self.IP_address
    
class port_status(models.Model):
    port_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(65353)])
    port_status = models.CharField(max_length=20)

    def __str__(self):
        return f'Port ' + str(self.port_number)