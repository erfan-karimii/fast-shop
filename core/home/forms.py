from django import forms
from .models import ContectUsKeeprt

class ContactUsKeeperForm(forms.ModelForm):
    class Meta:
        model = ContectUsKeeprt
        fields = '__all__'