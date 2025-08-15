from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import CustomUser

# ------------------------
# Validators
# ------------------------

# Ensures phone number format: optional '+' and country code, then 9–15 digits
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Enter a valid Mobile number"
)

# Ensures name contains only letters and spaces
name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message="Name must contain only letters and spaces."
)


# ------------------------
# Custom Registration Form
# Extends Django's UserCreationForm to include extra fields
# ------------------------
class CustomUserRegistrationForm(UserCreationForm):
    """
    Registration form for CustomUser.
    Includes:
    - Name (letters and spaces only)
    - Email (from User model)
    - Phone number (optional, validated format)
    - Profile image (optional)
    - Password & Confirm password (from UserCreationForm)
    """

    # Name field (required) with validation
    name = forms.CharField(
        max_length=100,
        required=True,
        validators=[name_validator],
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )

    # Phone number field (optional) with validation
    phone = forms.CharField(
        max_length=15,
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    # Profile image upload (optional)
    profile_image = forms.ImageField(required=False)

    class Meta:
        """
        Meta configuration for the form:
        - Model: CustomUser
        - Fields: Ordered list of fields displayed in the form
        """
        model = CustomUser
        fields = ('name', 'email', 'phone', 'profile_image', 'password1', 'password2')

    def save(self, commit=True):
        """
        Save the form data into a CustomUser instance.
        commit=True => save to database immediately.
        """
        # Create user object without saving to DB yet
        user = super().save(commit=False)

        # Assign custom fields
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data.get('phone', '')

        # Save profile image only if uploaded
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image

        # Save to DB if commit flag is True
        if commit:
            user.save()

        return user
