from django.contrib.auth.password_validation import validate_password
from typing import Any, Dict
from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','password']
    
    def clean(self) -> Dict[str, Any]:

        try :
            password = self.cleaned_data['password']
            validate_password(password)
        except forms.ValidationError as e:
            raise forms.ValidationError({'password':list(e.messages)})
        return super().clean()
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    