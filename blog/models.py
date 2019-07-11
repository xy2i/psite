from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

from markdownx.models import MarkdownxField


def get_upload_path(instance, filename):
    """ Find the upload path of the background_image dynamically."""
    return "%s/%s" % (instance.slug, 'bg_image.png')


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_draft=False, published_date__lte=timezone.now())


class Post(models.Model):
    # Data definition
    title = models.TextField()
    description = models.TextField()
    content = MarkdownxField()
    is_draft = models.BooleanField(default=False) # Either Draft or Published
    published_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=255, blank=True)
    background_image = models.ImageField(upload_to=get_upload_path)

    # PostQuerySet becomes the manager
    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

    # TODO: fix this mess
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        super(Post, self).save(*args, **kwargs)

    def make_published(self):
        """ Turns an unpublished Post into a published one.
        If the Post is already published, do nothing.
        """
        self.published_date = timezone.now()
        self.is_draft = False
        self.save()