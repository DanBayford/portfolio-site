from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel


@register_snippet
class SocialLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    light_icon = models.FileField(
        upload_to="social_icons/", help_text="Upload an SVG file (bg-neutral-600)"
    )
    dark_icon = models.FileField(
        upload_to="social_icons/", help_text="Upload an SVG file (bg-neutral-400)"
    )

    def __str__(self):
        return self.title

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        FieldPanel("light_icon"),
        FieldPanel("dark_icon"),
    ]
