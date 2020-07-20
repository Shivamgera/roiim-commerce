from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as django_forms

User = get_user_model()


class SignupForm(forms.ModelForm):
    required_css_class = 'required'
    email = forms.EmailField(
        label="Email Address",
        error_messages={
            "unique": (
                "Registration error")
        }
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, request=None, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user

class LoginForm(django_forms.AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)