#ecotracksys/forms.py
from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'complaint_type', 'related_pickup', 'description', 'photo']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complaint Subject'}),
            'complaint_type': forms.Select(attrs={'class': 'form-control'}),
            'related_pickup': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pickup Request ID (optional)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your complaint'}),
        }
