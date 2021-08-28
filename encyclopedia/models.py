from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=900)

    def __str__(self):
        return self.name
