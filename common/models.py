from django.db import models


class CommonModel(models.Model):

    """Common MOdel Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
