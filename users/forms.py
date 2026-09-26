from django import forms
from users.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'is_hosteller', 'branch', 'year']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 XXXXXXXXXX'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={'min': 1, 'max': 8, 'placeholder': '1-8'}),
        }