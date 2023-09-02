from django.contrib.auth.password_validation import validate_password
from typing import Any, Dict
from django import forms
from .models import User

class LoginForm(forms.ModelForm):
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
    
    
    # def validate(self, attrs):
        
    #     try :
    #         password = attrs.get('password') 
    #         validate_password(password)
    #     except exceptions.ValidationError as e:
    #         raise serializers.ValidationError({'password':list(e.messages)})
    #     return super().validate(attrs)