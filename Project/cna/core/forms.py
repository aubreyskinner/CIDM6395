from django import forms
from .models import User  # Import your custom User model
from django.contrib.auth.forms import UserCreationForm
from .models import CNAListing
from .models import WeeklyJobSummary

class CustomUserCreationForm(UserCreationForm):
    account_type = forms.ChoiceField(
        choices=[('CNA', 'I am a CNA (create a listing)'), ('Client', 'I am looking for care (browse CNAs)')],
        required=True,
        widget=forms.RadioSelect,
        label="Account Type"
    )

    class Meta:
        model = User  # Reference your custom User model here
        fields = ['username', 'password1', 'password2', 'account_type']

    # Add custom logic for password fields
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
        
        # Ensure that at least one profile type is selected
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