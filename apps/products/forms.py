from django import forms

from django.forms.models import modelformset_factory


from .models import  Category


CAT_CHOICES = (
	('electronics', 'Electronics'),
	('accessories', 'Accessories'),
)

class ProductFilterForm(forms.Form):
	q = forms.CharField(label='Search', required=False)
	category_id = forms.ModelMultipleChoiceField(
		label='Category',
		queryset=Category.objects.all(), 
		widget=forms.CheckboxSelectMultiple, 
		required=False)
	# category_title = forms.ChoiceField(
	# 	label='Category',
	# 	choices=CAT_CHOICES,
	# 	widget=forms.CheckboxSelectMultiple,
	# 	required=False)
	max_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)
	min_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)
