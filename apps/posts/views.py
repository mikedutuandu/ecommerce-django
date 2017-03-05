from .models import Post
from django.views.generic import DetailView,ListView


class PostDetailView(DetailView):
    model = Post
    template_name = "theme_lotus/posts/post_detail.html"


class PostListView(ListView):
    queryset = Post.objects.active()
    template_name = "theme_lotus/posts/post_list.html"


