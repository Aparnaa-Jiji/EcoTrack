# miniproject/ecotrack/ecotracksys/forms.py
from django import forms

from accounts.models import CustomUser
from .models import Complaint, Collector, PickupRequest

# =========================
# ComplaintForm
# =========================
from django import forms
from .models import Complaint

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

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if photo:
            # ✅ File size check (max 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must not exceed 5 MB.")

            # ✅ File type check
            valid_types = ["image/jpeg", "image/png"]
            if hasattr(photo, "content_type") and photo.content_type not in valid_types:
                raise forms.ValidationError("Only JPG and PNG formats are allowed.")

        return photo


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



# ecotracksys/forms.py
# core/forms.py
from django import forms
from .models import Zone
from accounts.models import CustomUser



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
    if phone:
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
    return phone



# ecotracksys/forms.py
from django import forms
from accounts.models import CustomUser
from django import forms
from accounts.models import CustomUser

from django import forms
from django.contrib.auth import update_session_auth_hash
from accounts.models import CustomUser

class AdminProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,  # optional
        widget=forms.PasswordInput(render_value=False,attrs={'placeholder': '••••••••'}),
        help_text="Leave blank if you don't want to change the password"
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'profile_image',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make name and email read-only
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

    def save(self, request=None, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        password_changed = False
        if password:
            user.set_password(password)  # hash password only if provided
            password_changed = True
        if commit:
            user.save()
            if request and password_changed:
                # Update session hash if password changed so user won't be logged out
                update_session_auth_hash(request, user)
        return user
# ecotracksys/forms.py
from django import forms
from accounts.models import CustomUser
from django.contrib.auth import update_session_auth_hash

class CollectorProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=False, attrs={'placeholder': '••••••••'}),
        help_text="Leave blank if you don't want to change the password"
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'profile_image']  # email included

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email read-only
        self.fields['email'].widget.attrs['readonly'] = True
        # Make phone read-only
        self.fields['phone'].widget.attrs['readonly'] = True

    def save(self, request=None, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        password_changed = False
        if password:
            user.set_password(password)
            password_changed = True
        if commit:
            user.save()
            if request and password_changed:
                update_session_auth_hash(request, user)  # prevent logout
        return user
