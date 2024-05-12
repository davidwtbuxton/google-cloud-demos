Wagtail with Google's images service
====================================

Code for a [Wagtail custom image model][1] that uses [Google's images service][2], with files saved in a Google Cloud Storage bucket (using [django-storages][3]).

This allows you to upload images in the Wagtail CMS, which are then stored in a GCS bucket, but the image rendition is created and served by the Google Images API. The Images API is very high performance, and supports resizing images with URL parameters.


Installation
------------

The Cloud Storage bucket must have per-object ACLs enabled. The Images API does not work if the bucket has [uniform bucket-level access][4] enabled.

- Add "django-storages[google]' and 'appengine-python-standard' to your app's Python dependencies.
- Add `app_engine_apis: true` in app.yaml.
- Add the [App Engine bundled services WSGI wrapper][5].
- Add "googleimages" to Django's INSTALLED_APPS setting.
- [Configure Django's settings for django-storages][6], including `GS_BUCKET_NAME`.
- Update Django's settings: `WAGTAILIMAGES_IMAGE_MODEL = "googleimages.GoogleImage"`
- Replace `wagtail.images.models.Image` with `googleimages.GoogleImage` in your models.
- Run database migrations. This includes a data migration that copies existing data from wagtailimages.Image models to googleimages.GoogleImage models.

The data migration uses a Postgres-specific SQL function to reset sequence IDs.

The Images API does not support SVGs. This code will fall back to Wagtails's default behaviour for SVSs.

For local development, this code will not call the Images API, but will fall back to Wagtail's default behaviour.


Jinja2 templates
----------------

A custom image template function is included, which supports the same arguments as [Wagtail's image tag][7], and always caches the tag output for performance.

Add "googleimages.jinja2tags.images" to Jinja extensions in your Django
settings:

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.jinja2.Jinja2",
            "DIRS": [],
            "OPTIONS": {"extensions": ["googleimages.jinja2tags.images"]},
        },
    ]

In your templates, use it like:

    {{ image(page.photo, "width-400") }}


[1]: https://docs.wagtail.org/en/stable/advanced_topics/images/custom_image_model.html
[2]: https://cloud.google.com/appengine/docs/legacy/standard/python/images
[3]: https://django-storages.readthedocs.io/
[4]: https://cloud.google.com/storage/docs/uniform-bucket-level-access
[5]: https://github.com/GoogleCloudPlatform/appengine-python-standard
[6]: https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
[7]: https://docs.wagtail.org/en/stable/topics/images.html
