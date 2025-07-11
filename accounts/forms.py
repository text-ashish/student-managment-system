from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label="Confirm Password"
    )
    role = forms.ChoiceField(
        choices=[(r[0], r[1]) for r in Profile.USER_ROLES if r[0] != 'admin'],

        widget=forms.Select(attrs={'class': 'form-input'}),
        required=True,
        label="Register As"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data
