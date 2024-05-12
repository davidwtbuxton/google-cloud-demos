"""
A custom image model that uses Google's Images API to generate renditions.

When running locally, this model switches behaviour to use the Wagtail base
image implementation (does not use the Images API), but still has extra fields.
"""

import logging
import os
import mimetypes

from django.conf import settings
from django.core.files import File
from django.db import IntegrityError, models
from wagtail.images.models import AbstractImage, AbstractRendition, Filter
from wagtail.images.models import Image as WagtailImage

from . import operations

logger = logging.getLogger(__name__)


def on_app_engine():
    """True if it looks like the application is deployed on App Engine."""
    return os.environ.get("GAE_ENV", "") == "standard"


class GoogleImage(AbstractImage):
    google_url = models.CharField(max_length=250, blank=True, editable=False)
    alt_text = models.TextField(blank=True)

    admin_form_fields = WagtailImage.admin_form_fields + ("alt_text",)

    # Local development cannot generate serving URLs with the Images API.
    if on_app_engine():

        def create_rendition(self, filter: Filter) -> AbstractRendition:
            """Create an Images API serving URL on first use."""
            if not self.google_url and is_supported_image_type(self.file.name):
                bucket = settings.GS_BUCKET_NAME
                self.google_url = operations.google_image_url(self.file, bucket)

                try:
                    self.save(update_fields=["google_url"])
                except IntegrityError:
                    # Can fail here if 2 threads fetch the FIFE URL at the same
                    # time. Ignore it.
                    logger.exception(
                        "Failed to update %r, google_url=%r", self, self.google_url
                    )

            return super().create_rendition(filter)

    # Allow local development to do Images API resizing if we already have a
    # serving URL (like if you copy content from a production database).
    def generate_rendition_file(self, filter: Filter, *, source: File = None) -> File:
        if self.google_url:
            # If google_url is set, we have an Images API serving URL. We
            # can skip rendering the image.
            return

        return super().generate_rendition_file(filter, source=source)


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        GoogleImage, on_delete=models.CASCADE, related_name="renditions"
    )
    google_url = models.CharField(max_length=250, blank=True)

    class Meta:
        unique_together = [("image", "filter_spec", "focal_point_key")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimization: save the final serving URL in this rendition.
        self.google_url = google_url_for_rendition(
            self.image.google_url, self.filter_spec
        )
        if self.google_url and not self.width:
            # Django / Wagtail set the image dimensions by reading the rendition
            # file as part of the instance pre-save. We don't have a file!
            self.width, self.height = get_dimensions(self.image, self.filter_spec)

    @property
    def url(self) -> str:
        """Use the Images API URL, else use Wagtail's URL logic.

        The google_url field will only be set if this rendition is for a valid
        GoogleImage that can be served by the Images API (e.g. not an svg).
        """
        return self.google_url if self.google_url else super().url


def is_supported_image_type(filename: str) -> bool:
    """True if this filename can be served by the Images API.

    SVG is NOT supported.
    """
    supported_content_types = {
        "image/bmp",
        "image/gif",
        "image/heic",
        "image/heif",
        "image/jpeg",
        "image/png",
        "image/tiff",
        "image/vnd.microsoft.icon",
        "image/webp",
        "image/x-icon",
    }
    # Not strict, because image/webp is not defined on older Linux.
    content_type, _ = mimetypes.guess_type(filename, strict=False)

    return content_type in supported_content_types


def google_url_for_rendition(base_url: str, filter_spec: Filter) -> str:
    """Construct an Images API serving URL with transform paramters.

    The base URL will be an empty string if this rendition cannot be served by
    the Images API (e.g. an svg).
    """
    if base_url and filter_spec:
        google_params = operations.google_filter_spec(filter_spec)
        return f"{base_url}={google_params}"

    return base_url


def get_dimensions(image: GoogleImage, filter_spec: str) -> tuple[int, int]:
    """Calculate width x height for an image after transforms are applied."""
    # But we don't want to do the actual transforms.
    transform = Filter(filter_spec).get_transform(image)

    return transform.size
