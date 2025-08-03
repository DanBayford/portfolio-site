from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.db.models import Q
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TagBase, ItemBase
from wagtail import blocks
from wagtail.models import Page
from wagtail.images.blocks import ImageBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from .blocks import CodeSnippetBlock

# Add search functionality
class BlogIndexPage(Page):
    template = "blog/index.html"
    parent_page_types = ["pages.HomePage"]
    subpage_types = ["blog.BlogPostPage"]
    paginate_by = 2

    # Page content
    body = RichTextField(blank=True)

    # CMS config
    content_panels = Page.content_panels + ["body"]

    class Meta:
        verbose_name = "Blog Index"

    def __str__(self):
        return "Blog Index Page"

    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)

        # Get all posts
        posts = (
            BlogPostPage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
        )

        # Filter by tags if required
        selected_tags = request.GET.getlist("tag", "")
        print('selected_tags', selected_tags)

        if selected_tags:
            tags = BlogTag.objects.filter(slug__in=selected_tags)
            tag_query = Q()
            for tag in tags:
                tag_query |= Q(tags=tag)
            posts = posts.filter(tag_query).distinct()

        # Paginate if required
        page_number = request.GET.get("page")

        paginator = Paginator(posts, self.paginate_by)

        try:
            paginated_posts = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_posts = paginator.page(1)
        except EmptyPage:
            paginated_posts = paginator.page(paginator.num_pages)

        ctx["posts"] = paginated_posts
        ctx["selected_tags"] = selected_tags
        ctx["all_tags"] = BlogTag.objects.all()

        return ctx


"""
Content

Headings
Images
Code blocks
Links
(Streamfield)
"""


class BlogPostPage(Page):
    template = "blog/post.html"
    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    # Page content
    preview = RichTextField(
        blank=False,
        default="Please fill me in",
        help_text="Used on home page to preview post",
    )
    body = StreamField(
        [
            ("heading", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageBlock()),
            ("about_block", CodeSnippetBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    tags = ClusterTaggableManager(through="blog.TaggedBlog", blank=True)

    # CMS config
    content_panels = Page.content_panels + [FieldPanel("preview"), FieldPanel("body")]

    promote_panels = Page.promote_panels + [
        FieldPanel("tags"),
    ]

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return f"Blog Post Page - {self.title}"

    # [TODO] - replace with preview field
    def content_preview(self):
        return self.body


"""
Tags only available for Blog post pages
Connected to BlogPostPage via TaggedBlog join table below
"""


@register_snippet
class BlogTag(TagBase):
    free_tagging = (
        False  # Editors cannot create new tags on demand - ony via snippets admin page
    )

    class Meta:
        verbose_name = "Blog tag"
        verbose_name_plural = "Blog tags"


class TaggedBlog(ItemBase):
    tag = models.ForeignKey(
        BlogTag, related_name="tagged_blogs", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to="blog.BlogPostPage", on_delete=models.CASCADE, related_name="tagged_items"
    )
