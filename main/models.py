from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

import uuid

# Create your models here.
class Profil(models.Model) :
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['user'], name='user_unique_profil'),
            models.UniqueConstraint(fields=['email'], name='email_unique_profil')
        ]

    def __str__(self) :
        return self.name

class Playlist(models.Model) :
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    items = ArrayField(models.CharField(max_length=200))
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)