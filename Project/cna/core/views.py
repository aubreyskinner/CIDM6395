from rest_framework import viewsets
from .models import CNA, ClientProfile
from .serializers import CNASerializer, ClientProfileSerializer
from django.shortcuts import render
from .models import CNA
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail



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
    return render(request, 'contact_cna.html', {'cna': cna})

# def contact_cna(request, cna_id):
    cna = get_object_or_404(CNA, pk=cna_id)

    if request.method == 'POST':
        send_mail(
            'New Service Request',
            'You have received a new service request from a potential client.',
            'your_email@example.com',  # From email address
            [cna.email],               # Send to CNA's email
            fail_silently=False,
        )
        return redirect('success')  # Redirect after sending the email

    return render(request, 'contact_cna.html', {'cna': cna})

# def success(request):
    return render(request, 'success.html')