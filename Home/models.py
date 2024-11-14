from django.db import models


class BannerModel(models.Model):
    image = models.ImageField(upload_to=True)
    description = models.TextField()

    def __str__(self):
        return self.description


class ImageModel(models.Model):
    SECTION_IMAGE = [
        ('doctor', 'Doctor'),
        ('about', 'About'),
    ]
    img = models.ImageField(upload_to=True)
    type = models.CharField(max_length=150, choices=SECTION_IMAGE, default='doctor')
    about = models.ForeignKey('AboutUsModel', models.SET_NULL, 'images_about', blank=True, null=True)

    def __str__(self):
        return self.type


class AboutUsModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
