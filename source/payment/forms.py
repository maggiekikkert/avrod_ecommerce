from django import forms
from django.forms import ModelForm
from payment.models import Customer

# class PaymentForm(forms.Form):
#     model = Customer
#     cardholder = forms.CharField(max_length=30, required=False)