# Generated by Django 4.1.6 on 2023-02-28 08:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "source_code",
                    models.URLField(blank=True, max_length=2000, null=True),
                ),
                (
                    "live_preview",
                    models.URLField(blank=True, max_length=2000, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
