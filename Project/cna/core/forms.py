from django import forms
from .models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import CNAListing
from .models import WeeklyJobSummary
from .models import Review

class CustomUserCreationForm(UserCreationForm):
    account_type = forms.ChoiceField(
        choices=[('CNA', 'I am a CNA (create a listing)'), ('Client', 'I am looking for care (browse CNAs)')],
        required=True,
        widget=forms.RadioSelect,
        label="Account Type"
    )

    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2', 'account_type']

    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password",
    )
    
    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get("account_type")
        
        if not account_type:
            raise forms.ValidationError("Please select at least one profile type: CNA or Client.")
        
        return cleaned_data
    
class CNAListingForm(forms.ModelForm):
    class Meta:
        model = CNAListing
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'hourly_rate', 'experience', 'location', 'availability']

class WeeklyJobSummaryForm(forms.ModelForm):
    class Meta:
        model = WeeklyJobSummary
        fields = ['client_name', 'week_of', 'total_hours', 'pay_rate', 'notes']
        widgets = {
            'week_of': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional comment'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional comment'}),
        }