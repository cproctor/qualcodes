from django.db import models

# Create your models here.

class Code(models.Model):
    "A qualitative code to be applied to a piece of text"
    name = models.CharField('Name', max_length=200, unique=True)

    def __str__(self):
        return self.name

class Artifact(models.Model):
    text = models.TextField('Text')
    codes = models.ManyToManyField(Code, related_name='artifacts')
    user_id = models.CharField('User ID', max_length=200)
    column_id = models.CharField('Column ID', max_length=200)
