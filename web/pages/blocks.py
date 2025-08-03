from wagtail import blocks


class AboutItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Project or role title")
    description = blocks.RichTextBlock(required=False, help_text="Project description")
    url = blocks.URLBlock(required=False, help_text="Link to the project or company")
    start_date = blocks.DateBlock(required=True, help_text="Start date")
    end_date = blocks.DateBlock(
        required=False, help_text="End date (leave blank if current)"
    )
    is_current = blocks.BooleanBlock(
        required=False, default=False, help_text="Current position?"
    )

    class Meta:
        template = "blocks/about_item.html"
        icon = "doc-full"
        label = "About Item"
