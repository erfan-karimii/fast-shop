from django.contrib.auth.password_validation import validate_password
from typing import Any, Dict
from django import forms
from .models import User , Profile

    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(max_length=255,)
    class Meta:
        model = User
        fields = ['email','password','password2']
    
    def clean(self) -> Dict[str, Any]:
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError({'password':'پسورد اول و دوم وارد شده یکی نمی باشد.'})

        try :
            password = self.cleaned_data['password']
            validate_password(password)
        except forms.ValidationError as e:
            raise forms.ValidationError({'password':list(e.messages)})
        return super().clean()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class ResetPassword(forms.Form):
    last_password = forms.CharField(max_length=255,)
    password = forms.CharField(max_length=255,)
    password2 = forms.CharField(max_length=255,)
    
    def clean(self) -> Dict[str, Any]:
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError({'password':'پسورد اول و دوم وارد شده یکی نمی باشد.'})

        try :
            password = self.cleaned_data['password']
            validate_password(password)
        except forms.ValidationError as e:
            raise forms.ValidationError({'password':list(e.messages)})
        return super().clean()