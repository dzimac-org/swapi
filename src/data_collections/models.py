from django.db import models
from django.urls import reverse


class Collection(models.Model):
    file = models.FileField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("collections-detail", kwargs={"pk": self.pk})


class SWPerson(models.Model):
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="persons"
    )
    name = models.CharField()
    birth_year = models.CharField()
    homeworld = models.CharField()
    height = models.CharField()
    mass = models.CharField()
    hair_color = models.CharField()
    skin_color = models.CharField()
    eye_color = models.CharField()
    gender = models.CharField()
    date = models.DateField()
