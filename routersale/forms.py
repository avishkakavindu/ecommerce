from django import forms
from store_app.models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'country', 'address', 'city', 'state', 'postcode', 'phone', 'email', 'amount', 'payment_id']
