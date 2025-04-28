from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_cna', 'is_client']
        
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
        is_cna = cleaned_data.get("is_cna")
        is_client = cleaned_data.get("is_client")
        
        # Ensure that the user can only select one profile type: CNA or Client
        if is_cna and is_client:
            raise forms.ValidationError("A user cannot be both a CNA and a Client.")
        
        # Ensure that at least one profile type is selected
        if not is_cna and not is_client:
            raise forms.ValidationError("Please select at least one profile type: CNA or Client.")
        
        return cleaned_data
