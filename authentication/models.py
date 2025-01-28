import uuid
from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    age = models.PositiveIntegerField(null=False)
    gender = models.CharField(max_length=10, null=True, blank=False)
    mobile_number = models.CharField(max_length=15, null=False)
    photo_url = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
