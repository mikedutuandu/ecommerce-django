from .models import Post
from django.views.generic import DetailView,ListView
import random

class PostDetailView(DetailView):
    model = Post
    template_name = "theme_lotus/posts/post_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        context["related"] = sorted(Post.objects.get_related(instance)[:8], key=lambda x: random.random())
        return context


class PostListView(ListView):
    queryset = Post.objects.active()
    template_name = "theme_lotus/posts/post_list.html"


