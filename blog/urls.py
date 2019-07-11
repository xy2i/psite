from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from blog.views import Index, DetailPost

app_name = 'blog'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:post_slug>/', DetailPost.as_view(), name='post'),
]

# Serve files locally if not in prod
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)