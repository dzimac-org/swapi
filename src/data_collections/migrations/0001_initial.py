# Generated by Django 4.2 on 2024-07-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(max_length=32, upload_to="")),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
