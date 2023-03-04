from pathlib import Path

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.utils.encoders import JSONEncoder


def avatar_file_path_func(instance, filename):
    from wrh_organization.helpers.utils import get_random_upload_path
    return get_random_upload_path(str(Path('uploads', 'account', 'user', 'avatar')), filename)


class User(AbstractUser):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_OTHER = 'o'
    GENDER_UNKNOWN = 'u'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
        (GENDER_UNKNOWN, 'Unknown'),
    )

    email = models.EmailField(unique=True, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=avatar_file_path_func)
    more_data = models.JSONField(null=True, encoder=JSONEncoder, editable=False)
    prefs = models.JSONField(null=True, encoder=JSONEncoder, editable=False)
    draft = models.BooleanField(default=False, null=False, editable=False)
    agree_terms = models.BooleanField()
    privacy_policy_agree_date = models.DateTimeField()
    agree_waiver = models.BooleanField()
    agreement_waiver_agree_date = models.DateTimeField()
    opt_in_email = models.BooleanField(default=False)
    opt_in_email_agree_date = models.DateTimeField(null=True, blank=True)
    # verified_email = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.prefs:
            self.prefs = {}
        if self.email:
            self.email = self.email.lower()
        if self.username:
            self.username = self.username.lower()
        return super().save(*args, **kwargs)
