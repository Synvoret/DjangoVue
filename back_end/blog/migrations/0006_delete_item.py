# Generated by Django 5.2 on 2025-05-16 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_profile_post_item"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Item",
        ),
    ]
