from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_cna = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.TextField(blank=True)

    def __str__(self):
        return f"Client: {self.user.username}"

class CNA(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    experience = models.TextField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Notification(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    message    = models.TextField()
    timestamp  = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"