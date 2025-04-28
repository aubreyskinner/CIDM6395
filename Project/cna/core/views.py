from rest_framework import viewsets
from .models import CNA, ClientProfile
from .serializers import CNASerializer, ClientProfileSerializer
from django.shortcuts import render
from .models import CNA
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login



class CNAViewSet(viewsets.ModelViewSet):
    queryset = CNA.objects.all()
    serializer_class = CNASerializer

class ClientProfileViewSet(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def cna_list(request):
    cnas = CNA.objects.all()
    return render(request, 'cna_list.html', {'cnas': cnas})

def contact_cna(request, cna_id):
    cna = get_object_or_404(CNA, pk=cna_id)

    if request.method == 'POST':
        # send a simple notification email to the CNA
        send_mail(
            subject=f"New Service Request",
            message="You have a new request for service—please log in to view details.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[cna.email],
            fail_silently=False,
        )
        return redirect('success')

    return render(request, 'contact_cna.html', {'cna': cna})


def success(request):
    return render(request, 'success.html')

User = get_user_model()

def contact_cna(request, cna_id):
    cna = get_object_or_404(CNA, pk=cna_id)

    if request.method == 'POST':
        # find the User account for this CNA (by email)
        try:
            cna_user = User.objects.get(email=cna.email)
        except User.DoesNotExist:
            cna_user = None

        if cna_user:
            Notification.objects.create(
                user=cna_user,
                message=f"You have a new service request from {request.user.username}."
            )

        return redirect('success')

    return render(request, 'contact_cna.html', {'cna': cna})

@login_required
def notification_page(request):
    qs = Notification.objects.filter(user=request.user).order_by('-timestamp')
    # mark all as read when the page is viewed
    qs.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': qs})

@login_required
def unread_notification_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration

            # Redirect based on user profile type
            if user.user_type == 'CNA':  # Check if user selected 'CNA' profile
                return redirect('home')  # Redirect to home page (or a specific page like create listing if needed)
            else:
                return redirect('home')  # Redirect to home page (or another page if needed)
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def create_listing(request):
    if request.user.user_type == 'CNA':
        # Logic to create a listing for CNAs
        return render(request, 'create_listing.html')
    else:
        return redirect('home')  # If not a CNA, redirect to home

def available_cnas(request):
    if request.user.user_type == 'Looking for Care':
        # Logic to show available CNAs
        return render(request, 'available_cnas.html')
    else:
        return redirect('home')  # If not 'Looking for Care', redirect to home