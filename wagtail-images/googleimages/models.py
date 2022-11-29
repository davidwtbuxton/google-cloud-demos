import logging

from django.conf import settings
from django.db import models
from wagtail.images.models import Image as WagtailImage, AbstractImage, AbstractRendition

from . import operations


logger = logging.getLogger(__name__)


class GoogleImage(AbstractImage):
    google_url = models.CharField(max_length=250, blank=True)

    admin_form_fields = WagtailImage.admin_form_fields + (
        "google_url",
    )

    def get_rendition(self, filter):
        if not self.google_url:
            bucket = settings.GS_BUCKET_NAME
            self.google_url = operations.google_image_url(self.file, bucket)
            self.save(update_fields=["google_url"])

        # We want just the spec string.
        filter = getattr(filter, "spec", filter)
        Rendition = self.get_rendition_model()

        # We never actually record the renditions since the images service
        # renders everything on-the-fly then caches the result itself. This
        # means Image.objects.prefetch_renditions(..) does nothing.
        return Rendition(image=self, filter_spec=filter)

    def find_existing_rendition(self, filter):
        return self.get_rendition(filter)


class Rendition(AbstractRendition):
    image = models.ForeignKey(GoogleImage, on_delete=models.DO_NOTHING, related_name="renditions")

    class Meta:
        unique_together = [
            ("image", "filter_spec", "focal_point_key"),
        ]

    @property
    def url(self):
        spec = operations.google_filter_spec(self.filter_spec)

        return f"{self.image.google_url}={spec}"
