import logging

from django.conf import settings
from google.appengine.api import images


logger = logging.getLogger(__name__)


def op_max(args):
    """max-1000x500 fit within the given dimensions."""
    w, h = args.split("x")
    largest = max(int(w), int(h))

    return f"s{largest}"


def op_width(args):
    """width-640 reduces the width to the given size."""
    return f"w{args}"


def op_height(args):
    """height-480 reduces the height to the given size."""
    return f"h{args}"


def op_fill(args):
    """fill-200x200 resize and crop to the exact dimensions."""
    w, _, h = args.partition('x')

    return f"w{w}-h{h}-c"


def op_format(args):
    """format-jpeg output jpeg/png/gif (default png)."""
    formats = {
        "jpeg": "rj",
        "png": "rp",
        "gif": "rg",
        "webp": "rw",
        "webp-lossless": "rw",
    }

    return formats[args]


def op_original(args):
    """original renders the image at its original size."""
    return "s0"


def op_jpegquality(args):
    """jpegquality-40 set the JPEG image quality."""
    return f"l{args}"


def google_filter_params(filter_spec):
    """Convert a Wagtail filter to a map of the equivalent Google operations."""
    # The spec pattern is operation1-var1-var2|operation2-var1
    # Images API operations are not documented (except for s00)
    # https://stackoverflow.com/questions/25148567/list-of-all-the-app-engine-images-service-get-serving-url-uri-options

    # Map Wagtail operations to the Google images URL equivalent.
    operations_map = {
        "max": op_max,
        # min-500x200 cover the given dimensions
        "width": op_width,
        "height": op_height,
        "fill": op_fill,
        # fill-200x200-c100 resize and crop towards the focal point
        # scale-50 resize the image to the percentage specified
        "original": op_original,
        "format": op_format,
        # bgcolor-000 background color
        "jpegquality": op_jpegquality,
        # webpquality-50
    }

    operations = {}

    for spec in filter_spec.split("|"):
        op, _, args = spec.partition("-")

        try:
            func = operations_map[op]
        except KeyError:
            continue

        try:
            google_op = func(args)
            operations[op] = google_op
        except Exception:
            pass

    return operations


def google_filter_spec(filter_spec):
    """Convert a Wagtail filter to the equivalent Google images URL spec."""
    params = google_filter_params(filter_spec)
    default_quality = getattr(settings, "WAGTAILIMAGES_JPEG_QUALITY", None)

    if default_quality and "jpegquality" not in params:
        # settings.WAGTAILIMAGES_JPEG_QUALITY
        # settings.WAGTAILIMAGES_WEBP_QUALITY
        params["jpegquality"] = op_jpegquality(default_quality)

    return "-".join(params.values())


def google_image_url(fileobj, bucket):
    # Public URL is like
    # https://storage.googleapis.com/[bucket]/[prefix]/original_images/[filename]
    public_url = fileobj.url
    _, _, path = public_url.partition(bucket)

    if not path:
        logger.error("Image URL failed. Bucket not in path %r", public_url)
        return ""

    filename = f"/gs/{bucket}{path}"

    try:
        return images.get_serving_url(None, filename=filename, secure_url=True)
    except images.ObjectNotFoundError as err:
        logger.error("Image URL failed. %r, %r", filename, err)
        return ""
