from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail.admin.panels import FieldPanel
from utils.mixins import SinglePageMixin
from blog.models import BlogPostPage
from .blocks import AboutItemBlock


"""
Content:

Brief intro
Latest blog posts
Latest projects
"""


class HomePage(SinglePageMixin, Page):
    template = "pages/home.html"
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["pages.AboutPage", "blog.BlogIndexPage"]

    # Page content
    body = RichTextField(blank=True)

    # CMS config
    content_panels = Page.content_panels + ["body"]

    class Meta:
        verbose_name = "Home Page"

    def __str__(self):
        return "Home Page"

    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)
        ctx["latest_posts"] = BlogPostPage.objects.live().order_by(
            "-first_published_at"
        )[:5]
        return ctx


"""
Content:

About my career
Education
Hobbies and outside of work
(Streamfield)
Block for employment / uni (url, dates, content)
"""


class AboutPage(SinglePageMixin, Page):
    template = "pages/about.html"
    parent_page_types = ["pages.HomePage"]
    subpage_types = []

    # Page content
    body = StreamField(
        [
            ("heading", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageBlock()),
            ("about_block", AboutItemBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    # CMS config
    content_panels = Page.content_panels + [FieldPanel("body")]

    class Meta:
        verbose_name = "About Page"

    def __str__(self):
        return "About Page"
