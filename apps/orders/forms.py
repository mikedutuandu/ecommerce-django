from django import forms
from django.contrib.auth import get_user_model

from apps.accounts.models import UserAddress
User = get_user_model()




class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserAddress
		fields = [
			'fullname',
			'phone',
			'city',
			'district',
			'wards',
			'street',
		]





