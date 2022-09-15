from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMAIL = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = ("won", "Korean Won")
        USD = ("usd", "Dollar")

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    avatar = models.ImageField(blank=True)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
    genter = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    currency = models.CharField(max_length=5, choices=LanguageChoices.choices)