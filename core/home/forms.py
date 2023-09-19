from django import forms
from .models import ContectUsKeeprt
from captcha.fields import CaptchaField

class ContactUsKeeperForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = ContectUsKeeprt
        fields = ('first_name','last_name','phone_number','text','is_email_answer','captcha')

