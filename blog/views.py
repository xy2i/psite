from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from blog.models import Post
from django.db import models
from django.urls import reverse
from django.core.cache import cache

from .markdown_wrap import markdown

# TODO: There's something terribly wrong here... but how to place it in the right place?
def limit_to_published(request) -> models.QuerySet:
    posts = Post.objects.all()
    # If not a superuser...
    if not request.user.is_superuser:
        posts = posts.published()  # limit our query to only published objects

    return posts


class Index(ListView):
    model = Post
    template_name = 'blog/index.html'

    def get(self, request, *args, **kwargs):
        posts = limit_to_published(request)
        context = {'post_list': posts}
        return render(request, self.template_name, context)

class DetailPost(DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get(self, request, *args, **kwargs):
        post_list = limit_to_published(request)
        post_slug = self.kwargs['post_slug']
        cache_key = reverse('blog:post', args=[post_slug]) # use our cache key as the URL
        cache_time = 86400
        post = cache.get(cache_key) # if the pots doens't exist, return None

        if True:
            post = get_object_or_404(post_list, slug=post_slug)
            # Use our markdown wrapper defined in markdown_wrap.py
            post.content = markdown(post.content)  # Make the post rendered
            cache.set(cache_key, post, cache_time)

        context = {'post': post}
        return render(request, 'blog/show_post.html', context)