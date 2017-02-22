from django import forms
from django.contrib.auth import get_user_model

from .models import UserAddress
User = get_user_model()


class AddressForm(forms.Form):
	shipping_address = forms.ModelChoiceField(
		queryset=UserAddress.objects.filter(type="shipping"),
		widget = forms.RadioSelect,
		empty_label = None,
		
		)



class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserAddress
		fields = [
			'street',
			'city',
			'state',
			'zipcode',
		]





