# Generated by Django 5.0.6 on 2024-07-06 05:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("delty", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="selectedelement",
            name="hash",
            field=models.CharField(max_length=64),
        ),
    ]
