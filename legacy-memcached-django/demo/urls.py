from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

VIEW_CACHE_EXPIRES = 60  # Seconds.


# The same view is mapped to 2 paths, but /cache will be fast after it
# has warmed up.
urlpatterns = [
    path('cache', cache_page(VIEW_CACHE_EXPIRES)(views.slow)),
    path('', views.slow),
]
