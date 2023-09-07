from django import forms
from .models import Order


class NewOrderForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())


class CheckOrderFields(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("first_name","last_name","address",
                  "phone_number","zip_code","national_code")
