# Generated by Django 5.0.6 on 2024-08-02 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("delty", "0006_alter_elementsnapshot_diff"),
    ]

    operations = [
        migrations.AddField(
            model_name="elementsnapshot",
            name="crawling_job",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="element_snapshots",
                to="delty.crawlingjob",
            ),
            preserve_default=False,
        ),
    ]
