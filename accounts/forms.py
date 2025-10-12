#miniproject/ecotrack/accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import CustomUser


# ------------------------
# Validators
# ------------------------
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Enter a valid Mobile number"
)

name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message="Name must contain only letters and spaces."
)


# ------------------------
# Custom Registration Form
# ------------------------
class CustomUserRegistrationForm(UserCreationForm):
    """
    Registration form for CustomUser.
    Extends UserCreationForm to add:
    - Name
    - Phone
    - Profile image
    """

    name = forms.CharField(
        max_length=100,
        required=True,
        validators=[name_validator],
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'phone', 'profile_image', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        # ✅ Assign all custom fields
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']  
        user.phone = self.cleaned_data.get('phone', '')
        user.role = 'citizen' 

        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
        user.role = 'citizen'
        if commit:
            user.save()
        return user