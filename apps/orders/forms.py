from django import forms
from django.contrib.auth import get_user_model

from apps.accounts.models import UserAddress
User = get_user_model()




class UserAddressForm(forms.ModelForm):
	fullname = forms.CharField(required=True,
							widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input', 'placeholder': ''}),label='Họ tên')
	phone = forms.IntegerField(required=True,
							widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input', 'placeholder': ''}),
							   label='Điện thoại di động')
	city = forms.CharField(required=True,
							widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input', 'placeholder': ''}),
						   label='Tỉnh/Thành phố')
	district = forms.CharField(required=True,
							widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input', 'placeholder': ''}),
							   label='Quận/Huyện')
	wards = forms.CharField(required=True,
							widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input', 'placeholder': ''}),
							label='Phường/Xã')
	street = forms.CharField(required=True,
							widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input', 'placeholder': ''}),
							 label='Địa chỉ')
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
	# def clean_fullname(self):
	# 	pass
	#     # data = self.cleaned_data['title']
	#     # if "fred@example.com" != data:
	#     raise forms.ValidationError("You have forgotten about Fred!")
	#     # return data





