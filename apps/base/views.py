from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, View, TemplateResponseMixin, ContextMixin
from apps.products.models import Product,Category
from .forms import ContactForm


class HomeView(View):
    template_name = "theme_lotus/base/home.html"
    def get(self, request, *args, **kwargs):
        context = {}
        context['sections'] = []
        categories = Category.objects.filter(active=True)
        for category in categories:
            products = Product.objects.filter(default=category)[:8]
            context['sections'].append({"cat":category.title,"products":products})
        return render(request,self.template_name,context)





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
        contact_message = "%s: %s via %s" % (
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
    return render(request, "theme_default/base/forms.html", context)
