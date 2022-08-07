Wagtail with Google's images service
====================================

Sample code for a Wagtail custom image model that uses Google's image service, with files saved in a Google Cloud Storage bucket (using django-storages), instead of generating new images and serving directly from storage.

- Update your code to use the App Engine bundled services.
- Add "googleimages" to Django's INSTALLED_APPS setting.
- Add `WAGTAILIMAGES_IMAGE_MODEL = "googleimages.GoogleImage"` to settings.
- Replace `wagtail.images.models.Image` with `googleimages.GoogleImage` in your models.

Note that the custom image model does not save the Rendition instances to the database, which may break how some Wagtail sites use images.

Installing dependencies:

    $ pip install pip-tools
    $ pip-compile requirements.in
    $ pip-sync


- Wagtail custom image models: https://docs.wagtail.org/en/stable/advanced_topics/images/custom_image_model.html
- Django-storages: https://django-storages.readthedocs.io/
- Google images service: https://cloud.google.com/appengine/docs/legacy/standard/python/images#get-serving-url
- App Engine bundled services: https://github.com/GoogleCloudPlatform/appengine-python-standard
