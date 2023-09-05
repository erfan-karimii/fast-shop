from django import forms


class NewOrderForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())