from django.utils import timezone
from django.utils.text import slugify

def jwt_response_payload_handler(token, user, request, *args, **kwargs):
	data = {
		"token": token,
		"user": user.id,
		"orig_iat": timezone.now(),
		#"user_braintree_id": UserCheckout.objects.get(user=user).get_braintree_id
	}
	return data


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	model_class = type(instance)
	qs = model_class.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" % (slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug
