from django.db import models


# CHOICES CLASSES
class StatusChoices(models.TextChoices):
    ACTIVE = 1, "Active"
    INACTIVE = 2, "Inactive"
    DELETED = 3, "Deleted"
    BLOCKED = 4, "Blocked"


# Base model that will inherit in all models
class LogsMixin(models.Model):
    """Add the generic fields and relevant methods common to support mostly
    models
    """

    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """meta class for LogsMixin"""

        abstract = True

    @classmethod
    def get_objects(cls, **kwargs):
        return cls.objects.prefetch_related.filter(**kwargs)
