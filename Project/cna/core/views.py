from rest_framework import viewsets
from .models import CNA, ClientProfile
from .serializers import CNASerializer, ClientProfileSerializer
from django.shortcuts import render
from .models import CNA
from .models import WeeklyJobSummary
from django.db.models import Avg, Count
from .forms import WeeklyJobSummaryForm
from .models import CNAListing
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
from .forms import CNAListingForm
from .models import CNAListing  # Make sure CNAListing is imported
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from .models import Notification
from .models import Review
from .forms import ReviewForm



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


def success(request):
    return render(request, 'success.html')

User = get_user_model()

@login_required
def contact_cna(request, cna_id):
    cna = get_object_or_404(CNAListing, pk=cna_id)

    if request.method == 'POST':
        cna_user = cna.user

        if cna_user:
            sender_name = request.POST.get('sender_name')
            sender_phone = request.POST.get('sender_phone')
            care_location = request.POST.get('care_location')
            care_hours = request.POST.get('care_hours')
            care_needs = request.POST.get('care_needs')

            # Now create a detailed notification
            full_message = (
                f"New service request from {sender_name} ({sender_phone}):\n"
                f"Location: {care_location}\n"
                f"Hours Needed: {care_hours}\n"
                f"Care Needs: {care_needs}"
            )

            Notification.objects.create(
                user=cna_user,
                message=full_message
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

from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Capture and print the account_type value
            account_type = form.cleaned_data.get('account_type')
            print(f"Account Type selected: {account_type}")  # Debug print

            # Now handle different types based on the selected account type
            if account_type == 'CNA':
                user.is_cna = True
                user.is_client = False
                user.save()
                return redirect('cna_dashboard')
            elif account_type == 'Client':
                user.is_cna = False
                user.is_client = True
                user.save()
                return redirect('client_dashboard')
            else:
                print("Unexpected account type: ", account_type)
                return redirect('home')
        else:
            print("Form errors:", form.errors)  # Print errors to debug

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
@login_required
def cna_dashboard(request):
    return render(request, 'cna_dashboard.html')  # Show CNA specific content

@login_required
def client_dashboard(request):
    return render(request, 'client_dashboard.html')  # Show Client specific content

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = CNAListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)  # Don't save immediately
            listing.user = request.user        # Link the listing to the logged-in user
            listing.save()                     # Now save
            return redirect('cna_list')         # Redirect after saving
    else:
        form = CNAListingForm()

    return render(request, 'create_listing.html', {'form': form})

@login_required
def cna_list(request):
    # Logic for showing available CNAs
    return render(request, 'cna_list.html')

from django.shortcuts import render, redirect
from .models import CNAListing
from .forms import CNAListingForm


def cna_list(request):
    cnas = CNAListing.objects.all()  # Fetch all CNA listings from the database
    return render(request, 'cna_list.html', {'cnas': cnas})

def cna_list(request):
    # Get filter parameters from GET request
    location_filter = request.GET.get('location', '')
    experience_filter = request.GET.get('experience', '')
    hourly_rate_filter = request.GET.get('hourly_rate', '')

    # Apply filters to the query if the filters are provided
    cnas = CNAListing.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )

    if location_filter:
        cnas = cnas.filter(location__icontains=location_filter)
    if experience_filter:
        cnas = cnas.filter(experience__icontains=experience_filter)
    if hourly_rate_filter:
        try:
            cnas = cnas.filter(hourly_rate__lte=float(hourly_rate_filter))
        except ValueError:
            pass  # If the filter is not a valid number, ignore the filter

    return render(request, 'cna_list.html', {'cnas': cnas})

@login_required
def cna_finance_dashboard(request):
    # Only show jobs for the logged-in CNA
    jobs = WeeklyJobSummary.objects.filter(user=request.user).order_by('-week_of')

    # Calculate total expected pay for all entries
    total_expected = sum(job.expected_pay for job in jobs)

    return render(request, 'cna_finance_dashboard.html', {
        'jobs': jobs,
        'total_expected': total_expected,
    })


@login_required
def add_job_summary(request):
    if request.method == 'POST':
        form = WeeklyJobSummaryForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user  # Assign to logged-in CNA
            job.save()
            return redirect('cna_finance_dashboard')
    else:
        form = WeeklyJobSummaryForm()

    return render(request, 'add_job_summary.html', {'form': form})

@login_required
def delete_job_summary(request, pk):
    job = get_object_or_404(WeeklyJobSummary, pk=pk, user=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('cna_finance_dashboard')
    return render(request, 'confirm_delete.html', {'job': job})


@login_required
def leave_review(request, cna_id):
    cna = get_object_or_404(CNAListing, pk=cna_id)

    # Optional: Prevent duplicate reviews from the same user
    if Review.objects.filter(reviewer=request.user, cna=cna).exists():
        return redirect('contact_cna', cna_id=cna.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.cna = cna
            review.save()
            return redirect('cna_list')
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'form': form, 'cna': cna})
