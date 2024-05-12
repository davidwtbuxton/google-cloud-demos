"""
Copy images from one database model to another.

For Wagtail's default image model, do:

    ./manage.py googleimages_copy wagtailimages.Image googleimages.GoogleImage
"""

import operator

from django.apps import registry
from django.core.management.base import BaseCommand
from django.utils.functional import partition


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("src")
        parser.add_argument("dest")

    def handle(self, *args, **options):
        # wagtailimages.Image is the default image model.
        SrcModel = registry.apps.get_model(options["src"])
        DestModel = registry.apps.get_model(options["dest"])

        convert_images(SrcModel, DestModel)


def find_common_fields(*models):
    """Fields common to the models, ignoring related object manager fields."""
    # This is simpler than trying to introspect field names and working out
    # which can be set directly (but less flexible).
    return [
        "id",
        "collection",
        "title",
        "file",
        "width",
        "height",
        "created_at",
        "uploaded_by_user",
        "focal_point_x",
        "focal_point_y",
        "focal_point_width",
        "focal_point_height",
        "file_size",
        "file_hash",
    ]


def convert_images(SrcModel, DestModel):
    """Copy the core properties from one image model table to another."""
    common_fields = find_common_fields(SrcModel, DestModel)
    getter = operator.attrgetter(*common_fields)

    batch = []

    for src_obj in SrcModel._base_manager.all():
        properties = dict(zip(common_fields, getter(src_obj)))
        dest_obj = DestModel(**properties)
        batch.append(dest_obj)

    # And then we need to do _update_ for existing rows, but _insert_ for
    # new rows.
    existing_dest_ids = set(DestModel._base_manager.values_list("pk", flat=True))

    def insert_or_update(obj):
        return obj.id in existing_dest_ids

    inserts, updates = partition(insert_or_update, batch)

    DestModel.objects.bulk_create(inserts, batch_size=1000)

    update_fields = list(common_fields)
    update_fields.remove("id")
    DestModel.objects.bulk_update(updates, update_fields, batch_size=1000)
