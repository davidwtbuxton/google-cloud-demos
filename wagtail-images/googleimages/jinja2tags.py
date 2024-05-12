"""
Things for use with a Jinja2 template backend.

Add googleimages.jinja2tags.images to Jinja extensions in your Django
settings:

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.jinja2.Jinja2",
            "DIRS": [],
            "OPTIONS": {"extensions": ["googleimages.jinja2tags.images"]},
        },
    ]
"""

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils import safestring
from jinja2.ext import Extension
from wagtail.images.jinja2tags import image as wagtail_image
from wagtail.images.utils import to_svg_safe_spec


def image(image_, filterspec, **kwargs):
    """Like Wagtail's image tag, but with caching and SVG handling.

    All output is cached. SVG images are never rendered using the Google
    Images API (because it cannot render SVG).
    """
    # Use the image's database ID, because its __str__ may not be unique.
    vary_on = [image_.pk, filterspec, kwargs]
    # Key prefix something like 'template.cache.googleimages'.
    key = make_template_fragment_key("googleimages", vary_on)
    result = cache.get(key)

    if result:
        if isinstance(result, str):
            # App Engine memcache does not preserve the SafeString type.
            result = safestring.mark_safe(result)
    else:
        if image_.is_svg():
            # This removes operations that trigger a Pillow exception.
            filterspec = to_svg_safe_spec(filterspec)

        # This result is either a Rendition, or a SafeString, depending on if
        # there are extra <img> tag attributes. The templates depend on it
        # being a Rendition and having width and height attributes.
        result = wagtail_image(image_, filterspec, **kwargs)
        cache.set(key, result, timeout=None)  # Cache FOREVER.

    return result


class images(Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment.globals["image"] = image
