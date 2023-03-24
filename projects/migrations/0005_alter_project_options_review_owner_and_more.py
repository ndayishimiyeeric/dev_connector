# Generated by Django 4.1.6 on 2023-03-24 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_rename_date_to_experience_to_date"),
        ("projects", "0004_project_owner"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["created_at"]},
        ),
        migrations.AddField(
            model_name="review",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("owner", "project")},
        ),
    ]
