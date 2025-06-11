from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random



from django.db import models
class Product(models.Model):
    seller = models.ForeignKey('myapp.CustomUser', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name
    


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=200, choices=USER_ROLES, default='buyer')
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username