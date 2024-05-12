from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.search import index


class HomePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


class BlogPage(Page):
    date = models.DateField('Post date')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields +[
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label="Gallery images")
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey("googleimages.GoogleImage", on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]
