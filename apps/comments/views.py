from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from apps.comments.forms import CommentForm
from apps.comments.models import Comment
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin



class CreateCommentView(LoginRequiredMixin,View):
    login_url = '/dang-nhap/'
    def post(self,request):
        form = CommentForm(request.POST or None)
        if form.is_valid() and request.user.is_authenticated():
            c_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=c_type)
            obj_id = form.cleaned_data.get('object_id')
            title_data = form.cleaned_data.get("title")
            content_data = form.cleaned_data.get("content")
            parent_obj = None
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=obj_id,
                content=content_data,
                parent=parent_obj,
                title=title_data,
            )
            return redirect(new_comment.content_object.get_absolute_url())



