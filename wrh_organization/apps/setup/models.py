import uuid

from django.db import models
from rest_framework.utils.encoders import JSONEncoder


class FormsModel(models.Model):
    name = models.CharField(max_length=200)
    layout = models.JSONField(null=True, blank=True, encoder=JSONEncoder)

    def __str__(self):
        return self.name


class Criteria(models.Model):
    description = models.CharField(max_length=200)
    criteria = models.JSONField(null=True, blank=True, encoder=JSONEncoder)

    def __str__(self):
        return self.description


class CustomView(models.Model):
    Types = [
        (0, 'Event'),
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    type = models.IntegerField(choices=Types)
    name = models.CharField(max_length=100)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    is_default = models.BooleanField()