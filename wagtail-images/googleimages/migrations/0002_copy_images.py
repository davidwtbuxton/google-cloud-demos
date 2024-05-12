# Generated by Django 4.2.3 on 2023-09-20 09:28

from django.db import migrations

from googleimages.management.commands import googleimages_copy


def copy_images(apps, schema_editor):
    """Copy existing images from Wagtail's image model to our custom model."""
    # wagtailimages.Image is the name for wagtail.images.models.Image.
    SrcModel = apps.get_model("wagtailimages", "Image")
    DestModel = apps.get_model("googleimages", "GoogleImage")

    googleimages_copy.convert_images(SrcModel, DestModel)


# Reset sequence IDs to avoid "Key (id)=(1) already exists" error when adding
# a new image after copying all the old images over. This SQL is enerated
# using `./manage.py sqlsequencereset googleimages`. Works both for migrating
# forwards and backwards.
reset_sequence = """
SELECT setval(pg_get_serial_sequence('"googleimages_googleimage"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "googleimages_googleimage";
SELECT setval(pg_get_serial_sequence('"googleimages_rendition"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "googleimages_rendition";
"""


class Migration(migrations.Migration):
    dependencies = [
        ("googleimages", "0001_initial"),
        ("wagtailimages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_images, migrations.RunPython.noop),
        migrations.RunSQL(reset_sequence, reset_sequence),
    ]