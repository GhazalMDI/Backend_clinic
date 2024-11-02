from django.db import models
from Home.models import ImageModel


class AboutUsModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
