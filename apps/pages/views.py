from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from apps.products.models import Product
from .forms import ContactForm

# Create your views here.
def home(request):
	title = 'Sign Up Now'

	products = Product.objects.all().order_by("?")[:6]
	products2 = Product.objects.all().order_by("?")[:6]

	context = {
		"title": title,
		"products":products,
		"products2":products2
	}

	# return render(request, "theme_default/pages/home.html", context)
	return render(request, "theme_lotus/pages/home.html", context)
	# return render(request, "theme_lotus/pages/detail.html", context)
	# return render(request, "theme_lotus/pages/products.html", context)



def contact(request):
	title = 'Contact Us'
	title_align_center = True
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'youotheremail@email.com']
		contact_message = "%s: %s via %s"%( 
				form_full_name, 
				form_message, 
				form_email)
		some_html_message = """
		<h1>hello</h1>
		"""
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				html_message=some_html_message,
				fail_silently=True)

	context = {
		"form": form,
		"title": title,
		"title_align_center": title_align_center,
	}
	return render(request, "theme_default/pages/forms.html", context)
















