from django.db import models
from django.urls import reverse


class Collection(models.Model):
    file = models.FileField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("collections-detail", kwargs={"pk": self.pk})