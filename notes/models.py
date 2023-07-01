from django.db import models

# Create your models here.
class MyNotes(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title