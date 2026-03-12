from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# ==============================
# 1️⃣ Email Login Form
# ==============================


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")

            if not user.check_password(password):
                raise forms.ValidationError("Invalid email or password")

            if not user.is_active:
                raise forms.ValidationError("Account is inactive")

            # ✅ VERY IMPORTANT (fixes your error)
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            self.user = user

        return cleaned_data

    def get_user(self):
        return getattr(self, "user", None)


# ==============================
# 2️⃣ Custom Signup Form
# ==============================

class CustomSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # email as username
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user