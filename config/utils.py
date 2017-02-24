from django.utils import timezone
from django.utils.text import slugify


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
