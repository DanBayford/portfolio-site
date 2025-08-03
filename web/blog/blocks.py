from wagtail import blocks


class CodeSnippetBlock(blocks.StructBlock):
    LANGUAGE_CHOICES = (
        ("python", "Python"),
        ("javascript", "JavaScript"),
        ("docker", "Docker"),
    )
    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES, required=True, help_text="")
    content = blocks.TextBlock(required=True, help_text="The code snippet")
    caption = blocks.CharBlock(required=False, help_text="Caption for code snippet")

    class Meta:
        template = "blocks/code_snippet.html"
        icon = "code"
        label = "Code Snippet"
