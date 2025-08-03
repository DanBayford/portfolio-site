from django.core.exceptions import ValidationError


class SinglePageMixin:
    """
    Method over riding of clean method to prevent more than one instance of a particular type of page (ie an About page) being created
    """

    def clean(self):
        super().clean()
        if (
            self.__class__.objects.exists() and not self.pk
        ):  # Check for existing pk as this may be an update save, rather than a create save (ie no pk yet)
            raise ValidationError(
                f"Only one instance of {self.__class__.__name__} is allowed"
            )
