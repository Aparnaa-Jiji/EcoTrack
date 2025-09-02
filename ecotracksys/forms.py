# miniproject/ecotrack/ecotracksys/forms.py
from django import forms

from accounts.models import CustomUser
from .models import Complaint, Collector, PickupRequest

# =========================
# ComplaintForm
# =========================
from django import forms
from .models import Complaint, PickupRequest

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'complaint_type', 'related_pickup', 'description', 'photo']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'complaint_type': forms.Select(attrs={'class': 'form-control'}),
            'related_pickup': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your complaint'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# =========================
# CollectorForm
# =========================
class CollectorForm(forms.ModelForm):
    """
    ModelForm for Collector with phone, name, and zone validation.
    """

    class Meta:
        model = Collector
        fields = [
            'name',
            'phone',
            'zone',
            'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Collector Name',
                'maxlength': 120,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'maxlength': 20,
            }),
            'zone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Operational Zone',
                'maxlength': 120,
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean_phone(self):
        """
        Ensure the phone number contains only digits and optional '+'.
        """
        phone = self.cleaned_data.get('phone')
        if phone and not all(c.isdigit() or c == '+' for c in phone):
            raise forms.ValidationError("Phone number must contain only digits and optional '+'.")
        return phone

    def clean_name(self):
        """
        Ensure the collector's name is alphabetic and non-empty.
        """
        name = self.cleaned_data.get('name')
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError("Name must contain only letters and spaces.")
        return name.strip()

    def clean_zone(self):
        """
        Ensure the zone is not empty and contains only valid characters.
        """
        zone = self.cleaned_data.get('zone')
        if not zone:
            raise forms.ValidationError("Zone cannot be empty.")
        if not all(c.isalnum() or c in [' ', '-', '_'] for c in zone):
            raise forms.ValidationError("Zone can only contain letters, numbers, spaces, hyphens, or underscores.")
        return zone.strip()

# ecotracksys/forms.py
from django import forms
from .models import Zone

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'ward', 'collector', 'lat_min', 'lat_max', 'lng_min', 'lng_max']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ward': forms.TextInput(attrs={'class': 'form-control'}),
            'collector': forms.Select(attrs={'class': 'form-control'}),
            'lat_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'lat_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'lng_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'lng_max': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone', 'profile_image']  # exclude email
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone
