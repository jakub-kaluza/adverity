# Generated by Django 3.2.9 on 2021-11-07 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Metadata",
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
                ("download_date", models.DateTimeField()),
                ("filename", models.CharField(max_length=255)),
            ],
        ),
    ]
