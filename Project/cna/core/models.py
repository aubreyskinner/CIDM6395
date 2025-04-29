from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model


class User(AbstractUser):
    is_cna = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return self.username

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
    
class CNAListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')  # <-- ADD THIS LINE
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    experience = models.TextField()
    location = models.CharField(max_length=255)
    availability = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.location}"
    
User = get_user_model()

class WeeklyJobSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # CNA who owns this entry
    client_name = models.CharField(max_length=100)
    week_of = models.DateField(help_text="Start date of the week (e.g., Monday)")
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)
    pay_rate = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.TextField(blank=True)

    @property
    def expected_pay(self):
        return round(self.total_hours * self.pay_rate, 2)

    def __str__(self):
        return f"{self.client_name} - Week of {self.week_of}"
    
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    cna = models.ForeignKey(CNAListing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.cna.first_name}"

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    cna = models.ForeignKey(CNAListing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.cna.first_name}"
